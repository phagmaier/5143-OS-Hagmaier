class Ready:
	def __init__(self):
		self.readyQueue = []
		self.send = False
		self.move = None
		self.job = None
	
	def addReady(self, jobs, algo):
		self.send = True
		for i in jobs:
			self.job = i
			self.job.priority = self.job.priorityCopy
			self.job.moved = True
			self.readyQueue.append(self.job)
		self.sort(algo)

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

	def pb(self):
		self.readyQueue.sort(key=lambda x: x.priority)
		return self.readyQueue.reverse()

	def sjf(self):
		return self.readyQueue.sort(key=lambda x: x.jobLength)

	def srj(self):
		return self.readyQueue.sort(key=lambda x: x.currentLength)

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


	def cpuWait(self):
		for i in self.readyQueue:
			i.CPUWaitTime += 1
			i.priority += .25

	def change(self):
		if len(self.readyQueue) > 0:
			for i in self.readyQueue:
				i.moved = False

	def __str__(self):
		self.s= ",".join([str(element.id) for element in self.readyQueue])
		return self.s
