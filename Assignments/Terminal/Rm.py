'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: The rm command can remove files without a flag and can remove directories with the -r flag. Like most of the commands it can 
do this on multiple files and in this case multiple directories. Because of this all inputted files and directories are with respect to their type
appended to a list either deleteFile or deleteDir after being checked to make sure they exist. this check is done by looping through all the args and performing
a os.isdir() and isfile.() if it is not a flag or bool. To be honest I wasn't sure how to handle it being piped or if info was piped to it but It should work 
if it is piped a string with the name of the file in the directory or the complete dile/dir path. Once everything is parsed and in the appropriate 
list a for loop is called and each file is deleted along with each dir. If the dir has more than three files in it or the list has more than three dirs in it 
the user will be prompted for input to see if they are sure they want to delete the files/dir
'''

import os
import shutil
def rm(wasPiped=None, *args):
	pipeOrRe = False
	deleteDir = []
	deleteFiles = []
	flag = 'None'
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
		elif arg[0] == '-':
			flag = arg
			if flag != '-r' and flag != '-f' and flag != '-rf' and flag != '-fr':
				print('Invalid flag: ' + flag)
				return 
		elif os.path.isdir(arg):
			deleteDir.append(arg)
		elif os.path.isfile(arg):
			deleteFiles.append(arg)
		else:
			print('invalid folder or directory')
			return 
	if 'r' in flag: 
		if len(deleteDir) > 0:
			if 'f' not in flag:
				usr =input('You are about to delete a directory. Press Y if you want to continue: ')
				if usr != 'y' and usr != 'Y':
					return
				else:
					for i in deleteDir:
						try:
							shutil.rmtree(i)
						except:
							pass
			else:
				for i in deleteDir:
					try:
						shutil.rmtree(i)
					except:
						print('An unkown error occured could not delete: ' + i)
		if len(deleteFiles) > 0:
			if deleteFiles >= 3 and len(deleteDir) == 0:
				if 'f' not in flag:
					usr =input('You are about multiple files. Press Y if you want to continue: ')
					if usr != 'y' and usr != 'Y':
						return
					else:
						for i in deleteFiles:
							try:
								os.remove(i)
							except:
								print('An unkown error occured could not delete: ' + i)
				else:
					for i in deleteFiles:
							try:
								os.remove(i)
							except:
								print('An unkown error occured could not delete: ' + i)

	else:
		if len(deleteDir) > 0:
			print('cannot delete directories')
		if len(deleteFiles) > 0 and 'f' not in flag:
			if len(deleteFiles) >= 3:
				usr = input('You are about multiple files. Press Y if you want to continue: ')
				if usr != 'y' and usr != 'Y':
					return
				else:
					try: 
						for i in deleteFiles:
							os.remove(i)
					except:
						print('An unkown error occured could not delete: ' + i)
			else:
				try: 
					for i in deleteFiles:
						os.remove(i)
				except:
					print('An unkown error occured could not delete: ' + i)
		else:
			try: 
				for i in deleteFiles:
					os.remove(i)
			except:
				print('An unkown error occured could not delete: ' + i)

	return
