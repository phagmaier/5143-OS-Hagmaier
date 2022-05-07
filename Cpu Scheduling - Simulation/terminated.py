class Terminated:
  def __init__(self):
	  self.termQueue = []
	  self.job = None

  def addTerm(self, job, count):
	  self.job = job
	  self.job.TurnAroundTime = count - self.job.arrival
	  self.termQueue.append(self.job)
	  self.display()

  def display(self):
    pass
    



