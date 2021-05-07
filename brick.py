from __future__ import print_function
import signal,copy,sys,time
from random import randint
from board import *
brickPos = []

class Brick():
	def __init__(self,height,width):
		self.height = height
		self.width = width
	def brickInit(self,bricknum):
		for i in range(bricknum):
			x = randint(1,self.height-2)
			y = randint(1,self.width-2)	
			if gameArray[2*x+1][4*y+1]!="X" and not [x,y] in brickPos:
				brickPos.append([x,y])
		return

	def drawBricks(self):
		size = len(brickPos)
		for i in range(size):
			#print(i,"\n")
			x = brickPos[i][0]
			y = brickPos[i][1]
			
			if(x*y!=1 and (gameArray[2*x+1][4*y+1]!="X" )):
				gameArray[2*x+1][4*y+1] = "/" 
				gameArray[2*x+1][4*y+2] = "/"
				gameArray[2*x+1][4*y+3] = "/"
				gameArray[2*x+1][4*y+4] = "/"
				gameArray[2*x+2][4*y+1] = "/" 
				gameArray[2*x+2][4*y+2] = "/"
				gameArray[2*x+2][4*y+3] = "/"
				gameArray[2*x+2][4*y+4] = "/"
		return
	def drawposBricks(self,state):
		size = len(state.brickPos)
		for i in range(size):
			x = state.brickPos[i][0]
			y = state.brickPos[i][1]
			if(x*y!=1 and (state.posArray[x+1][y+1]!="X" )):
				state.posArray[x+1][y+1] = "/" 