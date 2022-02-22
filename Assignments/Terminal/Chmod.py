'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: Chmod changes the permissions of the file. Like all my functions it takes in wasPiped and args
args will check for if file should be redirected along with the number that will end up being the change in file
permisions. count is used to make sure only the number and file were enetered by the user. and we also error check to make sure it was not 
only a number but not a number that is too large along with making sure the file that is to be changed exists. In order to convert the 
number to octal we have to save the result of (number_entered, 8) which converts it and then we save that as an integer and use the 
os.chmod command to change the permissions accordingly. 
'''
import os
def chmod(wasPiped=None, *args):
	pipeOrRe = False
	count = 0
	file = None
	x = None
	num = None
	for arg in args:
		count+=1
		if isinstance(arg, bool) == True:
			pipeOrRe = arg
		elif os.path.isfile(arg) == True:
			file = arg
		else:
			try:
				x = int(arg)
				num = arg
			except:
				pass
	if count != 3:
		print('1 Invalid command')
		return
	if file == None or x == None:
		print('3 invalid command')
		return 
	else:
		if len(num) > 4:
			print('invalid mode: ' + str(x))
			return
		else:
			#change = x
			octal = int(num, 8)
			try:
				os.chmod(file, octal)
				return
			except:
				print('invalid mode: ' + change + ' or invalid file')
				return
#chmod(None, False, '777', 'modme.txt')
