'''
 Program:       Terminal
 Author:        Parker Hagmaier
 Date:          February 20, 2022
Decription: This is the function that utilizes dictionaries in order to 
'call' the commands/functions. Each command/function is imported and then placed 
isnide the dictionary. the call function takes the actual function which is the command
that the user wants to engage with along with the paramiters wasPiped which indicates if 
the the command was piped or redirected in order to let the function know that it should excepct 
not only files but also strings and lists as that is how I returned output if the function is to
be piped/redirected. 
PipeOrRe is a param which is also passed and which is passed to all functions letting the 
function know if it should print or return it's output. 
X is a list which contains all the falgs and files or if it was piped strings and or lists
we pass x using *x because all the functions take args and so this passes the list not as a list but
everythig in the list as an arg for args
'''
from Sort import*
from Clear import*
from History import*
from Cd import*
from Less import*
from Ls import*
from Tail import*
from Head import*
from Cat import*
from Cp import*
from DoubleRe import*
from Grep import*
from HistoryLine import*
from MkDir import*
from Mv import*
from Pwd import*
from Rm import*
from Rmdir import*
from Wc import*
from Who import*
from Chmod import*
from Redirect import*
def call(func, wasPiped, pipeOrRed, x):
	dic = {'ls': ls, 'mkdir': mkdir, 'cd': cd, 'pwd': pwd, 'cp': cp, 'mv': mv, 'rmdir': rmdir, 'rm': rm,
	'cat': cat, 'less':less, 'head':head, 'tail': tail, 'grep': grep, 'wc': wc, 'doubleRe': doublere, 'redirect':redirect,
	'history': history, '!':historyLine, 'chmod': chmod, 'clear': clear, 'who': who, 'sort': sort}
	if func not in dic:
		print('Error. ' + func + ' is not a command')
		return
	else:
		return dic[func](wasPiped, pipeOrRed, *x )
