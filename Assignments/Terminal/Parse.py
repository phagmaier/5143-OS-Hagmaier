'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: The parse command is called from our main function and this is what determines what the function is and what will be passed to that function.
We first make sure that the length of what was passed is greater than one and then we search to see if a pipe or redirect is in the function
If it is we put the contents of the command into a sperate list where everyting before the pipe or redirect is passed recursivley into the function
but the the pipeOrRe condition being switched to True so we know to return the output and not display it 
we take the first item in the list and pass it to the call function as the command to be called and everything else is passed as part of the args
if it was piped we then take the output and put it back into the original command with everything after the pipe or redirect and the function is once 
again passed back to the call command where the same process will occur again if there is a pipe or redirect. It should be noted that redirect is considered a function
and we do actually call that as a command but we change it from >> and or > to redirect or doubleRe so that it isn't seen as a pipe or redirect 
'''

from callCommand import*
#need to add a argument for was piped
def parse(x, wasPiped=None, pipeOrRedirect=False):
	if len(x) == 0:
		return
	else:
		if '|' not in x and '>' not in x and '>>' not in x:
			y = []
			y = x[1:]
			command = x[0]
			return call(command, wasPiped, pipeOrRedirect, y)
		else:
			z = []
			#y = []
			count = 0
			for i in x:
				if i == '|' or i == '>' or i == '>>':
					pipeOrRedirect = i
					break
				else:
					count +=1
			#condition for pipeing
			if pipeOrRedirect != '>' and pipeOrRedirect!= '>>':
				z = x[:count]
				file = parse(z, wasPiped, pipeOrRedirect=True)
				x.insert(count+2,file)
				x = x[count+1:]
				#print(x)
				parse(x, True, pipeOrRedirect)
				#func = x[count+1]
				#call(func, flag, file, pipeOrRedirect, current_dir)
			else:
				z = x[:count]
				file = parse(z, wasPiped, pipeOrRedirect=True)
				x.insert(count+2, file)
				x = x[count+1:]
				if pipeOrRedirect == '>':
					redirect = 'redirect'
					x.insert(0, redirect)
				else:
					redirect = 'doubleRe'
					x.insert(0, redirect)
				x.insert(count+1,file) 
				parse(x, True, pipeOrRedirect)
