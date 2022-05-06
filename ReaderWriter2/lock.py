"""
A simple lock that checks if the priority instruction number that is passed into unlock is the same in 
as the self.num variable this ensures that we are only running the proper shared memory instructions

inc increments the number and occurs after we have terminated a priority instruction

unlock releases the lock and allows prioirty instructions to be ran
set lock is redundant and incriments the key (lock number) to the next prioirty instruction value that needs to be run
"""
class Lock:
	def __init__(self):
		self.num = 0

	def inc(self):
		self.num += 1

	def unlock(self, num):
		if num == self.num:
			return True
		else:
			False
	def setLock(self):
		self.num += 1
