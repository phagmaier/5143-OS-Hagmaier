'''
 Program:       Terminal
 Author:        Dr. Griffin
 Date:          February 20, 2022
Decription: This is a class that allows user input to be captured 
This class is used in both my main function to capture user input for the terminal and
it is user in the Less function is order to capture both up and down arrows along 
with the space bar q and control c
'''

class Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self):
        return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty
        import sys
    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()
if __name__=='__main__':
    G = Getch()
    while(G):
        pass
