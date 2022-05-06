from asyncio import threads
from dataclasses import dataclass
from sys import argv
import sys
import threading

import time
import copy
import json
from memory import createMem
from RandInstruction import RandInstructions
from collections.abc import MutableMapping
from random import randint
import random
from rich.panel import Panel
import threading
import time
from collections.abc import MutableMapping
blah=''
blah1=''
class RWLock:
    """
    The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7] 
    with a modification -- adding an additional lock (C{self.__readers_queue})
    -- in accordance with [2].
    """
    
    def __init__(self):
        self.__read_switch = _LightSwitch()
        self.__write_switch = _LightSwitch()
        self.__no_readers = threading.Lock()
        self.__no_writers = threading.Lock()
        self.__readers_queue = threading.Lock()
        """A lock giving an even higher priority to the writer in certain
        cases (see [2] for a discussion)"""
    
    def reader_acquire(self):
        self.__readers_queue.acquire()
        self.__no_readers.acquire()
        self.__read_switch.acquire(self.__no_writers)
        self.__no_readers.release()
        self.__readers_queue.release()
    
    def reader_release(self):
        self.__read_switch.release(self.__no_writers)
    
    def writer_acquire(self):
        self.__write_switch.acquire(self.__no_readers)
        self.__no_writers.acquire()
    
    def writer_release(self):
        self.__no_writers.release()
        self.__write_switch.release(self.__no_readers)
    

class _LightSwitch:
    """An auxiliary "light switch"-like object. The first thread turns on the 
    "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
    def __init__(self):
        self.__counter = 0
        self.__mutex = threading.Lock()
    
    def acquire(self, lock):
        self.__mutex.acquire()
        self.__counter += 1
        if self.__counter == 1:
            lock.acquire()
        self.__mutex.release()

    def release(self, lock):
        self.__mutex.acquire()
        self.__counter -= 1
        if self.__counter == 0:
            lock.release()
        self.__mutex.release()


class Reader(threading.Thread):
    def __init__(self, rw_lock, init_sleep_time, sleep_time,to_write,l,m,reg,cpu,num):
        """
        @param buffer_: common buffer shared by the readers and writers
        @type buffer_: list
        @type rw_lock: L{RWLock}
        @param init_sleep_time: sleep time before doing any action
        @type init_sleep_time: C{float}
        @param sleep_time: sleep time while in critical section
        @type sleep_time: C{float}
        """
        threading.Thread.__init__(self)
        self.__rw_lock = rw_lock
        self.__init_sleep_time = init_sleep_time
        self.__sleep_time = sleep_time
        self.__to_write = to_write
        self.buffer_read = None
        self.__l = l
        self.__registers = reg
        self.__num = num
        """a copy of a the buffer read while in critical section"""    
        self.entry_time = None
        """Time of entry to the critical section"""
        self.exit_time = None
        """Time of exit from the critical section"""

    def run(self,layout):
        #time.sleep(self.__init_sleep_time)
        global blah1
        rownum1=0
        for each in self.__to_write:
            time.sleep(random.random())
            self.__rw_lock.reader_acquire()
            self.entry_time = time.time()
            #time.sleep(self.__sleep_time)
            # each is a 4 line instruction set
            # each = ['READ A225 R1', 'READ A220 R2', 'ADD R1 R2', 'WRITE R1 A225']

            read1 = each[0]
            read2 = each[1]

            readvalue1 = self.__l.readMem(read1.split()[1])
            readvalue2 = self.__l.readMem(read2.split()[1])
            rownum1 = rownum1 + 1
            if (rownum1 == 20):
                blah1 = ""
                rownum1 = 0
            if read1.split()[2] == 'R1':
                self.__registers[0] = readvalue1
                blah1 = blah1 + "Reader " +str(self.__num)+ " reading from "+ read1.split()[1] +" - "+ str(self.__registers[0])+'\n'
                layout["body"].update(Panel(blah1, border_style="red"))
                #print("Reader " +str(self.__num)+ " reading from "+ read1.split()[1] +" - "+ str(self.__registers[0]))
            else:
                self.__registers[1] = readvalue1
                blah1 = blah1 + "Reader " +str(self.__num)+ " reading from "+ read1.split()[1] +" - "+ str(self.__registers[1])+'\n'
                layout["body"].update(Panel(blah1, border_style="red"))
                #print("Reader " +str(self.__num)+ " reading from "+ read1.split()[1]+" - " + str(self.__registers[1]))
            if (rownum1 == 20):
                blah1 = ""
                rownum1 = 0
            if read2.split()[2] == 'R1':
                self.__registers[0] = readvalue2
                blah1 = blah1 + "Reader " +str(self.__num)+ " reading from "+ read2.split()[1] +" - "+ str(self.__registers[0])+'\n'
                layout["body"].update(Panel(blah1, border_style="red"))
                #print("Reader " +str(self.__num)+ " reading from "+ read2.split()[1] +" - "+ str(self.__registers[0]))
            else:
                self.__registers[1] = readvalue2
                blah1 = blah1 + "Reader " +str(self.__num)+ " reading from "+ read2.split()[1] +" - "+ str(self.__registers[1])+'\n'
                layout["body"].update(Panel(blah1, border_style="red"))
                #print("Reader " +str(self.__num)+ " reading from "+ read2.split()[1] +" - "+ str(self.__registers[1]))
            
            # print("Reader " +str(self.__num)+ " reading " + str(self.__registers[0]))
            # print("Reader " +str(self.__num)+ " reading " + str(self.__registers[1]))
            self.exit_time = time.time()
            self.__rw_lock.reader_release()
            time.sleep(random.random())
        return self.__l


class Register:
    """Represents a single `register` with a read and write method
    to change the registers values.
    """

    def __init__(self):
        """Constructor"""
        self.contents = 0

    def write(self, x):
        """Change value of register"""
        self.contents = x

    def read(self):
        """Return value of register"""
        return self.contents

    def __str__(self):
        """Print out instance in readable format"""
        return f"[{self.contents}]"

    def __repr__(self):
        """Same as __str__"""
        return self.__str__()

class Registers(MutableMapping):
    """Represents a set of registers in an overloaded OOP fashion that
    allows for assignments to go like:
                r = Registers()
                r[0] = 44
                r[1] = 33
    """

    def __init__(self, num=2):
        """Constructor"""
        self.num = num
        self.registers = []
        for i in range(num):
            self.registers.append(Register())

    def __setitem__(self, k, v):
        """Assigns a value to a particular register as long as the key is
        integer, and within bounds.
        """
        if isinstance(k, int) and k < self.num:
            # setattr(self, self.registers[k], v)
            self.registers[k].write(v)

    def __getitem__(self, k):
        """Returns a value from a specific register indexed by `k`"""
        if isinstance(k, int) and k < self.num:
            # getattr(self, k)
            return self.registers[k].read()
        return None

    def __len__(self):
        """Len() of object instance. Must be here to overload class
        instance or python chokes.
        """
        return self.num

    def __delitem__(self, k):
        """Overloads the del keyword to delete something out of a
        list or dictionary.
        """
        if isinstance(k, int):
            self.registers[k] = None

    def __iter__(self):
        """Allows object iteration, or looping over this object"""
        yield self.registers

    def __str__(self):
        s = "[ "
        i = 0
        for r in self.registers:
            s += f"R{i}{str(r)} "
            i += 1
        return s + "]"

    def __repr__(self):
        return self.__str__()

def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return l * r


def div(l, r):
    return l / r

class OPERATION(object):
    def __init__(self, registers):
        self.reg1 = None
        self.reg2 = None
        self.operation = None
        self.registers = registers
        self.ops = {
        "ADD": add, 
        "SUB": sub, 
        "MUL": mul, 
        "DIV": div
        }

    def exec(self, operation):
        self.reg1 = self.registers[0]
        self.reg2 = self.registers[1]
        self.operation = operation.upper()
        ans = self.ops[self.operation](self.reg1, self.reg2)
        self.registers[0] = ans
        registers = self.registers
        return registers

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"

class Writer(threading.Thread):
    def __init__(self, rw_lock, init_sleep_time, sleep_time, to_write,l,m,reg,cpu,num):
        """
        @param buffer_: common buffer_ shared by the readers and writers
        @type buffer_: list
        @type rw_lock: L{RWLock}
        @param init_sleep_time: sleep time before doing any action
        @type init_sleep_time: C{float}
        @param sleep_time: sleep time while in critical section
        @type sleep_time: C{float}
        @param to_write: data that will be appended to the buffer
        """
        threading.Thread.__init__(self)
        self.__rw_lock = rw_lock
        self.__init_sleep_time = init_sleep_time
        self.__sleep_time = sleep_time
        self.__to_write = to_write
        self.__memory = m
        self.__l = l
        self.__registers = reg
        self.__cpu = cpu
        self.entry_time = None
        self.__num = num
        """Time of entry to the critical section"""
        self.exit_time = None
        """Time of exit from the critical section"""
        
    def run(self,layout):
        global blah
        rownum = 0
        for each in self.__to_write:
            time.sleep(random.random())
            blah = blah + "Before acquire writer" + str(self.__num)+"\n"
            layout["side"].update(Panel(blah, border_style="red"))
            
            self.__rw_lock.writer_acquire()
            self.entry_time = time.time()
            
            # each is a 4 line instruction set
            # each = ['READ A225 R1', 'READ A220 R2', 'ADD R1 R2', 'WRITE R1 A225']
            #print(each)
            read1 = each[0]
            read2 = each[1]
            action = each[2]
            write = each[3]
            readvalue1 = self.__l.readMem(read1.split()[1])
            readvalue2 = self.__l.readMem(read2.split()[1])
            if read1.split()[2] == 'R1':
                self.__registers[0] = readvalue1
            else:
                self.__registers[1] = readvalue1
            if read2.split()[2] == 'R1':
                self.__registers[0] = readvalue2
            else:
                self.__registers[1] = readvalue2
            # print(self.__registers[0])
            # print(self.__registers[1])
            alu = OPERATION(self.__registers)
            if action.split()[0] == 'ADD':
                self.__registers = alu.exec("add")
            if action.split()[0] == 'MUL':
                self.__registers = alu.exec("add")
            if action.split()[0] == 'SUB':
                self.__registers = alu.exec("add")
            if action.split()[0] == 'DIV':
                self.__registers = alu.exec("add")
            #print(self.__registers[0])
            self.__l.updateMem(write.split()[2],self.__registers[0])
            rownum = rownum + 1
            if (rownum == 40):
                blah = ""
                rownum = 0
            blah = blah + "Writer "+str(self.__num)+" - wrote to " + write.split()[2] + ' value - ' + str(self.__registers[0]) +'\n'
            layout["side"].update(Panel(blah, border_style="red"))
            #return self.__l
        #return self.__l
            self.exit_time = time.time()
            self.__rw_lock.writer_release()
            blah = blah + "After release writer" + str(self.__num)+"\n"
            layout["side"].update(Panel(blah, border_style="red"))
            time.sleep(random.random())
        return self.__l
