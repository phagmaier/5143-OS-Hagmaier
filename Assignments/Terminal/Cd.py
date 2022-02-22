'''
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
def cd(wasPiped=None, *args):
	import os
	count = 0
	pipeOrRe = False
	arg = None
	directory = None
	for arg in args:
		count+=1
		if isinstance(arg, bool):
			pipeOrRe = arg
		else:
			directory = arg
	if count > 2:
		print('Error improper command')
		return 
	elif directory == None:
		return
	if directory == '~':
		directory = os.path.expanduser('~')
		directory = str(directory)
	try:
		os.chdir(directory)
	except:
		print('No directory: ' + directory)
		return
	if pipeOrRe == False:
		return
	else:
		return directory
