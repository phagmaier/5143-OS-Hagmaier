'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Main Class:    Shell
 Date:          February 20, 2022
 Description:  History is a fairly simple command. it contains wasPiped and args like all the commands and this where 
 what is entered in after the commmand is entered into the terminal is parsed. We error check to make sure hisory is passed
 by itself and more things can only be passed after it if there is a pipe or redirect but this is taken care of in the parse function
 here we just make sure that in args nothing else is passed besides the boolean pipOrRe which indicated if it is to be piped which
 is determined by our parse function. Because we save the history file in the home directory we must cd there and cd back after all
 the lines of history are read into a list and either displayed or returned as output for the next function 
'''

import os
def history(wasPiped=None, *args):
	import os
	pipeOrRe = False
	current_dir = os.getcwd()
	current_dir = str(current_dir)
	home = os.path.expanduser('~')
	home = str(home)
	os.chdir(home)
	lines = []
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
	if current_dir == home:
		with open('history.txt', 'r') as history:
			if pipeOrRe == False:
				for line in history:
					print(line[2:])
				history.close()
				return
			else:
				for line in history:
					lines.append(line)
				history.close()
				return lines
	else:
		try:
			os.chdir(home)
		except:
			print('An unexpcted error occured')
			return
		with open('history.txt', 'r') as history:
			if pipeOrRe == False:
				for line in history:
					print(line[2:])
				history.close()
				os.chdir(current_dir)
				return
			else:
				for line in history:
					lines.append(line)
				os.chdir(current_dir)
				return lines
