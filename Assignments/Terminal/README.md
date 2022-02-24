# Terminal Project
 Name Terminal Project
 Date: 2/20/2022
 Shell must be ran in the terminal. 
 Group of: Parker Hagmaier, Sabin Dheke, and, Md Abubakkar.
 In this project we have created a basic terminal using python.
 a full list of the functions and commands can be found in the commands.md page
 I am not great at github so if this needs to be more orginized or changed in some way please let me know
 All of our commands/functions work and are able to be redirected/piped and or recieve input from both pipes and redirects 
 Not all of the code is perfect for example our ls does not display the way ls is displayed sorted into rows in columns in a real terminal but 
 Everything does work. Also it should be noted our delete function does not function perfectly either and I don't know why on one point it worked
 in Ubuntu and I tried to change it for mac and cannot remeber what was chnaged but it does technically delete but the characters don't show 
 as being deleted if you write over them the chnage is reflected but until them it just looks like the cursor is moving backwards 
 it is most likley a simple mistake that I am too incompetent to fix for myself 
 another problem is if a list is nested not all commands/functions will remove the outer brackets and this will effect commands such as sort
 The shell.py file contains the actual shell which is what takes user input and calls commands or at least calls the fnction that calls commands
 the shell.py is the shell part but the work of sending the commands to get called and dealing with pipe or redirects is done in the parse.py file which then
 calls the call() function which uses a dictionary that has all our functions imported into it
 our parse uses reccursion to deal with pipeing and or redirection constantly calling itself without the pipe or redirect and then feeding that in as input to the 
 next command this is more thourgly explained in the comments of each specific command/function 
 The Ls command is where i recieved the most help since i was clueless on how to accomplish this and it will be cited bellow along with others
## Sources:
 LS Command (source which was the source I took from more than any other source): Carl Tashian Youtube channel (https://www.youtube.com/watch?v=VTNrfcDrP_U&t=107s) 
 Colors: https://stackoverflow.com/questions/63768372/color-codes-for-discord-py (Used almost in its entirety since it is just the codes on how to change the color)
 The sort in Ls along with the sort in my sort function to sort by lowercase is from: https://stackoverflow.com/questions/28136374/python-sort-strings-alphabetically-lowercase-first
 rm and rm dir. (How to use shutil to remove directories/files): https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/
 Cd (how to change directories in python): https://www.geeksforgeeks.org/change-current-working-directory-with-python/
 Pwd (how to get the current working directory python): https://www.tutorialspoint.com/How-to-know-current-working-directory-in-Python
