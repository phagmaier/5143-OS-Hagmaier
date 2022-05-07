import json
from jobs import Job

jobs = []

f = open('datafile.json')

file = json.load(f)

for i in file['jobs']:
	jobs.append(i)

values = []

for i in jobs[0]:
	values.append(i)

print(values)


jobzz = []

for i in values:
	jobzz.append(jobs[0][i])
print(jobzz)

def createJobs():
	for i in jobs:
		for x in values:
			job = [jobs[i][x]]




#print(values)

#print(job)

#print(job[0])

#from here you would say like 
#job[0] = Arival time 
#job[1] = id
#3 = priority 
#4 = cpu bursts
#5 = ioBursts