'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
 Description:  Tail is similar to head the difference being it displays the last ten lines of the file. It is a function 
 that if '-n' is not passed as a flag then by default the last 10 lines of the 
 file will be read. if -n is passed as a flag then the number specified after will be the number displayed. 
 If either the default or the number enetered is larger then the number of lines then the entire file will be displayed.
 wasPiped and args are arguments as they are in all my functions. wasPiped indicated whether the function shoudl accepts strings and 
 or lists that came from other functions and args will contain if the output should be piped i.e returned as a list in this case. 
 PipeOrRe is the variable that stores if it is to be redirected files contains all the files passed and list and strings variables do 
 the same with input that was redirected. We loop through args with a for loop to determine what the input is and if the input is valid 
 if the correct flag is entered then number which defaults to 10 is chnaged to whatever is passed and if no number is passed an error message is
 displayed but it will not break the shell. linesIfPiped contains the piped or redirect output if pipeOrRe is anything other than False. 
 We use isinstance and os.path.isfile to check what the type of input is and then we deal with it accordingly. The only difference between 
 the types of inputs is for files we must open it and count the lines and for lists we just loop through each element in the list and we consider
 that a line (we display it as such as well). Because multiple files can be passed to head we loop through each file and then for each file 
 we have another loop which loops throguh the files lines up to the number entered or the deault number and we wither display it if it is not
 going to be piped or we append it to linesIfPiped in order for it to be passed to the next command. 
'''
import os
def tail(waspiped=None, *args):
	import os
	pipeOrRe = False
	files = []
	lists = []
	strings = []
	flag = None
	number = 10
	linesIfPiped = []
	for arg in args:
		if waspiped !=None:
			try:
				if isinstance(arg, list) == True:
					for i in arg:
						lists.append(i)
				else: 
					if isinstance(arg, str):
						strings.append(arg)
			except:
				pass
		if isinstance(arg, bool) == True:
			pipeOrRe= arg
		elif arg == '-n':
			flag = arg
		elif arg[0] == '-' and arg != '-n':
			print('invalid command')
			return
		try:
			if arg.isdigit() == True:
				number = int(arg)
		except:
			pass
		try:
			if os.path.isfile(arg) == True:
				files.append(arg)
		except:
			pass 
	if len(files) > 0:
		for i in files:
			with open(i, 'r') as tailfile:
				lines = tailfile.readlines()
				if number < len(lines):
					tailLines = lines[(0-number):]
				elif number > len(lines):
					tailLines = lines
				if pipeOrRe == False:
					for i in range(len(tailLines)):
						if pipeOrRe == False:
							print(f"{tailLines[i]}", end="")
							if tailLines[i][-1] != '\n':
								print('\n')
						else:
							linesIfPiped.append(tailLines)
					tailfile.close()

	if len(lists) > 0:
		if number > len(lists):
			number = int(len(lists))
			for i in range(number):
				if pipeOrRe == False:
					print(lists[i])
				else:
					linesIfPiped.append(lists[i])
		else:
			lists = lists[0-number:]
			for i in range(number):
				if pipeOrRe == False:
					print(lists[i])
				else:
					linesIfPiped.append(lists[i])

	if len(strings) > 0:
		for i in strings:
			if pipeOrRe == False:
				print(i)
		else:
			linesIfPiped.append(i)
	if pipeOrRe == False:
		return 
	else:
		return linesIfPiped
#tail(None, False, 'Readme.txt')
