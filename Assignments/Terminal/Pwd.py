'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: The PWD function/command tells the user what directory they are in. Like every function it takes
the params wasPiped and args. PWD should never be piped or at least I don't know how to deal with having input piped to it.
It can the current directory as a string if it is piped but it cannot handle being piped to. 
To eror correct we loop through all the args to make sure only the manditory pipeOrRe variable is the only thing that was passed in args
and if it's not we through an error. The actual function or act of getting the current directory is done through os.getcwd()
'''

def pwd(wasPiped = None, *args):
  if wasPiped !=None:
    print('Error dont know how to deal with this')
    return
	import os
	pipeOrRe = False
	x = 0
	for arg in args:
		x+=1
		if isinstance(arg, bool):
			pipeOrRe = arg
	if x > 1:
		print('Invalid command')
		return
	else:
		currentDir=os.getcwd()
	if pipeOrRe == False:
		print(currentDir)
		return currentDir
	else:
		return str(currentDir)
