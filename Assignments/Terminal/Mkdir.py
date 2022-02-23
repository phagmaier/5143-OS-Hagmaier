'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: mkDir creates a new directory 
we loop through all the arguments in args and we make sure that only the new directory
and the pipeOrRe which has to be passed by parse is the only arguments given. We then have to make sure 
that the new directoory doesn't already exist in the directory where we are creating it so we check using os.path.isdir()
and if it's not we then use os.mkdir()
'''


def mkdir(wasPiped=None, *args):
	import os
	pipeRed=False
	newDir = None
	count = 0
	pipedDir = None
	for arg in args:
		count +=1
		if arg == True:
			pipeRed = False
		elif arg == None:
			pipeRed = False
		else:
			newDir = arg
	if count > 2:
		print('An error occured')
		return
	else:
		try:
			if os.path.isdir(newDir) == True:
				print('Cannot create directory ' + newDir + ': File already exists')
				return
		except:
			pass
		try:
			if pipeRed == False:
				os.mkdir(newDir)
			else:
				#don't even know if you can pipe the creation of a new directory
				pipedDir = os.mkdir(newDir)
		except:
			print('Error: something wrong with my function or the file already exists')
			return
		if pipeRed == False:
			return
		else:
			return pipeRed
#mkdir('Bannana')
#mkdir('Bannana')
