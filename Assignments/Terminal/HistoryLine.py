'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Main Class:    Shell
 Date:          February 20, 2022
 Description:  HistoryLine is the !x command. THis is mostly handled inside the main function but we do have a function for it just in case 
 the output needs to be redirected or piped. It is similar to the history command in that we need to cd into the home directory and then
 cd back into the directory we were at previously the only difference is we read the lines into a list and we then select the corresponding
 line that matches the number enetered after the exclimation point. We must also take the number and not the exclimation point so we take everything after the
 exclimation point and of course error check to make sure it is both a number and a line that exists within history i.e if we only have 100 lines line 1000 cannot
 be entered and if it is an error is thrown but it will not crash the program. 
'''
def historyLine(wasPiped=None, *args):
	import os
	pipeOrRe = False
	number = None
	number = 0
	for arg in args:
		count +=1
		if isnstance(arg, bool):
			pipeOrRe = arg
		else:
			number = arg
			try:
				number = int(number)
			except:
				print('Invalid Command')
				return
	if number == None:
		print('Invalid command')
		return
	elif count > 2:
		print('Invalid command')
		return
	elif count < 2:
		print('Invalid command')
		return
	else:
		number = number -1
		current = os.getcwd()
		current = str(current)
		home = os.path.expanduser('~')
		home = str(home)
		if current != home:
			os.chdir(home)
			with open('history.txt', 'r') as history:
				length = history.readlines()
				length = len(length)
				history.close()
				if num > length or num < 0:
					print('Command does not exist')
					os.chdir(current)
					return
				else:
					with open('history.txt', 'r') as history:
						for i in range(number+1):
							line = history.readline()
					os.chdir(current)
					return line[2:]
		else:
			with open('history.txt', 'r') as history:
				for i in range(number+1):
					line = history.readline()
					return line[2:]
