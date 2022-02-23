'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: Sort is a command that is supposed to sort files and if piped or redirected also strings and lists depending on what command was piped or redirected.
The reason i didn't just use listname.sort() is because it doesn't sort with respect to lowercase meaning lowercase doesn't come first. This is how it was sorted
on Ubuntu but I learned that not all systems sort like this which is why multiple sorts are called on the list called liens which contains the contents to be sorted. 
the two sorts i ran consecuitivley are lines = sorted(lines, key=str.istitle) and lines = sorted(lines, key=str.lower) which works pretty well but is not always perfect.
There is also a problem sorting when a tab is at the start of a line or if the quotes are in a line ect... On standard fies lists and strings where is is just rows
of characters it will work perfectly but this is not always the case with input to the function. Like all my functions it takes as arguments waspiped and args. Sort at
this time only sorts one file or redirected/piped input.
'''

def sort(wasPiped=None, *args):
	import os
	pipeOrRe = False
	lines = []
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe= arg
		try:
			if os.path.isfile(arg):
				with open(arg, 'r') as infile:
					lines = [line.rstrip() for line in infile]
					lines.sort()
		except:
			pass
		if wasPiped == True:
			if isinstance(arg, list):
				for i in arg:
						if isinstance(i, list):
							for x in i:
								x.strip('\t')
								lines.append(x)
							lines.sort()
						else:
							lines.append(i) 
			elif isinstance(arg, str):
				lines.append(arg)
				lines.sort()
	if len(lines) == 0:
		print('Error')
		return
	if pipeOrRe == False:
		lines = sorted(lines, key=str.istitle)
		lines = sorted(lines, key=str.lower)
		for i in lines:
			print(i)
	else:
		return lines
