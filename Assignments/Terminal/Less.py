'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: In Less the contents of a file (or if piped a list or string) is displayed to screen (if it is to be redirected
the entire contents of the file are passed as output as a list). You also need to be able to scroll through the output if the 
contents is larger than the console size which is done through gethch in order to read in user input (only q u down spacebar and control c everything
else does nothing) 
getch is utilized inside the getNext() function which is the same as in our main function except is doesn't display what is inputted and only the keys 
mentioned above do anything to the display. The defaultLess function is what is originally called and is the function where we determine the size of the console
so we display only what can fit on the console) throughout all these functions we havse several paramiters:
filename: is the input given (typically a file unless it was piped)
ConsoleLines: The size of the number of lines the console can display which will act as both a limit of whether we can scroll down or not and as a limit of when
we stop displaying what was read in from the file. 
PipeOrRe is a variable in all my functions that determines if the output should be displayed or if it should be returned (it is always a boolean True or False)
start defaults at 0 and it indicates what the first line being displayed is so that we know what to print to the screen. 
LastLine variable is the size of the file so we know if we can continue scrolling down or not. 
count is used to determine if we can scroll up and is used to prevent errors so we can't go up when the first line of the file is already being displayed
if the file is smaler then the number of console lines then console lines becomes the number of lines in the file 
Every time up and down is pressed the screen is flushed and a new output is displayed depenet if on the up down or spacebar was pressed
if the down arrow is pressed the start gets increased by one and so does the last line. The count will also get decrimented so we know we can now 
press the up arrow
I found it easiest to have each function call each other so after the output is displayed whether it be from the function down less which is called from the down arrow
or space bar and which moves the output down one line it then returns to the getNext function where the user can again decide if they want to view more of the file using
up down or spacebar. And each time getNext is called it will always either call itself if an invalid character is pressed or it will call the up or down functions
where those functions as mentioned above determine if they can move up or down through the file but regarless they will always call back to next
The only way to exit this command is by enteing q or control c
of course the function is also technically quit if it is being piped in which case what would have been the ouput gets passed as a list where each line is a string
inside the list and it is retunred to the next command 

'''
import os
from getch import Getch
getch = Getch()

def getNext(filename, consuleLines, pipeOrRe, start = 0, last_line= 0, count=0):

  char = getch()                      # read a character (but don't print)
  # ctrl-c
  if char == '\x03':
    os.system('cls' if os.name == 'nt' else 'clear')
    raise SystemExit()
  elif char == 'q':
    os.system('cls' if os.name == 'nt' else 'clear')
    return
    #raise SystemExit()
  elif char == ' ':
  	downLess(filename, consuleLines, pipeOrRe, start, last_line, count)

  elif char in '\x1b':                # arrow key pressed
      null = getch()                  # waste a character
      direction = getch()             # grab the direction
      
      if direction in 'A':            # up arrow pressed
         return upLess(filename, consuleLines, pipeOrRe, start, last_line, count)
          
      if direction in 'B':            # down arrow pressed
        return downLess(filename, consuleLines, pipeOrRe, start, last_line, count)
  else:
    return



def defaultLess(filename, pipeOrRe):
  count =0
  size = os.get_terminal_size()
  consoleLines = size.lines
  os.system('cls' if os.name == 'nt' else 'clear')
  if isinstance(filename, list):
  	lines = []
  	lines = filename
  	last_line = len(filename)
  	last_line = int(last_line)
  	#need to adda  check to make sure that number of lines is greater than console range
  	#if it's not then you kist print all the contents of the file
  	#need to do this if it's a file as well
  	if last_line < int(consoleLines):
  		consoleLines = last_line
  	for i in range(consoleLines):
  		print(lines[i])
  elif os.path.isfile(filename) == True:
  	with open(filename, 'r') as file:
  		lines = [line for line in file.readlines()]
  	file.close()
  	last_line = len(lines)
  	last_line = int(last_line)
  	if last_line < int(consoleLines):
  		consoleLines = last_line
  	for i in range(consoleLines):
  		print(f'{lines[i]}', end="")
  elif isinstance(filename, str):
  	lines = ''
  	lines = filename
  	last_line = 0
  	print(lines)
  else:
  	print('Could not read')
  	return
  if pipeOrRe == False:
  		return getNext(filename, consoleLines, pipeOrRe, start = 0, last_line = last_line, count=0)
  else:
  	return lines


def upLess(filename, consuleLines, pipeOrRe, start = 0, last_line= 0, count=0):
	if isinstance(filename, list):
		lines = []
		lines = filename
		if count < 0:
			os.system('cls' if os.name == 'nt' else 'clear')
			count += 1
			consuleLines -= 1
			start -=1
			for i in range(start, consuleLines):
				print(lines[i])
		else:
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
	elif os.path.isfile(filename):
		with open(filename, 'r') as file:
			lines = [line for line in file.readlines()]
			file.close()
		if count < 0:
			os.system('cls' if os.name == 'nt' else 'clear')
			count += 1
			consuleLines -= 1
			start -=1
			for i in range(start, consuleLines):
				print(f'{lines[i]}', end="")
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
		else:
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
	else:
		return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)

def downLess(filename, consuleLines, pipeOrRe, start = 0, last_line= 0, count=0):
	if isinstance(filename, list):
		lines = []
		lines = filename
		consuleLines = int(consuleLines)
		last_line = int(last_line)
		if last_line - consuleLines > 0:
			os.system('cls' if os.name == 'nt' else 'clear')
			count -=1
			start +=1
			consuleLines +=1
			for i in range(start, consuleLines):
				print(lines[i])
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
		else:
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
	elif os.path.isfile(filename):
		with open(filename, 'r') as file:
			lines = [line for line in file.readlines()]
			file.close()
		if last_line - consuleLines > 0:
			os.system('cls' if os.name == 'nt' else 'clear')
			count -=1
			start +=1
			consuleLines +=1
			consuleLines = int(consuleLines)
			last_line = int(last_line)
			for i in range(start, consuleLines):
				print(f'{lines[i]}', end="")
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
		else:
			return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)
	else:
		return getNext(filename, consuleLines, pipeOrRe, start, last_line, count)



def less(wasPiped=None, *args):
	import os
	pipeOrRe = False
	file = None
	for arg in args:
		if isinstance(arg, bool):
			pipeOrRe = arg
		else:
			file = arg
	if wasPiped == None:
		if os.path.isfile(file) != True:
			print(str(file) + ": is not a file")
			return
		else:
			defaultLess(file, pipeOrRe)
	else:
		defaultLess(file, pipeOrRe)
	
#less(None, 'Readme.txt')
#less(True, ['Hello', 'Parker'])
#less(None, 'aa.txt')
