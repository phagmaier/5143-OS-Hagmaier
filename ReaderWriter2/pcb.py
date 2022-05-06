'''
we have 4 static variables and each contains a register value
pReg1 and pReg2 sotre the values of the prioirty register values
this is static because not every pcb will have the every prioirity instructiona and thus different register values
This is just an easy way to make sure they all have the proper register values in order
The same goes with reg1 and reg2 only these store the register values for regular instruction register values
This will also be shared across objects although we update these values each context switch to updatw with values stored in self.r1 self.r2 ect...
It doesn't necissarily need to be static and as I am writting this it now seems somewhat pointless

noPlaceToGo is a list and stores prioirty instructions that don't have an associated prioirty instruction value
once a load R4 is found these instructions become the first instructions inside that prioirty instruction
prioirty queue stores all our key value pairs in a dictionary.
each key is a load r4 and all values are instructions that follow before the next load r4
read boolean informs us if we still have instructions that need to be read and sent to the CPU when we have loaded all instructions and our instructions
list is of length zero it switches to false
instructions stores all instructions as a list

numbers stores what prioirty instructions are associated with each pcb and when a r4 instruction is loaded it is appended to numbers in order to let 
our main function know that we can run this particular prioirty instruction with this particular pcb

interupted tells us if were interupted any time before terminating an instruction and in that case we have to restore the state of the cpu when 
this particular pcb gets time on the cpu 

sleeptime stores the time left on interupted sleep instructions
cpustate is the state we were in when interupted i.e we just loaded a instruction or just ran an instruction
sent prioirty tells us if we have sent a prioirty instruction. We do this so when we termiante an instruction
we can incriment our lock to tell us which prioirty instruction to look for next and keeps the order

'''

import copy
class Pcb:
	import copy
	#saves value of prioirty registers has to be static so we can go in order with
	#correct values
	pReg1 = 0
	pReg2 = 0
	reg1 = 0
	reg2 = 0
	def __init__(self):
		self.noPlaceToGo = []
		self.priorityQueue = {}
		self.num = None
		self.instructions = None
		self.read = True #whn false it means no more instructions left to read
		#standad rgisters
		self.r1 = 0 
		self.r2 = 0
		self.r3 = 0
		self.numbers = []
		self.interupted = None
		self.state = None
		self.sleepTime = 0
		self.cpuState = None
		self.sentPriority = False

  #saves all information that was in cpu inside a list
	def getCpuState(self, state):
		self.cpuState = copy.deepcopy(state)
  
  #return the cpu state so that after an interupt we can set the cpu back to the state it was in when interupted
	def restoreCpuState(self):
		return self.cpuState
  
  #gets the sleep time or how many more clock ticks a sleep instruction has left after getting interupted
	def getSleepTime(self, time):
		self.sleepTime = time

  #if we get interupted after a load into cpu we save that instruction to self.interupted
	def getInterupted(self, instruction):
		self.interupted = instruction
		
  #called whenever we encounter a load r4 to know that we have that prioirty instruction inside this particular PCB
	def addNum(self, num):
		self.numbers.append(num)
  
  #sets the prioirty register values when we load a prioirty instruction into the cpu 
	def setPrioirtyReg(self, reg1, reg2):
		Pcb.pReg1 = reg1
		Pcb.pReg2 = reg2
  
  #when a regular instruction is run we save the register values
	def setReg(self, reg1, reg2):
		Pcb.r1 = reg1
		Pcb.r2 = reg2
  
  #used when reading ahead so that we can save our prioirty instructions away from regular instructions
  #if noPlace is not empty that becomes the value inside this prioirty instruction
  #this function essentially sets the key value each time we encounter a load r4 inside cpu
	def addPriority(self, num):
		self.num = num
		#self.listOfNums.append(num)
		if len(self.noPlaceToGo) > 0:
			self.priorityQueue[num] = self.noPlaceToGo
			self.noPlaceToGo = []
		else:
			self.priorityQueue[num] = []
  
  #when we encounter a prioirty instruction we append it to the latest prioirty instruction ket value saved is self.num
	def appendPriority(self, inst):
		try:
			self.priorityQueue[self.num].append(inst)
		except:
			self.noPlaceToGo.append(inst)
			if self.num:
				print("You messed up somehow!")
  
  #calle in our main to load instruction file variable into our pcb
	def getFile(self, file):
		self.instructions = file
  
  #when we want to load an insttruction into cpu we call getInstruction and it returns the first list of instructions
  #it then deletes that instruction from our self.instructions list
	def getInstruction(self):
		self.instruction = self.instructions[0]
		self.instructions = self.instructions[1:]
		if len(self.instructions) == 0:
			self.read = False
		return self.instruction
	
  #if we have the desired prioirty instruction and we are unlocked we can get the values inside the corresponding prioirty instruction and return it
	def getPrioirty(self, num):
		return self.priorityQueue[num]
  
  #checks if the prioirty instruction we are on exists within our particular pcb
	def check(self, num):
		if num in self.numbers:
			return True
		else:
			return False
    
  #checks if the prioirty instruction we are on exists within our particular pcb
	def betterCheck(self, num):
		if num in self.priorityQueue.keys():
			return True
		else:
			return False
