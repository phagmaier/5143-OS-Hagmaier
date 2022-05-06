'''
initilize the cpu with the memory variable so that we can update memory
the termqueue is what we append to whenever we complete a operation inside our instructions
an operation is defined as something such as add r1 r2 it is one of the operations inside our instruction bloc
register values are initlily set to zero but will be updated with either prioirty register values or standard instruction
register values when an instruction block is added to the cpu
the ready variable indicates whether the cpu is busy and if we can add an instruction block into the cpu
sleeping is a boolean that indicates if the cpu is sleeping in which case we need to run sleepFunc
termMe indicates if an instruction is complete and needs to be added to the term object
if the process is interupted before being terminated interupted will be set to true
state shows what state the cpu is in used for when interupted so it is either load, running or term
self.numbers are the load r4 values the cpu finds when running a instruction block these numbers will be sent to the corresponding PCB

'''

import copy
class Cpu:
	import copy
	def __init__(self, memory):
		self.memory = memory
		self.termQueue = []
		self.r1 = 0
		self.r2 = 0
		self.r3 = 0
		self.sleeping = False
		self.ready = True #means ready to load
		self.runMe = False #means ready to be run
		self.termMe = False #means ready to be termianted
		self.addNum = False
		self.sleepTime = 0
		self.instructions = None
		self.interupted = None
		self.state = None
		self.numbers = []

	'''
  addNum tells us whether or not we found a load r4 and if so we need to send those values to the pcb 
  we return this to send to the pcb
  '''
	def addNumber(self):
		num = self.addNum
		self.addNum = False
		return num
  
  #checks to see if we have loaded the corresponding prioirty instruction
	def check(self, number):
		if number in self.numbers:
			return True
		else:
			return False
  '''
  Function that is called when a pcb sends a instruction block to the cpu
  need to pass in the corresponding register values and it sets the values
  here we also make sure the values are not too big so that we don't get ridiculously massive or small numbers
  we set runMe variable to True so we know to use run cpu function so we can processs our instruction block
  and we save the instruction in interupted in case we get interupted so we can update the cpu state to the pcb
  '''
	def addCpu(self, instructions, register1, register2):
		self.r1 = register1
		self.r2 = register2
		#in some runs numbers were too big
		if self.r1 >= 10000:
			self.r1 //= 100
		if self.r2 >= 10000:
			self.r2 //= 100
		self.runMe = True
		self.ready = False
		self.instructions = instructions
		self.interupted = instructions
  '''
  call this function when we have finished running instructions and need to send and then reset the termqueue inside our cpu
  '''
	def terminate(self):
		self.termMe = False
		self.ready = True
		self.runMe = False
		self.interupted = None
		sendToTerm = self.termQueue
		self.termQueue = []
		return sendToTerm
  
  '''
  called after we have loaded instructions into cpu we set termMe to true so we know we need to send the termqueue to the term object 
  runMe then is set to false because once this is called our instructions have been read and we save the state so that we can send it and update
  the pcb in case it is interupted 
  Instructions are ran by a while loop that runs through each item in the instructions block and sends it to be parsed and then it decrements the 
  list and once the intruction list is of length zero we are done
  '''
	def run(self):
		self.termMe = True
		self.runMe = False
		instructions = self.instructions
		while len(instructions) > 0:
			instruction = instructions[0]
			self.parse(instruction)
			instructions = instructions[1:]
		if len(self.termQueue) > 0:
			self.interupted = self.termQueue

	'''
  we split the single instruction to turn it into a list so it is easier to parse what instruction type we are looking at
  depending on what is in the first item of the split instruction we call the corresponding operation to be performed and sent to the termqueue
  '''
	def parse(self, instruction):
		og = instruction
		instruction = instruction.split()

		if instruction[0] == "ADD":
			self.add(instruction[1:])
			self.termQueue.append(og)

		elif instruction[0] == "SUB":
			self.sub(instruction[1:])
			self.termQueue.append(og)

		elif instruction[0] == "MUL":
			self.mul(instruction[1:])
			self.termQueue.append(og)

		elif instruction[0] == "DIV":
			self.div(instruction[1:])
			self.termQueue.append(og)

		elif instruction[0] == "READ":
			self.read(instruction[1:])
			self.termQueue.append(og)

		elif instruction[0] == "WRITE":
			self.write(instruction[1:])
			self.termQueue.append(og)

		elif instruction[0] == "LOAD":
			self.load(instruction[1], instruction[2])
			self.termQueue.append(og)

		elif instruction[0] == "sleep":
			self.sleep(instruction[1])
      
  '''
  adds the two register values and if the register value is too large or too small we decrement the values
  '''
	def add(self, instruction):
		reg1 = instruction[0]
		reg2 = instruction[1]
		if self.r1 >= 1000:
			self.r1 = 10
		if self.r2 >= 1000:
			self.r2 = 10
		if reg1[0:2] == "R1":
			self.r1 += self.r2
		elif reg1[0:2] == "R2":
			self.r2 += self.r1
		else:
			print("I messed up the parse")
			return
    
  '''
  subtracts the two register values and if the register value is too large or too small we decrement the values
  '''
	def sub(self, instruction):
		reg1 = instruction[0]
		reg2 = instruction[1]
		if self.r1 >= 1000:
			self.r1 = 10
		if self.r2 >= 1000:
			self.r2 = 10
		if self.r1 < 0:
			self.r1 = 1
		if self.r2 < 0:
			self.r2 = 1
		if reg1[0:2] == "R1":
			self.r1 -= self.r2
		elif reg1[0:2] == "R2":
			self.r2 -= self.r1
		else:
			print("I messed up the parse")
			return

   '''
  multiplies the two register values and if the register value is too large or too small we decrement the values
  '''
	def mul(self, instruction):
		reg1 = instruction[0]
		reg2 = instruction[1]
		if self.r1 >= 1000:
			self.r1 = 10
		if self.r2 >= 1000:
			self.r2 = 10
		if reg1[0:2] == "R1":
			self.r1 *= self.r2
		elif reg1[0:2] == "R2":
			self.r2 *= self.r1
		else:
			print("I messed up the parse")
			return
    
  '''
  divides the two register values and if the register value is too large or too small we decrement the values
  '''
	#do integer division just so it's cleaner numbers
	def div(self, instruction):
		reg1 = instruction[0]
		reg2 = instruction[1]
		if self.r1 >= 1000:
			self.r1 = 10
		if self.r2 >= 1000:
			self.r2 = 10
		if self.r1 < 0:
			self.r1 = 1
		if self.r2 < 0:
			self.r2 = 1
		if reg1[0:2] == "R1":
			if self.r2 == 0:
				self.r1 = self.r1
			else:
				self.r1 //= self.r2
		elif reg1[0:2] == "R2":
			if self.r1 == 0:
				self.r2 = self.r2
			else:
				self.r2 //= self.r1
		else:
			print("I messed up the parse")
			return

  '''
  Reads value in memory location to a register value
  '''
	def read(self, instruction):
		section = instruction[0][0]
		location = instruction[0][1:]
		register = instruction[1]
		if register == "R1":
			self.r1 = int(self.memory[section][location])
		elif register == "R2":
			self.r2 = int(self.memory[section][location])
		else:
			print("I messed up the Parse")
			return
    
   '''
  writes value in register to a memory location
  '''

	def write(self, instruction):
		section = instruction[1][0]
		location = instruction[1][1:]
		register = instruction[0]
		if register == "R1":
			self.memory[section][location] = self.r1
		elif register == "R2":
			self.memory[section][location] = self.r2
		else:
			print("I messed up the Parse")
			return
  '''
  loads value in r3 to r3 and r4 to r4 when we load an r4 
  we append that number to numbers to later send to pcb
  '''
	def load(self, instruction1, instruction2):
		if instruction2 == "R3":
			self.r3 = int(instruction1)
		elif instruction2 == "R4":
			self.addNum = int(instruction1)
			self.numbers.append(instruction1)
		else:
			print("I messed up the Parse")
			return
	'''
  save instruction. set termMe to false because instruction technically isn't done processing
  we set the sleep time to the corresponding value and save sleep to interupted so we know if interupted we are stil sleeping
  '''
	def sleep(self, instruction):
		instruction = int(instruction)
		self.interupted = 'sleep ' + str(instruction)
		self.term = False
		self.sleepTime = instruction
		self.sleeping = True
  
  '''
  decrements sleep time if it's zero set termMe to true to send to term queue and we set cpu so it's ready to accept a new instruction block
  '''
	def sleepFunc(self):
		self.sleepTime -= 1
		self.interupted = 'sleep ' + str(self.sleepTime)
		if self.sleepTime == 0:
			self.sleeping = False
			self.ready = True
			self.term = True
			self.termQueue.append("Sleep")
  '''
  get instructions that were in the cpu
  '''
	def getInterupt(self):
		return self.interupted
  
  '''
  get the state of the cpu was in before interupted by RR
  '''
	def getState(self):
		return self.state
	'''
  After each run get the register values so we can update the pcb register values
  '''
	def getRegValues(self):
		return [self.r1, self.r2]
  
  '''
  get the sleep value so we can load it into the pcb
  '''
	def getSleepTime(self):
		return self.sleepTime
  
  '''
  when round robin time slice ends and we switch to next process cpu is reset and everything is reset as if no instruction was ever loaded
  '''
	def reset(self):
		self.termQueue = []
		self.r1 = 0
		self.r2 = 0
		self.r3 = 0
		self.sleeping = False
		self.ready = True #means ready to load
		self.runMe = False #means ready to be run
		self.termMe = False #means ready to be termianted
		self.addNum = False
		self.sleepTime = 0
		self.instructions = None
		self.interupted = None
		self.state = None
  
  '''
  save all values to a list to send to pcb so we can load the cpu with the correct values after an interupt
  '''
	def saveState(self):
		copyTerm = copy.deepcopy(self.termQueue)
		copyInstructions = copy.deepcopy(self.instructions)
		return [copyTerm, self.r1, self.r2, self.r3, self.sleeping, self.ready, self.runMe, self.termMe, self.addNum, self.sleepTime, copyInstructions, self.interupted, self.state]
	
  '''
  reset cpu to the state it was in beofre the interupt
  '''
	def restore(self, state):
		if state == None:
			self.termQueue = []
			self.r1 = 0
			self.r2 = 0
			self.r3 = 0
			self.sleeping = False
			self.ready = True #means ready to load
			self.runMe = False #means ready to be run
			self.termMe = False #means ready to be termianted
			self.addNum = False
			self.sleepTime = 0
			self.instructions = None
			self.interupted = None
			self.state = None
		else:
			self.termQueue = state[0]
			self.r1 = state[1]
			self.r2 = state[2]
			self.r3 = state[3]
			self.sleeping = state[4]
			self.ready = state[5]
			self.runMe = state[6]
			self.termMe = state[7]
			self.addNum = state[8]
			self.sleepTime = state[9]
			self.instructions = state[10]
			self.interupted = state[11]
			self.state = state[12]
