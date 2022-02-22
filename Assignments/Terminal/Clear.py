'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: the clear command clears the console. we do this through os.system('clear) the only other we do is check to make sure no 
additional arguments were passed into args besides the obligitory boolean pipeOrRe which indicated if it should be piped or not
which to be honest I'm not sure if it's possible to pipe it so i don't allow it it will just return the screen regarless. 
'''

import os
def clear(waspiped=False, *args):
	import os
	pipeOrRe = False
	count = 0
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
		count+=1
	if count > 1:
		print('Invalid command')
		return
	else:
		os.system('clear')
		return 
