from asyncio import threads
from sys import argv
import sys
# import threading
# import unittest
import threading
import time
import json
from memory import createMem
from RandInstruction import RandInstructions
from collections.abc import MutableMapping
from random import randint, shuffle
import random
from Rich_Layout import *
from RWlock import *

"""
class:                  Main


"""

class Main:

    """
    name:                   __init__
    parameters:             self
    returns:                N/A
    purpose:                construct an object of the Main class.
    """
    def __init__(self):
        self.memory = {}
        for section in range(3):
            section = str(chr(section + 65))
            self.memory[section] = {}
            for i in range(100, 255, 5):
                r = random.randint(1,9)
                self.memory[section][i] = r
        with open("memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)
    
    """
    name:                   updateMem
    parameters:             self, place, value
    returns:                N/A
    purpose:                updates the memory location with the new value
    """
    def updateMem(self,place,value):
        block = place[:1]
        location = place[1:]
        self.memory[block][int(location)] = value

    """
    name:                   readMem
    parameters:             self, loc
    returns:                the value in the specified memory location
    purpose:                returns a single memory location inside the chosen memory block (A,B,C)
    """
    def readMem(self,loc):
        block = loc[:1]
        location = loc[1:]
        return self.memory[block][int(location)]

    """
    name:                   localMem
    parameters:             self
    returns:                the total updated memory
    purpose:                returns the entire memory
    """
    def localMem(self):
        return self.memory

"""
class:                      CPU
"""
class StringArithmetic:
    """
    name:                   __init__
    parameters:             self, registers
    returns:                N/A             
    purpose:                To construct an object of the CPU CLASS
    """
    def __init__(self, registers):
        self.cache = []
        self.pc = 0
        self.registers = registers
        self.operation = OPERATION(registers)


    """
    name:               __str__
    parameters:         self
    return:             string version of the registers and the arithmetic operations values
    purpose:            returns a string version of the registers and arithmetic operation
    """
    def __str__(self):
        return f"[{self.registers}{self.operation}]"

"""
name:                   generateInstructions
parameters:             instr, numofwriters
returns:                instrList
purpose:                to check if the param instr is local or nonlocal, meaning threads can only lock down one secion of memory A,B,C or
                        allowed to access all memory blocks. It will create random instructions and append them to the instrList.
                        At the end the list will be returned
"""
def generateInstructions(instr,numWriters):
    # boolean variable, if we are using local or nonlocal variable
    local=False
    # list of instructions
    instrList = []
    if instr == "local":
        local = True
    elif instr == "nonlocal":
        local = False
    # add random instructions to the list
    for i in range(1,int(numWriters)+1):
        ri = RandInstructions(localInst=local,outFile="writer"+str(i)+".json",readerThread = False)
        instrList.append(ri.getList())
    for i in range(1,(int(numWriters)*5)+1):
        ri = RandInstructions(localInst=local,outFile="reader"+str(i)+".json",readerThread = True)
        instrList.append(ri.getList())
    return instrList


if __name__ == '__main__':
        # create an object of the main class
        the_main = Main()
        # call the class method localMem
        m = the_main.localMem()
        # open json file
        with open("memory.json") as f:
            dataf = json.load(f)
        # create our layout for the terminal
        layout = make_layout()
        layout["header"].update(Header())
        layout["side"].update(Panel("Writers - ", border_style="red")) 
        layout["body"].update(Panel("Readers - ", border_style="red")) 
        
        # create our live loop
        with Live(layout, screen=True, redirect_stderr=False) as live:
            
                amount_writers = sys.argv[1]
                inputInstr = sys.argv[2] 
                amount_writers = int (amount_writers)
                amount_readers = int(amount_writers * 5)


                # create instructions for our simulation
                instructions = generateInstructions(inputInstr,amount_writers)
                # create an object of RWLock class. 
                rw_lock = RWLock()
                # list to hold both reader and writer threads
                threadsList = []              
                # create the amount of registers
                reg = Registers(2)
                # create an object of the StringArithmetic class
                arith = StringArithmetic(reg)
                
                # append the writers to the threadList
                for i in range(int(amount_writers)):
                    threadsList.append((Writer(rw_lock,0,0.1,instructions[i],the_main,m,reg,arith,1)))

                # append the readers to the threadList
                for i in range((amount_readers)):
                    threadsList.append(Reader(rw_lock,0.1,0.2,instructions[i],the_main,m,reg,arith,1))

                # shuffle the threads so they are not in order
                shuffle(threadsList)

                # loop through the threads in the threadlist
                for thread in threadsList:
                    start = thread.run(layout)
                    x = start
                # join the writer threads where it will lock down then continue when it releases
                for thread in threadsList:
                    thread.join()
                    

                # write to memory.json with the updated memory values
                with open("memory.json", "w") as f:
                    json.dump(the_main.localMem(), f, indent=4)
                with open("memory.json") as f:
                    data = json.load(f)           
