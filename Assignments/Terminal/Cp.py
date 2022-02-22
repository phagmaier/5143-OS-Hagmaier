'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: This is the cp command which will not only copy files but will change the name if no directory is
given for it to change in to. With all my commands it takes wasPiped and args. We parse the args to check for 
if it should be piped (this is one of those cases where I don't know what to do if it is piped if it is piped
I return the file not sure how this works in a real piped cp command) 
As with the real cp command we can rename in mass so we put everything that is to be copied in a list named copy
(we do not support mass renaming but it won't crash the program rather it will through up an error message)
we know it is to be renamed and not copied if what is passed into args is both not a file and not a directory
if both copyto and renmae variable == ''. shutil.copy is used to copy os.rename is used to rename. 
'''

import os
import shutil
def cp(wasPiped=None, *args):
	pipOrRe = False
	import os
	import shutil
	copy = []
	rename = ''
	copyTo = ''
	gettingPiped =[]
	for arg in args:
		if isinstance(arg, bool):
			pipOrRe = arg
		elif os.path.isdir(arg) == True:
			copyTo = arg
		elif os.path.isfile(arg) == True:
			copy.append(arg)
			rename = ''
			copyTo = ''
		else:
			rename = arg
	if len(copy) == 1 and rename != '':
		try:
			if pipOrRe == False:
				#shulti.move(copy[0], rename)
				os.rename(copy[0], rename)
			#else:
				#gettingPiped.append(shulti.move(copy[0], rename))
		except:
			print('An unkown error occured. Could not copy file')
			return
	elif len(copy) >= 1 and rename != '':
		print('Error can\'t support renaming multiple files')
		return
	elif copyTo != None and len(copy) > 0 and copyTo != '':
		for i in range(len(copy)):
			try:
				if pipOrRe == False:
					shutil.copy(copy[i], copyTo)
				else:
					gettingPiped.append(shutil.copy(copy[i], copyTo))
			except:
				print('An error occurred was not able to copy')
				return 
	else:
		print('Invalid command')
		return 
	if pipOrRe == False:
		return 
	else:
		return gettingPiped
