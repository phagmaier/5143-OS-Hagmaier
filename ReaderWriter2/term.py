'''
A very simple termQueue 
initilize with a empty list
we call add each time the cpu finishes processsing a instruction and then it appends those instruction to the termQueue
'''
class Term:
	def __init__(self):
		self.termQueue = []

	def add(self, instruction):
		for i in instruction:
			if type(i) == list:
				for x in i:
					self.termQueue.append(x)
			else:
				self.termQueue.append(i)
