'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: This command displays a file(s) or if it was piped it displays the contenets 
of whatever command was called before being piped. The actual cat function parses the args
and according to what was given it either opens the file and read all the lines or does the 
same with strings and or lists but only if it was piped. If it was piped it calls the helper function
piped which deals with the the string and lists 
'''



import os
'''
The piped function takes the piped input param which just means all the input 
given to cat that was not a file and meant to be read. It then checks if it was a string
or a list and prints it accordingly or if the other argument pipeOrRe is not False then
it will return the the piped input to the cat function so that it can return the list
of containing the contents of the lists and or strings along with any files it may have been
passed
'''
def piped(pipedInput, pipeOrRe):
	import os
	if isinstance(pipedInput,list):
		if pipeOrRe == False:
			for i in pipedInput:
				print(i)
			return
		else:
			return pipedInput
	elif isinstance(pipedInput, str):
		if pipeOrRe == False:
			print(pipedInput)
			return
		else:
			noFile= 'cat: ' + str(pipedInput) + ': No such file or directory\n'
			return noFile
	else:
		#don't know if the input is invalid if it will break it because
		#invalid files don't break cat so I will just give same 'invalid' statment as if that happend
		if pipeOrRe == False:
			print('cat: ' + str(pipedInput) + ': No such file or directory\n')
		else:
			return pipedInput

'''
The cat function like all the command function takes in a wasPiped argument 
along with args wasPiped indicated if it was piped or redirected and args 
will contain if it is going to be piped if any falgs and the data to be read
the not valud list contains any files that aren't able to be read since cat can take multiple
files and it doesn't shut down if one of those files doesn't exist it just displays
that the file doesn't exist we append that not valid input to said array.
lineNumbers is the total number of lines in each specific file that is passed we read
each file and pass in the line numbers to this list so that when we display the contents of 
the file we can use this list to determine the length of the for loop used to both read in the 
line and then display it
For pipe is the list that contains the contents of all files, list or strings that will be returned
if the pipeOrRe variable is anything but false (this is determined by the args and is passed first 
from the parse function and then again by the call function)
'''

def cat(wasPiped=None, *args):
	import os
	x = []
	notvalid = []
	pipeOrRe = False
	lineNumbers = []
	forPipe = []
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
		else:
			x.append(arg)
	for i in range(len(x)):
		try:
			with open(x[i], 'r') as catFile:
				numlines = len(catFile.readlines())
				lineNumbers.append(numlines)
			catFile.close()
		except:
			notvalid.append(x[i])
			lineNumbers.append(0)
	for i in range(len(x)):
		if x[i] in notvalid:
			if wasPiped != None:
				if pipeOrRe ==False:
					piped(x[i], pipeOrRe)
				else:
					forPipe.append(piped(x[i], pipeOrRe))
			else:
				if pipeOrRe == False:
					print('cat: ' + x[i] + ': No such file or directory\n')
				else:
					noFile= 'cat: ' + x[i] + ': No such file or directory\n'
					forPipe.append(noFile)
		else:
			with open(x[i], 'r') as catFile:
				for line in range(lineNumbers[i]):
					line = catFile.readline()
					if pipeOrRe == False:
						print(f'{line}', end="")
						if line[-1] != '\n':
							print('\n')
					else:
						forPipe.append(line)
				catFile.close()
	if pipeOrRe == False:
		return
	else:
		return forPipe



#cat(None, 'Readme.txt', 'aa.txt', 'bbcd.txt', 'hello')
