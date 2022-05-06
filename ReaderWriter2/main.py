#######################################
'''
This file is responable for running our program as well as creating all the files and storing instructions into the Pcb
It will also use rich to visulize the results of shared memory, what is in the cpu and the progress we have mave
Progress being defined as the number of instructions in the term queue compared to the total number of instructions in each file

'''
#######################################
from rich.console import Console
from rich.table import Table
from lock import Lock
from cpu import Cpu
from pcb import Pcb
from term import Term
import copy
import json
from readAhead import*
import random
from random import randint
from buildInstructions import*
import time
#from tqdm import tqdm
from rich.live import Live
from datetime import datetime
from time import sleep
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
#from rich.console import render_group
import random
import json
import sys,os

'''
CpuViz is responable for visualizing what is being held inside the CPU 
'''
class CpuViz:
  '''
  Initilize the class holding no instructions
  '''
	def __init__(self):
		self.instructions = None
  '''
  Whenever a instruction block is placed into the CPU we will
  call update to reflect those changes
  '''
	def update(self, instructions):
		if self.instructions == None:
			self.instructions = ["EMPTY"]
		else:
			self.instructions = instructions
  '''
  we call build table every time we want to use rich to display 
  the CpuViz object. Each instruction in the block should be displayed inside it own row under the
  Instruction column header
  '''
	def build_table(self):
		#if you wanted you could add a coulumn for if it's a privliged instruction
		table = Table(title = "CPU")
		table.add_column("Instruction", justify="center", style="cyan", no_wrap=True)
		for i in self.instructions:
			table.add_row(i)
		return table
  
  #Allows Rich to display our object 
	def __rich__(self):
		return Panel(self.build_table())
'''
A simple progress bar that will take in the length of instructions being sent to the term queue
In order to update the length and percentage completed
'''
class Prog_Bar:
    '''
    We initilize the total to the number of total instructions across the number of files created by the program
    prog is short for progress meaning the total amount of instructions completed.
    The bar variable dicates how many bars will be placed inside our progress bar to show percentage compled
    '''
    def __init__(self, total):
        self.total = total
        self.prog = 0
        self.percent = 0.0
        self.bar = "┃" * int(self.percent) + '-' * (100 - int(self.percent))
     '''
     Called every time we send instructions to the termQueue to update the bar length and reflect an accurate percentage
     '''
    def update(self, prog):
        self.prog += prog
        self.percent = 100 * (self.prog / float(self.total))
        self.bar = "┃" * int(self.percent) + '-' * (100 - int(self.percent))
    def __rich__(self):
        return Panel(f"┃{self.bar}┃ {self.percent:.2f}%")
'''
MemRich is the class that allows us to display the shared memory values
It takes in the memory variable which is dictionary memory values have 31 locations
to make it easy I manually put in the 31st location so rows and columns only account for the first thirty values
'''
class MemRich:
	def __init__(self, memory):
		self.memory = memory["P"]
		self.columns = 6
		self.rows = 5
  #Each time the CPU runs an insruction this will update to reflect the possible changes in shared memory
	def update(self, memory):
		self.memory = memory['P']
		self.keys = self.memory.keys()
  '''
  This is called when we want to print or display out table it will build the table with each column being a 
  range of values five values incrimented by 5 excet for the final column which just shows location 250
  Use a for loop to generate rows and columns each row is the next memroy location in that range
  '''
	def build_table(self):
		total = 30 
		columns = 6
		rows = 5
		ranges = ["100-120", "125-145", "150-170", "175-195", "200-220", "225-145"]
		num = 100
		table = Table(title= "Protected Memory")
		for i in range(columns):
			table.add_column(ranges[i], justify="center", style="cyan", no_wrap=True)
		table.add_column("250")
		#pretty sure the best way to do this is with list comprehension but I'm lazy and don't
		#want to mess this up 
		for i in range(rows):
			if i == 0:
				table.add_row(str(self.memory[str(num)]),  str(self.memory[str(num+5)]), str(self.memory[str(num+10)]), str(self.memory[str(num+15)]), str(self.memory[str(num+20)]),str(self.memory[str(num+25)]), str(self.memory["250"]))
			else:
				table.add_row(str(self.memory[str(num)]),  str(self.memory[str(num+5)]), str(self.memory[str(num+10)]), str(self.memory[str(num+15)]), str(self.memory[str(num+20)]),str(self.memory[str(num+25)]), None)
			num += 30
		return table

	def __rich__(self):
		return Panel(self.build_table())

'''
numFiles is what allows users to input how many instruction files they wish to generate
console is used in rich to be able to generate our visuals
Layout splits the console into sections so we can display to different sections
The CPU visuals are in the header section
shared memory is in the main location of Layout
progress bar is displayed in the footer section fo the layout
'''
#################################################################################
numFiles = input("Enter the number of files you want to generate: ")
numFiles = int(numFiles)
console = Console()
layout = Layout()

layout.split(
    Layout(name = "header"),
    Layout(name = "main"),
    Layout(name = "footer")
)
#################################################################################

'''
start function is what we call to run our program.
We grab our json file which is saved as memory.json
We make 4 copies of this variable (deep copies) so each run can have the same original memory
chnagesleeps will hold the instructions after the sleeps have all been changed 
rrNum will generate a random number between 7 and 11 inclusive that will be used as our round robin time slice
Call generateFiles to create .exe instruction files. Numinstructions is passed to determine how many of these instructions will be run
We also make 4 deep copies of these instructions to make sure they each get the original instructions
We then run a for loop the number of runs determined by the number of files we create in order to determine the total number instructions generated
Across all files

The next for loop (structure if i == 1 ect... will dictate which run we will perform. 
run one or when i == 0 will run using the our original instructions without changing sleep values and will not take prioirty instructions
into account meaning prioirty or shared memory instructions will be treated like any other instruction. We call the noprioirty function. which is the 
function that handles how to run all instructions without taking into account locks or differentiating privliged instructions. We must also load 
The instruction file into the PCBs as well as create all our pcb objects

Run 2 or when i == 1 is the same as above excpet we will change the sleep values. THe shared memory of P should be different from the first 
run as a result of this

Run 3 will run our prioirtyFunc. Before doing that we create our PCBS the way we do in our first two runs the only difference being we use the 
readAhead function in order to store privliged isntructions inside our prioirtyQueue inside the PCB.

Run 4 will do the same thing as run 3 except we change the instruction sleep values which are stored inside the PCB
'''

def start():
	memory = getMemory()
	memory2 = copy.deepcopy(memory)
	memory3 = copy.deepcopy(memory)
	memory4 = copy.deepcopy(memory)
	changesleeps = []
	numInstructions = 0
	rrNum = randint(7,12)
	generateFiles(numFiles)
	instructions = fileToVariable(numFiles)
	instructions2 = copy.deepcopy(instructions)
	instructions3 = copy.deepcopy(instructions)
	instructions4 = copy.deepcopy(instructions)
	for i in instructions:
		numInstructions += total(i)

	for i in range(4):
		if i == 0:
			pcbs = load(numFiles, instructions)
			noPriority(rrNum, numFiles, memory, pcbs, numInstructions)
		if i == 1:
			for i in range(numFiles):
				changesleeps.append(changeSleep(instructions2[i]))
			changesleeps2 = copy.deepcopy(changesleeps)
			pcbs = load(numFiles, changesleeps)
			noPriority(rrNum, numFiles, memory2, pcbs, numInstructions)
		if i == 2:
			pcbs = []
			for i in range(numFiles):
				pcb = Pcb()
				pcb = getInstructions(instructions3[i], pcb)
				pcbs.append(pcb)
			prioriyFunc(rrNum, numFiles, memory3, pcbs, numInstructions)
		if i == 3:
			pcbs = []
			for i in range(numFiles):
				pcb = Pcb()
				pcb = getInstructions(changesleeps2[i], pcb)
				pcbs.append(pcb)
			prioriyFunc(rrNum, numFiles, memory4, pcbs, numInstructions)

#We just turn the json file into a dictionary variable
def getMemory():
	f = open('memory.json')
	data = json.load(f)
	return data

#change the sleep values for our instruction files
def changeSleep(instruction):
	for i in range(len(instruction)):
		for x in range(len(instruction[i])):
			if instruction[i][x][0] == "s":
				instruction[i][x] = "sleep " + str(randint(1, 16))
	return instruction

'''
We create PCBs and append it to the pcbs list. Before doing this we call the pcb method get file which takes a list of all our instructions
'''
def load(num, insts):
	pcbs = []
	for i in range(num):
		pcb = Pcb()
		pcb.getFile(insts[i])
		pcbs.append(pcb)
	return pcbs

#gets the total number of instructions inside each instruction file each instruction such as ADD R2 R1 is considered one instruction
def total(instructions):
	total = 0
	for i in instructions:
		for x in i:
			total += 1
	return total

#function given to use by Professor griffen. Generates our .exe instruction files
def generateFiles(num):
	 ri = RandInstructions(privilegedRatio=0.3, sleepRatio=0.15, numProcesses= num)

#converts the newly created .exe instruction files into a list variable stored here in files
def fileToVariable(num):
	files = []
	for i in range(num):
		name = 'program_' + str(i) + '.exe'
		f = open(name)
		data = json.load(f)
		files.append(data)
	return files

'''
prioirtyFunc takes rrNum which is the round robin time slice which determines the time slice for when one process 
gets time on the CPU. numFiles is the amount of files and thefore the number of PCBs that are created (each PCB is responsable for 1 instruction file)
memory holds the dictionary of values saved inside the memory. PCBs holds the pcbs in a list and numInstructions is the total number of instructions
cumulative calculated by summing the number of instructions in each file this variable is used to determine how far along in the run we are as well
as dictating when to stop the while loop

We create all our objects cpu, term, and lock (PCB objects are created inside the start function and passed as a list into prioirtyFunc)
Infinite variable just makes sure the while loop does not run forever it is cut off at one hundred thousand clock ticks
count is how many clock ticks have been run for each round robin. so if round robin is 7 each proccess get 7 clock ticks on cpu
Once count is 7 we set it back to zero and we switch which process gets CPU time
which PCB is being used by the function
lockNum is the prioirty instruction that needs to be run and the lock can only be accessed and shared memory instructions can only be run
if that shared instruction is in the pcb and able to be run by the cpu

ttheCpu, bar, and memoryViz are the objects that allow us to display what is in the CPU, how much progress we have made in the run and the values
inside shared memory

each if statment dictates what we should do inside that clock tick: send to the termQueue, run an instruction, load a regular instruction into the cpu,
and load a prioirty instruction into the cpu
if CPU state is sleeping we run sleep
if termMe is tue we send instructions that were in CPU to the termQueue and update the progress bar
if the current prioirty instruction is indide the PCB and therfore instruction file that has CPU time and the CPU is not busy we load a prioirty instruction
if we cannot load a prioirty instruction and we havent completed all our standard instructions we load a standard instruction block into the cpu
if runMe is true inside the CPU we run instructions that have been loaded into the cpu
Each time one of these actions is perfomed we save the state of the cpu into the PCB in order to keep track of the state in case a process is interupted
and kciked off due to the round robin time slice. if count is the same as the round robin time slice value (rrNum) we switch which process/pcb gets CPU time

We then load the state that is saved into the pcb into the cpu and we pick up from where we got interupted
'''
def prioriyFunc(rrNum, numFiles, memory, pcbs, numInstructions):
	memory = memory
	cpu = Cpu(memory)
	term = Term()
	pcbs = pcbs
	lock = Lock()

	infinite = 0
	rrNum = rrNum
	count = 0
	lockNum = 0
	pcbNum = 0

	theCpu = CpuViz()
	bar = Prog_Bar(numInstructions)
	memoryViz = MemRich(memory)


	while len(term.termQueue) <= numInstructions and infinite < 1000000:

		if cpu.sleeping == True:
			cpu.sleepFunc()
			pcbs[pcbNum].getCpuState(cpu.saveState())
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

		elif cpu.termMe == True:
			termVar = cpu.terminate()
			length = len(termVar)
			term.add(termVar)
			bar.update(length)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)
			
			if pcbs[pcbNum].sentPriority == True:
				lockNum += 1
				lock.setLock()
			pcbs[pcbNum].sentPriority = False
			pcbs[pcbNum].getCpuState(cpu.saveState())

		elif cpu.runMe == True:
			cpu.run()

			memoryViz.update(cpu.memory)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

			pcbs[pcbNum].getCpuState(cpu.saveState())
			if cpu.addNum != False:
				pcbs[pcbNum].addNum(cpu.addNumber())
			if pcbs[pcbNum].sentPriority == False:
				pcbs[pcbNum].setReg(cpu.r1, cpu.r2)
			else:
				pcbs[pcbNum].setPrioirtyReg(cpu.r1, cpu.r2)

		elif lock.unlock(lockNum) == True  and pcbs[pcbNum].betterCheck(lockNum) == True and cpu.ready == True:
			anInstruction = pcbs[pcbNum].getPrioirty(lockNum)
			cpu.addCpu(anInstruction, Pcb.pReg1, Pcb.pReg2)
			pcbs[pcbNum].sentPriority = True
			pcbs[pcbNum].getCpuState(cpu.saveState())

			theCpu.update(anInstruction)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

		elif cpu.ready == True and pcbs[pcbNum].read == True:
			anotherInstruction = pcbs[pcbNum].getInstruction()
			cpu.addCpu(anotherInstruction, Pcb.reg1, Pcb.reg2)
			pcbs[pcbNum].getCpuState(cpu.saveState())
			theCpu.update(anotherInstruction)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

		count += 1
		infinite += 1

		if count == rrNum:
			if pcbNum == (numFiles - 1):
				pcbNum = 0
			else:
				pcbNum += 1
			cpu.restore(pcbs[pcbNum].restoreCpuState())
			count = 0

	#print("The length of the term queue is:")
	#print(len(term.termQueue))
	#print("The number of instructions is: " + str(numInstructions))
	#print(memory)
	#print(term.termQueue)
	#print(term.termQueue)
	#print(memory['P'])

  
  
'''
noPriority takes rrNum which is the round robin time slice which determines the time slice for when one process 
gets time on the CPU. numFiles is the amount of files and thefore the number of PCBs that are created (each PCB is responsable for 1 instruction file)
memory holds the dictionary of values saved inside the memory. PCBs holds the pcbs in a list and numInstructions is the total number of instructions
cumulative calculated by summing the number of instructions in each file this variable is used to determine how far along in the run we are as well
as dictating when to stop the while loop

We create all our objects cpu, term, and lock (PCB objects are created inside the start function and passed as a list into prioirtyFunc)
Infinite variable just makes sure the while loop does not run forever it is cut off at one hundred thousand clock ticks
count is how many clock ticks have been run for each round robin. so if round robin is 7 each proccess get 7 clock ticks on cpu
Once count is 7 we set it back to zero and we switch which process gets CPU time
which PCB is being used by the function
lockNum is the prioirty instruction that needs to be run and the lock can only be accessed and shared memory instructions can only be run
if that shared instruction is in the pcb and able to be run by the cpu

theCpu, bar, and memoryViz are the objects that allow us to display what is in the CPU, how much progress we have made in the run and the values
inside shared memory

each if statment dictates what we should do inside that clock tick: send to the termQueue, run an instruction, load a regular instruction into the cpu,
and load a prioirty instruction into the cpu
if CPU state is sleeping we run sleep
if termMe is tue we send instructions that were in CPU to the termQueue and update the progress bar
if runMe is true inside the CPU we run instructions that have been loaded into the cpu
Each time one of these actions is perfomed we save the state of the cpu into the PCB in order to keep track of the state in case a process is interupted
and kciked off due to the round robin time slice. if count is the same as the round robin time slice value (rrNum) we switch which process/pcb gets CPU time

We then load the state that is saved into the pcb into the cpu and we pick up from where we got interupted
'''
def noPriority(rrNum, numFiles, memory, pcbs, numInstructions):
	memory = memory
	cpu = Cpu(memory)
	term = Term()
	pcbs = pcbs
	lock = Lock()

	infinite = 0
	rrNum = rrNum
	count = 0
	lockNum = 0
	pcbNum = 0

	theCpu = CpuViz()
	bar = Prog_Bar(numInstructions)
	memoryViz = MemRich(memory)

	while len(term.termQueue) <= numInstructions and infinite < 1000000:
		if cpu.sleeping == True:
			cpu.sleepFunc()
			pcbs[pcbNum].getCpuState(cpu.saveState())
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

		elif cpu.termMe == True:
			termingStuff = cpu.terminate()
			length = len(termingStuff)
			term.add(termingStuff)
			
			bar.update(length)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

			if pcbs[pcbNum].sentPriority == True:
				lockNum += 1
				lock.setLock()
			pcbs[pcbNum].sentPriority = False
			pcbs[pcbNum].getCpuState(cpu.saveState())

		elif cpu.runMe == True:
			cpu.run()
			pcbs[pcbNum].getCpuState(cpu.saveState())
			if cpu.addNum != False:
				pcbs[pcbNum].addNum(cpu.addNumber())
			if pcbs[pcbNum].sentPriority == False:
				pcbs[pcbNum].setReg(cpu.r1, cpu.r2)
			else:
				pcbs[pcbNum].setPrioirtyReg(cpu.r1, cpu.r2)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

		elif cpu.ready == True and pcbs[pcbNum].read == True:
			aInstruction = pcbs[pcbNum].getInstruction()
			cpu.addCpu(aInstruction, Pcb.reg1, Pcb.reg2)
			pcbs[pcbNum].getCpuState(cpu.saveState())
			theCpu.update(aInstruction)
			layout["footer"].update(bar)
			layout["main"].update(memoryViz)
			layout["header"].update(theCpu)
			time.sleep(.01)

		count += 1
		infinite += 1

		if count == rrNum:
			if pcbNum == (numFiles - 1):
				pcbNum = 0
			else:
				pcbNum += 1
			cpu.restore(pcbs[pcbNum].restoreCpuState())
			count = 0

'''
with Live allows us to dynamically update our visuals as they take place inside out function
we call start() inside with Live so that our visuals will update as they occur and we don't have to create a new table
or progress bar each time it is updated
'''
with Live(layout, screen=True, redirect_stderr=False) as live:
    start()
    try:
        while True:
            sleep(0)
    except KeyboardInterrupt:
        pass
