class Cpu:
	def __init__(self, algo, timeSlice):
		self.algo = algo
		self.timeSlice = timeSlice 
		self.busy = False
		self.job = None
		self.moving = False
		self.term = False
		self.move = None
		self.pause = False
		self.moveReady = False
		self.currentTime = 0
	def recieve(self, job):
		if job != None:
			self.job = job
			self.busy = True

	def moveToTerm(self):
		self.term = True
		self.move = self.job
		self.job = None
		self.busy = False
		self.pause = True #might not need this but idk
		return self.move

	def moveToWaiting(self):
		self.job.cpuBursts = self.job.cpuBursts[1:]
		self.moving = True
		self.move = self.job
		self.job = None
		self.busy = False
		self.pause = True
		return self.move

	#think this moveToReady should work as long as it is the same as 
	#moveToWaiting but not sure and haven't tested it yet 
	def moveToReady(self):
		self.moving = True
		self.move = self.job
		self.job = None
		self.busy = False
		self.pause = True
		self.moveReady = True
		return self.move
	#Ya you're going to have to change it to where the 
	#CPU is create with the algo and timeslice because it needs to be saved 
	#will probably also need a variable that is reset to zero after the 
	#time slize is reached to make sure that it only runs for that alloted time slice
	def run(self):
		self.algos = ['pb', 'fcfs', 'sjf', 'srj']
		if self.algo == 'rr':
			self.rrRun()
		elif self.algo in self.algos:
			self.regularRun()
		else:
			print('ERROR: I do not recognize that algorithm!!')
			return

	def rrRun(self):
		self.job.cpuBursts[0] -= 1
		self.currentTime += 1
		if self.job.cpuBursts[0] == 0:
			if len(self.job.cpuBursts) > 1:
				self.moveToWaiting()
			else:
				self.moveToTerm()
		elif self.currentTime == self.timeSlice:
			self.moveToReady()

	def regularRun(self):
		self.job.cpuBursts[0] -= 1
		self.job.currentLength -= 1
		if self.job.cpuBursts[0] == 0:
			if len(self.job.cpuBursts) > 1:
				self.moveToWaiting()
			else:
				self.moveToTerm()
	def reset(self):
		self.pause = False
		#self.moveReady = False
		#the way it is set up now I am manually turning this 
		#off when I add multple CPU's I may have to adjust this but 
		#for the test I will keep it as is 

	def __str__(self):
		return str(self.job.id)


#Will have to build a function for round robbin where the CPU
#can also return the job to the reayQueue