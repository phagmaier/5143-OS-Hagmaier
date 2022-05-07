class Job:
	def __init__(self, dataList):
		self.arrival = int(dataList[0])
		self.id = int(dataList[1])
		self.priority = int(dataList[2])
		self.priorityCopy = self.priority
		self.cpuBursts = [int(i) for i in dataList[3]]
		self.inputBursts = [int(i) for i in dataList[3]]
		self.CPUWaitTime = 0
		self.IOWaitTime = 0
		self.TurnAroundTime = 0 #time from New Queue to terminated can calculate in the main driver func
		self.cpuTime = 0 #total number of time needed in the cpu (redundant try to delete if not used)
		self.IoTime = 0 #total number of time needed in the IO
		self.jobLength = 0 #the total number of cpu bursts required (used for sjf)
		self.currentLength = 0 #the current length cpu time remaining in job (for srj)
		self.moved = False

		for i in self.cpuBursts:
			self.jobLength += i
			self.currentLength += i
			self.cpuTime +=i

		for i in self.inputBursts:
			self.IoTime += i
