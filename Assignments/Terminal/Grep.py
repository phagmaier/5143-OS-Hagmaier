'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: Grep when called with no flags will display all lines that match the entered text that is supposed to be matched.
Like all my commands it takes waspiped to indicate if it was piped and if so it should acceopt not just text files but the output
of the previous function which will be a string or a list depending on the function. if it was piped we append it to the variable
files. the match variable is the entered input that is to be matched within the file/string/list. we loop through all args
to both error check to make sure it is an acceptable command and we then parse it if it's acceptable into the flag variable
or append it to the files vairable. Count is used as an error checker to make sure what is supposed to be matched comes 
before the file that is to be checked for a match. If a flag is given and it is -l it will just display the name of the 
file if it exists if not it will display every line containing the match. If it is to be redicreted indicated by the 
pipeOrRe variable the outputis appended to the redirect list and will be returned at the end of the function. We use
a for loop to go through every file given since more than one file can be given for grep and we see if any line 
contains a match using 'if match in file' and if it is we either print that line or append it to the redirect list 
the same goes for if it is was piped or redirected in which case the same process occurs on the list or string 
we error check by making sure the input is a file list, or string (only list or string if redirected/piped) and 
for each of these types we have a condition that checks if what is in files corresponds to these types and handle them
in their own way i.e if it's a file we have to open in count the number of lines and loop through each line checking for a match 
if it's a list we do the same but for each element in the lsit and for the string we check if the match is in the string in it's 
entirety. If i were to redo i would probably divide each of these conditions into their own functions but as of now 
eac condition is checked and then according to which type it is it performs the operation according to it's type. 
'''
import os
def grep(wasPiped=None, *args):
	import os
	pipOrRe = False
	files = []
	match = ''
	count = 0
	redirect = []
	flag = None
	for arg in args:
		if isinstance(arg, bool) == True:
			pipOrRe = arg
			count +=1
		elif os.path.isdir(arg):
			print('grep:' + arg + ': Is a directory')
		elif os.path.isfile(arg) == True:
			files.append(arg)
			count +=1
		elif arg[0] == '-':
			flag = arg
		elif isinstance(arg, str) == True and count <=1:
			match = arg
			count +=1
		elif wasPiped !=None:
			if isinstance(arg, str):
				files.append(arg)
			elif isinstance(arg, list):
				files.append(arg)
			else:
				print('Invalid comamnd')
				return
	if flag != None and flag != '-l':
		print('invalid flag')
		return
	for file in files:
		if isinstance(file, list) == True:
			for i in file:
				for l in i:
					if isinstance(l, list):
						for z in l:
							if match in z:
								if pipOrRe == False:
									if flag == None:
										print(file + ':' + ' ' + z)
									else:
										print(file)
								else:
									if flag == None:
										redirect.append(file + ':' + ' ' + str(z))
									else:
										redirect.append(file)
					else:
						if match in l:
							if pipOrRe == False:
								if flag == None:
									print(l)
								else:
									print(file)
							else:
								if flag == None:
									redirect.append(file + ':' + ' ' + str(l))
								else:
									redirect.append(file)
		elif os.path.isfile(file) == True:
			with open(file, 'r') as grepfile:
				numLines = len(grepfile.readlines())
			grepfile.close()
			with open(file, 'r') as grepfile:
				for i in range(numLines):
					line = grepfile.readline()
					if match in line:
						if pipOrRe == False:
							if flag == None:
								print(file + ':' + ' ' + line)
							else:
								print(file)
						else:
							if flag == None:
								redirect.append(line)
							else:
								redirect.append(file)
				grepfile.close()
		else:
			if match in file:
				if pipOrRe == False:
					print(file)
				else:
					redirect.append(file)
	if pipOrRe == False:
		return 
	else:
		return redirect
