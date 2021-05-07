from __future__ import print_function
import signal,copy,sys,time,msvcrt
from random import randint

class GetchUnix:
    """
    def __init__(self):
        import tty 

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    """
    def __init__(self,timeout=1):
        import msvcrt 
        self.timeout=timeout
    def __call__(self):
        import msvcrt
        crtime = time.time()
        while(time.time()-crtime<self.timeout):
            if msvcrt.kbhit():
                return msvcrt.getch().decode("utf-8")
            else:
                pass
        return ''
    """class_GetchWindows: 
   def__init__(self): 
       importmsvcrt 
   def__call__(self): 
       importmsvcrt 
       returnmsvcrt.getch() """
