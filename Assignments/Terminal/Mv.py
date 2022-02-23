'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: The mv function can do several things. It can either move a file from one directory to another or it can rename a file if 
instead of a direcotry we pass it a name that is not a directory name. Because in the real mv command you can move several files at a time
we keep all the files passed in arguments and if rename isn't == '' the last file in arguments will be the destination to which the files will be moved
We do not support mass renanimg so if rename != '' and there are more than one files in arguments we will print an error message. We use os.rename()
to rename a file and shutil.move to move a file 
'''


import os
import shutil
def mv(waspiped=None, *args):
	import os
	import shutil
	redirect= []
	arguments=[]
	rename = ''
	pipeOrRe = False
	for arg in args:
		if isinstance(arg,bool):
			pipeOrRe=arg
		elif os.path.isfile(arg) == True or os.path.isdir(arg) == True:
				arguments.append(arg)
				rename = ''
		else:
			rename = arg
	if len(arguments) > 1 and rename != '':
		print('Error can\'t support mass renaming of files')
		return
	elif len(arguments) == 1 and rename !='':
		if pipeOrRe == False:
			shutil.move(arguments[0], rename)
		else:
			return shutil.move(arguments[0], rename)
	elif len(arguments) == 1 and rename =='':
		print('No such file or directory')
		return
	else:
		for i in range(len(arguments) -1):
			try:
				if pipeOrRe == False:
					shutil.move(arguments[i], arguments[-1])
				else:
					redirect.append(shutil.move(arguments[i], arguments[-1]))
			except:
				print('An unkown error occured')
				return 
		if pipeOrRe == False:
			return
		else:
			return redirect


#mv(None, 'triangle.txt','square.txt')
