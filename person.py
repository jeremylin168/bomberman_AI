from __future__ import print_function
import signal,copy,sys,time
from random import randint

class Person():
	def __init__(self,height,width):
		self.height = height
		self.width = width
	def checkPos(self,x,y):
		if(x<4 or x>=self.height*2-1 or y<2 or y>=width*4-3):
			return -1

