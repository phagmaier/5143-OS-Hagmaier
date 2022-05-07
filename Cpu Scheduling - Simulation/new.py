'''
When a job is loaded into our similation it is first moved to this queue
'''
class New:
	def __init__(self):
		self.queue = []
	'''
	add to new queue takes in a job and appends to queue
	'''
	def addNew(self, job):
		self.job = job
		self.queue.append(self.job)

