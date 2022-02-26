'''
 Program:       Terminal
 Author:        Parker Hagmaier and Youtube channel: Carl Tashian(https://www.youtube.com/watch?v=VTNrfcDrP_U&t=107s)
 Date:          February 20, 2022
Decription: This command is broken into several functions. Each falg has it's own function. There is also a function for pathExists which is not 
100% neccisary and still exists from previous terminal iterations but it does do some error checking still and it makes sure if you ls into a directory
that is not your current directory it is in fact a directory and it won't crash your program
The filetype function is called with long listing flags and detirmes if the file is a directory or not using stat.S_ISDIR()
The getTime function gets the time and date and converts it into how it is displayed in a real terminal 
The print function takes in the flags and if it is a long list it will display the output horizontall (the output does not match how actual ls displays)
and if it is a long list flag then the output will be displayed vertically this output does match the ls command in a real terminal
standardLs functions searches through the directory using os.listdir and anything that begins with a . will not be displayed 
the h function converts the sizes of the files and or directories inside the directory and converts it to K for thousand G for 1000000000 ect... 
For long list we have to get permissions size type of file the time userid and owner to do this we have to loop through all the files in the directory 
and we mostly use built in os functions along with getpwuid and getgrid for the group name and user id. Once you know what you are looking for and have to collect
in ls you use the inbuilt commands on each file you are looping through in the directory. 
#come back and comment the rest later later 
'''
import os
import stat
from pwd import getpwuid
from grp import getgrgid
import sys
'''
A leftover from previous versions it tries to make sure the ls directory
command where a directory that is not the current directory actually exists it is a function that error 
checks and makes sure this directory really is present within the system 
'''
def pathExists(path, current_path):
	x = os.path.exists(path)
	y = path
	if x == False:
		x = os.path.exists(current_path + '/' + path)
		y = current_path + '/' + path
	if x == False:
		x = os.path.exists(current_path + '\\' + path)
		y = current_path + '\\' + path
	if x == False:
		x = os.path.exists(current_path + path)
		y = current_path + path
	return y

'''
function to determine if file or directory and return the corresponding letter to be displayed 
d is for directory. Didn't need to be a function to itself but again I thought it made it easier and more readable
'''
def filetype(file):
	if stat.S_ISDIR(file):
		return 'd'
	else:
		return '-'
'''
a function to conver the datetime into the format it is diplayed in a real ls terminal commmand
'''
def get_time(date):
	import datetime
	time = datetime.datetime.fromtimestamp(date)
	return time.strftime('%b %d %H:%M')

'''
Thought it would unjumble the code if we could just send each command that needs to be printed to a print command 
ls prints differently depending if it is called with a -l flag. It is not displayed just as it is in the real command 
version since our non l display doesn't print alphabetically vertically and then switches to the next column to again display
horizontally we just print horizontally.
THe l flag prints all the directories/files vertically 
'''
def printFunc(data, flag=None):
	if flag == None:
		for thing in data:
			if ' ' in thing:
				thing = "'" + thing + "'"
			print(f'{thing}', end=" ")
		sys.stdout.write("\r" + '\n')
	elif 'l' in flag:
		for content in data:
			print(*content, sep = " ")
		sys.stdout.write("\r" + '\n')
	else:
		print('ERROR: Something wrong with my print command')
		sys.stdout.write("\r" + '\n')
		return
'''
here we loop through everything in the specified directory and we append it to the list x 
there is a condition to add quotes around spaces files/directories to mimic the real ls command
we also sort this list so it will be displayed as closley to the real ls command as possible 
the two sorts are an attempt to sort by lowercase which was suprisingly difficult the code to do this 
I found online and is cited in the sources section of our readme.md document 
'''

def standardLs(path):
	x = []
	for entry in os.listdir(path):
		if entry[0] != '.':
			x.append(entry)
	x.sort(key=lambda y:(not y.islower(), y))
	x = sorted(x, key = str.lower)
	for thing in x:
		if ' ' in thing:
			thing = "'" + thing + "'"
	return x
'''
The h function converts the filesizes into something more 'human readable'
to do this we must determine the size and depending on it's size we divide it by the corresponding character
i.e if it's of size 10000 it must be divided by 1000 and this 1000 will be replaced by k and whatever is left over 
will be expressed as a decimal 
'''
def hFunction(size):
	if size < 1000:
		hsize = str(size)
	elif size >= 1000000000:
		hsize = size / 1000000000
		hsize = float("{0:.1f}".format(hsize))
		hsize = str(hsize) + 'G'
	elif size >= 1000000:
		hsize = size / 1000000
		hsize = float("{0:.1f}".format(hsize))
		hsize = str(hsize) + 'M'
	else:
		hsize = size / 1000
		hsize = float("{0:.1f}".format(hsize))
		hsize = str(hsize) + 'K'
	return hsize
'''
In long list as with all the ls functions we need to loop through everything in the directory 
the for loop variable is fn. We then collect and save all the information from the filestats function and 
saving each particular aspect like owner or user id to a variablle. We also must determine the the file permisions 
the characters for these must be determined since they are originally in numeric format. We put the particular 
permission character in a list and from the source video cited above I learned you can determine what mode characters 
corresponds to what number through a clever way of doing a modulus 3 (i % 3) on each number to determine what the 
correspondng character is 
'''
def longList(path, h=None):
	x = []
	for fn in standardLs(path):
		filestats = os.stat(fn)
		#filestats = os.stat(path + "/" + fn)
		owner = str(filestats.st_nlink)
		uid = getpwuid(filestats.st_uid).pw_name
		grName = getgrgid(filestats.st_gid).gr_name
		if h ==None:
			size = str(filestats.st_size)
		else:
			size = hFunction(filestats.st_size)
		mode_chars = ['r', 'w', 'x']
		st_perms = bin(filestats.st_mode)[-9:]
		mode = filetype(filestats.st_mode)
		for i, perm in enumerate(st_perms):
			if perm == '0':
				mode += '-'
			else:
				mode += mode_chars[i % 3]
		time = get_time(filestats.st_mtime)
		y = [mode, owner, uid, grName, size, time, fn]
		x.append(y)
	return x

'''
Lsa is the long listing expect we include files that begin with '.' (dot)
we Here we just have to use a for loop to list through everything in the directory and append them to 
the y list and then we sort everything inside the array and return it to either be returned again or sent 
to the print function
'''
def lsA(path):
  x = ['.', '..']
  y = []
  for thing in os.listdir(path):
    if ' ' in thing:
      multiword = "'" + thing + "'"
      x.append(multiword)
    elif thing[0] == '.':
      y.append(thing[1:])
      x.append(thing[1:])
    else:
      x.append(thing)
  x.sort(key=lambda y:(not y.islower(), y))
  x = sorted(x, key = str.lower)
  for i in range(len(x)):
    for k in range(len(y)):
      if x[i] == y[k]:
        x[i] = '.' + x[i]
  return x

'''
here we get the 'filestats' of all files/directories in a directory 
as you can see we have to remove quotes from spaced directories/files since on mac the quote is passed
literally and it will not recognize the file hence the if statment for quotes and the fn[1:-1]
we then get the owner userId and group id all using the respictive call of the filestats.
If h is a flag we also modift the size by calling the hFunction on the silests.st_size variable
we also collect the mode and perms once agaiin using filestats
'''
def longListA(path, h=None):
	x = []
	for fn in lsA(path):
		if ' ' in fn:
			filestats = os.stat(path +'/'+  fn[1:-1])
		else:
			filestats = os.stat(path +'/'+  fn )
		owner = str(filestats.st_nlink)
		uid = getpwuid(filestats.st_uid).pw_name
		grName = getgrgid(filestats.st_gid).gr_name
		if h==None:
			size = str(filestats.st_size)
		else:
			size=hFunction(filestats.st_size)
		mode_chars = ['r', 'w', 'x']
		st_perms = bin(filestats.st_mode)[-9:]
		mode = filetype(filestats.st_mode)
		for i, perm in enumerate(st_perms):
			if perm == '0':
				mode += '-'
			else:
				mode += mode_chars[i % 3]
		time = get_time(filestats.st_mtime)
		y = [mode, owner, uid, grName, size, time, fn]
		x.append(y)
	return x
'''
This function will call the correct ls function depending on what falgs were or were not passed
the variable and checks to make sure that the proper directory is passed is not necisary and was a reminant from 
earlier terminal design where I thought the current directory must always be passed but I am afraid to delete anything and break the 
function. That being said what we do here is we check if the function is to be piped and if it's not we call the correct ls function
and save the output as a variable and then send that output to the print command. Need a print command because if it is 
redirected this print command will not be called and the long list print is different then the non long list print/display
'''
def callLs(path, flag, pipeOrRed, currentDir):
	if path !=None:
		newpath = currentDir + path
		if os.path.isdir(newpath) == False:
			newpath = currentDir + '/' + path
			if os.path.isdir(newpath) == False:
				newpath = path
				if os.path.isdir(newpath) == False:
					print('Invalid path')
					return
		currentDir = newpath
	if flag == None or flag == '-h':
		x = standardLs(currentDir)
		if pipeOrRed == False:
			printFunc(x)
			return
		else:
			return x
	elif flag == '-a' or flag == '-ah' or flag == 'ha':
		x = lsA(currentDir)
		if pipeOrRed == False:
			printFunc(x)
			return
		else:
			return x
	elif flag == '-l':
		x = longList(currentDir)
		if pipeOrRed == False:
			printFunc(x, '-l')
			return
		else:
			return x
	elif flag == '-la' or flag == '-al' and flag == None:
		x = longListA(currentDir)
		if pipeOrRed == False:
			printFunc(x, '-l')
			return x
		else:
			return x
	elif 'l' in flag and 'a' in flag and 'h' in flag and '-' in flag:
		x = longListA(currentDir, True)
		if pipeOrRed == False:
			printFunc(x, 'l')
			return x
		else:
			return x
	else:
		print('ls: invalid flag: ' + flag)
		return

'''
This function parses the argements sent and determines if it was piped if it should be piped and 
also error checks to make sure we didn't call ls on some directory that doesn't exist.
After we error check and colect flags by looping through the args we call callLs a function that
will call the proper ls function depending on what falgs were or were not passed 
'''
def ls(wasPiped, *args):
	import os
	pipeOrRed = False
	path = None
	currentDir = os.getcwd()
	flag = None
	count = 0
	for arg in args:
		count +=1
		if isinstance(arg, bool):
			pipeOrRed = arg
		elif arg[0] == '-':
			flag = arg
		elif os.path.isdir(arg) == True:
				path = arg
		else: 
			path = arg
	if count > 3:
		#add colored error print
		print('An Error occured')
		return
	else:
		#think i have to return this 
		return callLs(path, flag, pipeOrRed, currentDir)
		#callLs(path, flag, pipeOrRed, currentDir)
#home = os.path.expanduser('~')
#os.chdir(home)
#os.chdir(home + '/' + 'Desktop')
#print(filestats = os.stat('test file'))
#ls( '-a')
