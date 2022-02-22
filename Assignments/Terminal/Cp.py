''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: This command changes the directory. Like all my commands/functions
it takes it wasPiped and args. arg will contain the directory we are going to cd into
along with if it should be pipedOrRedirected although in a  real terminal
i'm unsure if you can pipe into cd and or pipeOrRedirect cd but i allowd it and
for pipe or re i just pass it the directory. The count variable makes sure nothing more than 
the directory is passed to args and the obligitory wasPiped boolean value. other than that
the function uses os.chdir to change the path and it automatically works for .. and . 
and for ~ we use os.path.expandesure in order to indicate that means take me to the home directory. 
we use try in order to make sure that if the directory is not a valid dir we will only get an error
message and our program will not crash  
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
