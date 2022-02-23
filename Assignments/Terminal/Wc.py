'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: This command displays the word count line count and the size (if no flags are passed) It also must be noted that this command is one of the ugliest
and worst written functions ever written. This must be made explicit and up top. The function does work and it does work if it is piped or redirected the problem is its 
innefeciency its length and ugliness. In retrospect this function would be better suited if broken into several commands. The reason for it's length is that
each particular flag had to be accounted for and the order in which is was displayed differed depending on which order the flags were enetered. For the most part
This function reads in a file or if piped a list and or string which is opened or scanned through and the line count is determined by taking the length of the 
readlines() function that is built into with python or if it is a list the new line character is checked for. The reason for it's length is each flag and it's 
possible combinations is checked for each type of possible input those being string list or file. The fllags dictate what is printed i.e just the word count
just word count and number lines just the word count and size ect... with all posible combination of these having to be taken into account for each particular
input type. 
'''

def wc(wasPiped=None, *args):
	import os
	pipeOrRe= False
	flag = None
	files =[]
	results = []
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
		elif arg[0] == '-':
			flag = arg
		else:
			if wasPiped == None:
				if os.path.isfile(arg) == True:
					files.append(arg)
				else:
					print('wc: '+ arg +': No such file or directory')
			else:
				files.append(arg)
	for file in files:
		if wasPiped == None:
			with open(file, 'r') as wcfile:
				numLines = len(wcfile.readlines())
				size = os.path.getsize(file) 
			wcfile.close()
			with open(file, 'r') as wcfile:
				wholeFile = wcfile.read()
				words = wholeFile.split()
			wcfile.close()
		
			if flag == None:
				if pipeOrRe == False:
					print(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(size) + ' ' + file)
				else:
					results.append(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(size) + ' ' + file)
			elif flag == '-w':
				if pipeOrRe == False:
					print(str(len(words)) + ' ' + file)
				else:
					results.append(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(size) + ' ' + file)
			elif flag == '-m':
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(count) + ' ' + file)
				else:
					results.append(str(count) + ' ' + file)
			elif flag == '-l':
				if pipeOrRe == False:
					print(str(numLines -1) + ' ' + file)
				else:
					results.append(str(numLines -1) + ' ' + file)
			elif flag == '-wm':
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(len(words)) + ' ' + str(count) + ' ' + file)
				else:
					results.append(str(len(words)) + ' ' + str(count) + ' ' + file)
			elif flag == '-wl':
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(len(words)) + ' ' + str(numLines -1) + ' ' + file)
				else:
					results.append(str(len(words)) + ' ' + str(numLines -1) + ' ' + file)
			elif flag == '-mw':
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(count) + ' ' + str(len(words)) + ' ' + file)
				else:
					results.append(str(count) + ' ' + str(len(words)) + ' ' + file)
			elif flag == '-ml':
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(count) + ' ' + str(numLines -1) + ' ' + file)
				else:
					results.append(str(count) + ' ' + str(numLines -1) + ' ' + file)
			elif flag == '-lm':
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(numLines -1) + ' ' + str(count) + ' ' + file)
				else:
					results.append(str(numLines -1) + ' ' + str(count) + ' ' + file)
			elif flag == '-lw':
				if pipeOrRe == False:
					print(str(numLines -1) + ' ' + str(len(words)) + ' ' + file)
				else:
					results.append(str(numLines -1) + ' ' + str(len(words)) + ' ' + file)
			elif len(flag) == 4 and '-' in flag and 'l' in flag and 'w' in flag and 'm' in flag:
				count = 0
				for i in wholeFile:
					count += 1
				if pipeOrRe == False:
					print(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(count) + ' ' + file)
				else:
					results.append(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(count) + ' ' + file)
			else:
				print('wc: invalid option -- ' + flag)
				return

		else:
			if os.path.isfile(file) == True:
				with open(file, 'r') as wcfile:
					numLines = len(wcfile.readlines())
					size = os.path.getsize(file) 
					wcfile.close()
				with open(file, 'r') as wcfile:
					wholeFile = wcfile.read()
					words = wholeFile.split()
					wcfile.close()
				if flag == None:
					if pipeOrRe == False:
						print(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(size) + ' ' + file)
					else:
						results.append(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(size) + ' ' + file)
				elif flag == '-w':
					if pipeOrRe == False:
						print(str(len(words)) + ' ' + file)
					else:
						results.append(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(size) + ' ' + file)
				elif flag == '-m':
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(count) + ' ' + file)
					else:
						results.append(str(count) + ' ' + file)
				elif flag == '-l':
					if pipeOrRe == False:
						print(str(numLines -1) + ' ' + file)
					else:
						results.append(str(numLines -1) + ' ' + file)
				elif flag == '-wm':
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(len(words)) + ' ' + str(count) + ' ' + file)
					else:
						results.append(str(len(words)) + ' ' + str(count) + ' ' + file)
				elif flag == '-wl':
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(len(words)) + ' ' + str(numLines -1) + ' ' + file)
					else:
						results.append(str(len(words)) + ' ' + str(numLines -1) + ' ' + file)
				elif flag == '-mw':
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(count) + ' ' + str(len(words)) + ' ' + file)
					else:
						results.append(str(count) + ' ' + str(len(words)) + ' ' + file)
				elif flag == '-ml':
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(count) + ' ' + str(numLines -1) + ' ' + file)
					else:
						results.append(str(count) + ' ' + str(numLines -1) + ' ' + file)
				elif flag == '-lm':
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(numLines -1) + ' ' + str(count) + ' ' + file)
					else:
						results.append(str(numLines -1) + ' ' + str(count) + ' ' + file)
				elif flag == '-lw':
					if pipeOrRe == False:
						print(str(numLines -1) + ' ' + str(len(words)) + ' ' + file)
					else:
						results.append(str(numLines -1) + ' ' + str(len(words)) + ' ' + file)
				elif len(flag) == 4 and '-' in flag and 'l' in flag and 'w' in flag and 'm' in flag:
					count = 0
					for i in wholeFile:
						count += 1
					if pipeOrRe == False:
						print(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(count) + ' ' + file)
					else:
						results.append(str(numLines - 1) + ' ' + str(len(words)) + ' ' + str(count) + ' ' + file)
				else:
					print('wc: invalid option -- ' + flag)
					return

			elif isinstance(file, list) == True or isinstance(file, str) == True:
				if isinstance(file, list) == True:
					numLines = 1
					words = 0
					count =0
					try:
						size = len(file.encode('utf-8'))
					except:
						size = 0
					for i in file:
						if isinstance(i, list) == True:
							for x in i:
								for g in i:
									if g == ' ':
										words +=1
										count+=1
									elif g == '\n':
										numLines +=1
										count+=1
									else:
										count+=1
						#addiional for loop
						else:
							for x in i:
								if x == ' ':
									words+=1
									count+=1
								elif g == '\n':
									numLines +=1
									count+=1
				elif isinstance(file, str) == True:
					numLines = 1
					words = 1
					size = 0
					count = 0
					for i in range(len(file)):
						if file[i] == '\n':
							numLines +=1
							count+=1
						elif file[i] == ' ':
							words +=1
							count +=1
						try:
							size=len(file.encode('utf-8'))
						except:
							size = 0
						else:
							count +=1
				else:
					print('error filetype not supported')
					return

				if flag == None:
					if pipeOrRe == False:
						print(str(numLines) + ' ' + str(words) + ' ' + str(size) + ' ' + str(file))
					else:
						results.append(str(numLines) + ' ' + str(words) + ' ' + str(size) + ' ' + str(file))
				elif flag == '-w':
					if pipeOrRe == False:
						print(str(words) + ' ' + file)
					else:
						results.append(str(numLines) + ' ' + str(words) + ' ' + str(size) + ' ' + str(file))
				elif flag == '-m':
					if pipeOrRe == False:
						print(str(count) + ' ' + str(file))
					else:
						results.append(str(count) + ' ' + str(file))
				elif flag == '-l':
					if pipeOrRe == False:
						print(str(numLines) + ' ' + str(file))
					else:
						results.append(str(numLines) + ' ' + str(file))
				elif flag == '-wm':
					if pipeOrRe == False:
						print(str(words) + ' ' + str(count) + ' ' + str(file))
					else:
						results.append(str(words) + ' ' + str(count) + ' ' + str(file))
				elif flag == '-wl':
					if pipeOrRe == False:
						print(str(words) + ' ' + str(numLines) + ' ' + str(file))
					else:
						results.append(str(words) + ' ' + str(numLines) + ' ' + str(file))
				elif flag == '-mw':
					if pipeOrRe == False:
						print(str(count) + ' ' + str(words) + ' ' + str(file))
					else:
						results.append(str(count) + ' ' + str(words) + ' ' + str(file))
				elif flag == '-ml':
					if pipeOrRe == False:
						print(str(count) + ' ' + str(numLines) + ' ' + str(file))
					else:
						results.append(str(count) + ' ' + str(numLines) + ' ' + str(file))
				elif flag == '-lm':
					if pipeOrRe == False:
						print(str(numLines) + ' ' + str(count) + ' ' + str(file))
					else:
						results.append(str(numLines) + ' ' + str(count) + ' ' + str(file))
				elif flag == '-lw':
					if pipeOrRe == False:
						print(str(numLines) + ' ' + str(words) + ' ' + file)
					else:
						results.append(str(numLines) + ' ' + str(words) + ' ' + file)
				elif len(flag) == 4 and '-' in flag and 'l' in flag and 'w' in flag and 'm' in flag:
					if pipeOrRe == False:
						print(str(numLines) + ' ' + str(words) + ' ' + str(count) + ' ' + file)
					else:
						results.append(str(numLines) + ' ' + str(len(words)) + ' ' + str(count) + ' ' + str(file))
				else:
					print('wc: invalid option -- ' + flag)
					return


	if pipeOrRe == False:
		return
	else:
		return results
