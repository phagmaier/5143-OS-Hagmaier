'''
Decrements the iobursts
job saves the job loaded. Busy indicates if a job is in the IO
send is a bollean that changes when a job needs to be sent to ready when finished.
move is the job to move. pause means an action has been taken in this clock tick.
'''

class IO:
	def __init__(self):
		self.job = None
		self.busy = False
		self.send = False
		self.move = None
		self.pause = False
	
	'''
	Recieves a job 
	'''
	def recieve(self, job):
		if job != None:
			self.job = job
			self.busy = True
	
	'''
	decrements IO bursts and sets proper boolean values so no other value can be loaded during this clock tick
	'''
	def moveToReady(self):
		self.job.inputBursts = self.job.inputBursts[1:]
		self.send = True
		self.move = [self.job]
		self.job = None
		self.busy = False
		self.pause = True
		return self.move
	
	'''
	decrements IO burst
	'''
	def run(self):
		self.job.inputBursts[0] -= 1
		if self.job.inputBursts[0] == 0:
			return self.moveToReady()

	'''
	resets for a new job to be loaded
	'''
	def reset(self):
		self.pause = False


	def __str__(self):
		#return str(self.job.id)
		return str(self.job.id)
