'''
This function is responsable for decrementing CPU time for a specific job.

In case of round robin we initialize with a time slice but timeslice will only be utilized by RR algorithm.
We also pass it an algo such as sjf rr ect...
moving dictates if we are moving out of the cpu. term is a boolean dictating whether we should send to termqueue or not. pause means 
cpu has taken an action during a clock tick and cannot take another. moveReady is used in round robin and dictates whether or not job should be sent
back to the readyqueue. current time comes from job and is the amount of cpu time that current job requires
'''
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
		
	'''
	function to pass in a job to the CPU
	'''
	def recieve(self, job):
		if job != None:
			self.job = job
			self.busy = True
	'''
	when a job is finished with the cpu this function takes the job and sends it to the cpu
	'''
	def moveToTerm(self):
		self.term = True
		self.move = self.job
		self.job = None
		self.busy = False
		self.pause = True #might not need this but idk
		return self.move
	
	'''
	set job to none and we remove that jobs cpuburst index since it is at zero 
	we also set pause to true since we are moving and this cpus action has been taken in this clock tick.
	THis function moves this job to the waitijng queue
	'''
	def moveToWaiting(self):
		self.job.cpuBursts = self.job.cpuBursts[1:]
		self.moving = True
		self.move = self.job
		self.job = None
		self.busy = False
		self.pause = True
		return self.move

	'''
	Same as the function above only it doesn't remove the cpuburst index because if this is called it means the job has been kicked 
	off due to round robin and is being sent back to the waiting queue
	'''
	def moveToReady(self):
		self.moving = True
		self.move = self.job
		self.job = None
		self.busy = False
		self.pause = True
		self.moveReady = True
		return self.move
	
	'''
	depending on what algorithm is run this run fucntion calls that particlar runFunction
	'''
	def run(self):
		self.algos = ['pb', 'fcfs', 'sjf', 'srj']
		if self.algo == 'rr':
			self.rrRun()
		elif self.algo in self.algos:
			self.regularRun()
		else:
			print('ERROR: I do not recognize that algorithm!!')
			return
	'''
	decrement cpuBurst time and then we check if it is zero in which case we indicate it needs to be moved to
	the waiting queue or if it needs to be moveed back to ready queue
	'''
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
	'''
	For non prioirty runs we don't have to check if we need to move the instruction back to the ready queue 
	so we only check if the job is finished with the cpu
	'''
	def regularRun(self):
		self.job.cpuBursts[0] -= 1
		self.job.currentLength -= 1
		if self.job.cpuBursts[0] == 0:
			if len(self.job.cpuBursts) > 1:
				self.moveToWaiting()
			else:
				self.moveToTerm()
	'''
	Resets the cpu for the next job
	'''
	def reset(self):
		self.pause = False
		#self.moveReady = False
		#the way it is set up now I am manually turning this 
		#off when I add multple CPU's I may have to adjust this but 
		#for the test I will keep it as is 

	def __str__(self):
		return str(self.job.id)
