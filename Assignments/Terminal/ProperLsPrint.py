# Not being able to print ls in the proper format really bothered me and 
# I just wanted to prove to myself that I could do it
# It's one of those problems you have to think about for a second and I'm much more of 
# a throw everything at the wall without planning ahead and see what sticks so just wanted to prove I wasn't a complete idiot 


x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29]
columns = 3 #pretending we got this from the os function that gets number of terminal lines 
rows = len(x) // columns
if len(x) % columns != 0:
	rows +=1
b = []
row = 0
string = '1'
stop = False
for i in range(rows):
	while row < columns:
		if row == 0:
			b.append(x[i])
			row +=1
			position = i + rows
		else:
			try:
				b.append(x[position])
				row +=1
				position += rows
			except:
				for item in b:
					print(item, end = ' ')
				stop = True
				break
	if stop != True:
		for item in b:
			print(item, end = ' ')
		print('\n')
		row = 0
		b = []
		position = 0
