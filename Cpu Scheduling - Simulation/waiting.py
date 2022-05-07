'''
A queue to store instructions waiting to use the IO
'''
class Waiting:
	def __init__(self):
		self.waitQueue = []
		self.send = False
		self.job = None
		self.move = None
	'''
	takes in jobs that have been moved of the cpu
	'''
	def addWaiting(self, job):
		self.send = True
		self.job = job
		self.job.moved = True
		self.waitQueue.append(self.job)
		self.sort()
	'''
	don't know why I didn't delete this
	'''
	def sort(self):
		pass
	'''
	when I move to an IO devise I need to remove the job from the queue and return the given job at the front of the queue 
	'''
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
	'''
	increments the IO wait time of every job in the queue
	'''
	def ioWait(self):
		for i in self.waitQueue:
			i.IOWaitTime += 1

				
	def __str__(self):
		self.s= ",".join([str(element.id) for element in self.waitQueue])
		return self.s
