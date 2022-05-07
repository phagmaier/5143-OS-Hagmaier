class Waiting:
	def __init__(self):
		self.waitQueue = []
		self.send = False
		self.job = None
		self.move = None

	def addWaiting(self, job):
		self.send = True
		self.job = job
		self.job.moved = True
		self.waitQueue.append(self.job)
		self.sort()

	def sort(self):
		pass

	def sendIo(self):
		for i in range(len(self.waitQueue)):
			if self.waitQueue[i].moved == False:
				self.move = self.waitQueue[i]
				self.waitQueue.remove(self.move)
				if len(self.waitQueue) == 0:
					self.send = False
				return self.move
			if i == len(self.waitQueue) - 1 and self.waitQueue[i].moved == True:
				#self.send = True
				self.move = None
				return self.move

	#function to change anything in waitQueue that was just moved 
	#to indicate that it can now be moved to the IO
	def change(self):
		if len(self.waitQueue) > 0:
			for i in self.waitQueue:
				i.moved = False

	def ioWait(self):
		for i in self.waitQueue:
			i.IOWaitTime += 1

				
	def __str__(self):
		self.s= ",".join([str(element.id) for element in self.waitQueue])
		return self.s