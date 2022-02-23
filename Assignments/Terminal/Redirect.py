'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: This is the redirect command > which will overwirte a file rather than append to it. 
Like all my commands it takes a waspiped argument to indicated if it was piped and should
acccept strings and or lists which it always should but a new user may. may try to use > filename.txt without realizing
you first must have a command given first. If wasPiped == None an error is given but it will not crash. If the file name given doesn't
exist we create the file if not we overwrite to the existing file. We then check if the input is a string or a list and if it is a list we write
to the file with a for loop printing each item in the list and if it is a string we write the entire string to the file. if the output is
supposed to be piped as indicated by the pipeOrRe argument that is allway passed as a boolean to args we either write directly to the file or 
we return the output of the file so that it can be used for the next command. 
'''

import os
def redirect(wasPiped=None, *args):
	import os
	pipeOrRe = False
	inputt = None
	file = None
	if wasPiped == None:
		print('An unexcepted error occured')
		return 
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
		elif isinstance(arg, list):
			inputt = arg
		elif os.path.isfile(arg):
			file = arg
		elif isinstance(arg, str)==True and inputt == None:
			inputt = arg
		elif inputt != None and isinstance(arg, str) == True and file == None:
			file = arg
		else:
			print('Invalid command')
			return 
	if file == None or inputt == None:
		print('invalid command')
		return 
	else:
		with open(file, 'w') as outfile:
			if isinstance(inputt, list):
				for i in inputt:
					outfile.write(str(i) + '\n')
				outfile.close()
			else:
				outfile.write(str(inputt))
	if pipeOrRe == False:
		return
	else:
		return inputt
