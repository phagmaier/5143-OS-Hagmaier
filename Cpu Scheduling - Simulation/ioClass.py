class IO:
	def __init__(self):
		self.job = None
		self.busy = False
		self.send = False
		self.move = None
		self.pause = False

	def recieve(self, job):
		if job != None:
			self.job = job
			self.busy = True

	def moveToReady(self):
		self.job.inputBursts = self.job.inputBursts[1:]
		self.send = True
		self.move = [self.job]
		self.job = None
		self.busy = False
		self.pause = True
		return self.move

	def run(self):
		self.job.inputBursts[0] -= 1
		if self.job.inputBursts[0] == 0:
			return self.moveToReady()


	def reset(self):
		self.pause = False


	def __str__(self):
		#return str(self.job.id)
		return str(self.job.id)