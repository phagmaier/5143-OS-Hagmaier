'''
Initilized as an empty list to store values waiting to use CPU
'''
class Ready:
	def __init__(self):
		self.readyQueue = []
		self.send = False
		self.move = None
		self.job = None
	'''
	when added to ready we store values of the jobs and sent moved to True so no other action can be taken in the clock tick
	'''
	def addReady(self, jobs, algo):
		self.send = True
		for i in jobs:
			self.job = i
			self.job.priority = self.job.priorityCopy
			self.job.moved = True
			self.readyQueue.append(self.job)
		self.sort(algo)
	'''
	depending on the algorithm the corresponding sort function will be called.
	'''
	def sort(self, algo):
		if algo == 'sjf':
			return self.sjf()
		elif algo == 'srj':
			return self.srj()
		elif algo == 'pb':
			return self.pb()
		elif algo == 'rr':
			pass
		elif algo == 'fcfs':
			pass
		else:
			print('Not built yet!')
	'''
	sorts the readyQueue by prioirty
	'''
	def pb(self):
		self.readyQueue.sort(key=lambda x: x.priority)
		return self.readyQueue.reverse()
	'''
	sorts by the shortest total cpuBurst number
	'''
	def sjf(self):
		return self.readyQueue.sort(key=lambda x: x.jobLength)
	'''
	sorts by the shortest remaining time of total cpuBursts remaining
	'''
	def srj(self):
		return self.readyQueue.sort(key=lambda x: x.currentLength)
	
	'''
	when the cpu is not busy this functin is called to send the first item in the queue to the cpu
	'''
	def sendCpu(self):
		for i in range(len(self.readyQueue)):
			if self.readyQueue[i].moved == False:
				self.move = self.readyQueue[i]
				self.readyQueue.remove(self.move)
				#for this and the waiting Queue you shouldn't automatically switch it to false
				#only switch to false if the the readyQueue is empty 
				if len(self.readyQueue) == 0:
					self.send = False
				return self.move
			if i == len(self.readyQueue) - 1 and self.readyQueue[i].moved == True:
				self.move = None 
				return self.move

	'''
	increment the wait time for every job in the queue
	'''
	def cpuWait(self):
		for i in self.readyQueue:
			i.CPUWaitTime += 1
			i.priority += .25
	'''
	when moved we call change to indicate an action was taken in the clock tick and another cannot be made
	'''
	def change(self):
		if len(self.readyQueue) > 0:
			for i in self.readyQueue:
				i.moved = False

	def __str__(self):
		self.s= ",".join([str(element.id) for element in self.readyQueue])
		return self.s
