'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
 Description: This is the the code for the actual 'Terminal' part of the terminal
 meaning that this is where the user input is handeled i.e printing out every character typed
 deleteing characters and for my convience the history and !x command is also handeled inside
 here because they use the global variable History. The code utilizes getch which was given to us
 by Doctor Griffin which is what allows us to read individual characrers in from the user these
 characters are then printed by the printCommand function (only if character entered is not enter
 or control c). Before being taken to the print comman the character is appened with appendCommand
 which appends the enetered character to the command variable which holds the user input
 Before the start function is called which begins the terminal program we either read from or create
 a history file that will store the history from all commands enetered and the history is read into 
 a list. We also change to the home directory because that is how every shell I've encountered works.
 Sys is used because we write with color so we print directly to the command line so we dont use print
 and Colors allows us to print with color. Once a command is called through enter the printNewLine
 function is called so the output of the command is not printed on the same line as where the user 
 enters command and this calls the parser which in turn will call the associated command function
 (assuming user entered a correct command the parser or what the parser calls does error check for this)
 and then we append the history list and call new command which calls getchar so the user can enter their
 next command 
 easyhistory and easy command are the history and !x commands and are called when these commands are not piped
 only because as mentioned above they utilize the global variables in this file and possibly/probably
 because I am an incompetent programmer 
 Also it should be mentioned the start command although only used when the terminal program first
 begins is used to originally display the path and the soon to be entered commands and is similar to
 the printCommand but is only used as the 'jumping off point' of our terminal 
'''

from getch import Getch
import sys
import os
from Colors import*
from Parse import*

getch = Getch()
'''
The unpiped un redirected history command that reads from the global list/variable History
all this function does it print the contents of the list
'''
def easyhistory():
	for i in History:
		print(i)
	return
'''
Didn't know how to title !x so i called it 'the easyCommand' as in the easy version of the !x command
by easy i mean as above with easyHistory unpiped and un redirected. It looks for the number
enetered by the user and returs/prints the line entered and the user can press ener to call said
command he called up using the number given to him by the hisotry 
'''
def easyCommand(command):
	try:
		number = command[1:]
		number = int(number)
	except:
		print('Invalid command')
		return
	line = History[number-1]
	line = line[2:]
	return str(line)

'''
This function is what saves the users history to a file once the terminal is exited that way
a running history can be saved and is not only avaliable from the current session. If a previous
history file was there from previous sessions we technically overwrite and write everything that 
is in the list but nothing should be lost as we read in what was in the history file previously 
to that list at the beggiing 
'''
def historyFunc():
	home = os.path.expanduser('~')
	home = str(home)
	os.chdir(home)
	with open('history.txt', 'w') as hiistory:
		for i in History:
			hiistory.write(i + "\n")
		hiistory.close()
	return
'''
Start is what literally starts the terminal. It prints out the home path along with the $ sign
as is common in some terminals and then calls getNext where the user input will be collected 
'''
def start():
	location = os.getcwd()
	location = str(location)
	print(bcolors.OKBLUE, end='')
	sys.stdout.write("\r" + location + "$ ")
	return getNext()

'''
This is where user input is appened to the command so that whatever the user types not just the
current typed character will be seen the delete function currently works and is why there is a 
condition for is char == None which should only occur if delete. some of the code is commeneted out
because at one point at least on my ubuntu that would sucessfuly remove the deleted char from 
the command line but it currently doesn't at least on my mac enviorment it still lets you delete
characters but it doesn't display it as deleted until you overwrite it with another char.
This function then calls the print command to display the user input 
'''
def appendCommand(char, command):
	if char == None:
		command = command[:-1]
		location = os.getcwd()
		location = str(location)
		#sys.stdout.flush()
		#sys.stdout.write("\r" + location + "$ " + command)
		#don't know why this won't show the character as deleted
		return printCommand(command, location)
	else:
		command = command + char
		location = os.getcwd()
		location = str(location)
		return printCommand(command, location)
'''
After a command is entered the stat command is called again and essentially refrshes the 
terminal so that a new command can be eneted and ran
'''
def newCommand(command):
	return start()

'''
This is the function that prints and is called each time a new characrer is entered 
we use sys.stdout instead of print in order to write in color as well as keep each new appened
character on the same line 
'''
def printCommand(command, location):
	location = str(os.getcwd())
	sys.stdout.flush()
	sys.stdout.write("\r" + location + "$ " + command)
	return getNext(command)

'''
This does much more than print a new line although that was it's original function
in order for the output of the function not to write on the same line as the user input 
we have to print a new line and since this is only needed after a command is called whenever enter
is hit byt the user and a command is going to be processed this handles both the printing of the 
new line as well as calling 'parse' which will parse the user input in the command variable 
and call the proper command 
'''
def printNewline(command):
	History.append(str(len(History) + 1) + ' ' + command)
	print(bcolors.RESET, end='')
	sys.stdout.write("\r" + '\n')
	x = command.split()
	if x[0] == 'history'and len(x) == 1:
		easyhistory()
		return start()
	elif '!' in x[0] and len(x) == 1:
		p = easyCommand(*x)
		location = os.getcwd()
		location = str(location)
		return printCommand(p, location)
	else:
		parse(x)
		return start()

'''
This function is what caputres user input and mostly utilizes getch although it is the longest 
function it is probably the most simple because all it does is call other function depending
on what charecter was enetered. If user hits control c the terminal program closes and if not
it calls the append function to pass it the most recent character entered 
'''
def getNext(command=''):
	char = getch()
	if char == '\x03': # ctrl-c
		historyFunc()
		raise SystemExit("Bye.")
	elif char in '\x1b':
		null = getch()
		direction = getch()
		if direction in 'A':
			getNext(command)
			#return 'UP'
		if direction in 'B':
			getNext(command)
			#return "DOWN"
		if direction in 'D':
			getNext(command)
			#return "LEFT"
		if direction in 'C':
			getNext(command)
			#return "RIGHT"
		#if direction in '\r':
			#return printNewline(command)
	elif char ==  '\r':
		return printNewline(command)
	elif char == ' ':
		appendCommand(char, command)
	elif char == '\x7f':
		appendCommand(None, command)
		#getNext(command)
		#return printCommand(command[:-1], str(os.getcwd()))
		#delete char
	else:
		appendCommand(char, command)
    #return char
'''
This section of the code makes sure the user begins at the home directory and makes sure if a history
file is not present and this is your first time using this program a file will be created and 
if this isn't the first time then the contents of the history will be read into a global list History
'''

home = os.path.expanduser('~')
home = str(home)
os.chdir(home)
global History
History = []
if os.path.isfile('history.txt') == False:
	with open('history.txt', 'w') as history:
		history.close()
else:
	with open('history.txt', 'r') as history:
		historyLines = history.read()
		History = historyLines.split('\n')
		history.close()
#here is where we begin our program
start()
