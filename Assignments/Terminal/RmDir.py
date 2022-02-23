'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: RMdir functions in a similar but simpler way to rm. The only difference is that only a directory can be deleted.
We check the input to make sure it is a directory and then that directory is subsequently deleted using shutil.rmtree()
multiple dirs can not be deleted with one command at this time. May update later since all it requires is a for loop and to change the directory
variable to a list 
'''

import os
import shutil
def rmdir(wasPiped=None, *args):
	import os
	import shutil
	pipeOrRe = False
	directory = None
	count = 0
	for arg in args:
		count+=1
		if isinstance(arg, bool):
			pipeOrRe= arg
		else:
			try:
				if os.path.isdir(arg) == True:
					directory = arg
			except:
				pass

	if directory == None or count > 2:
		print('Invalid comman')
		return 
	else:
		try:
			shutil.rmtree(directory)
		except:
			print('An unkown error occured could not remove file')
			return 
	return 
