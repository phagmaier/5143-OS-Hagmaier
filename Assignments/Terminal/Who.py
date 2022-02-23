'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: Who is a command that displays who is currently logged in. There is not much to say about this command. It parses and error 
checks the way all previous functions have. The actual functionality of the program is accomplished by os.getlogin() and os.getuid()
which will display everything the who command displays besides the original time of being logged onto. I display the current time so it at least
looks like it it shows the right thing but I could not figure out how to get login time and Dr. Griffin was lineint on this command. The current date and time is 
recieved through date.today() 
'''


import os
from datetime import datetime
from datetime import date 
def who(wasPiped=None, *args):
	pipeorRed = False
	count=0
	for arg in args:
		if isinstance(arg, bool):
			pipeorRed == arg
		else:
			print('Improper command cannot take flags or input')
			return
	if count> 1:
		print('Improper command cannot take flags or input')
		return

	try:
		userName = os.getlogin()
		userId = os.getuid()
	
	except:
		print('an unkown error occured could not retrive information')
		return
	if pipeorRed == False:
		print(userName + ' ' + ':' + str(userId) + ' ' + str(date.today()) + ' :' + str(userId))
		return
	else:
		return userName + ' ' + ':' + str(userId) + ' ' + str(date.today()) + ' :' + str(userId)
