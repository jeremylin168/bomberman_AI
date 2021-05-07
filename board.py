from __future__ import print_function
import signal,copy,sys,time
from random import randint
#gameArray = [[0 for x in range(80)] for y in range(40)]
gameArray = []
#posArray = []
#do = True
class Board():
	def __init__(self,height,width):
		self.height = height
		self.width = width
	def gameBoard(self):
		gameArray[0][0]=1
		theight = self.height*2+1
		twidth = self.width*4+1
		for i in range(1,theight):
			for j in range(1,twidth):
					if ( i<3 or i>=theight-2 ):
						gameArray[i][j] = "X"
					elif ( j<5 or j>=twidth-4 ):
						gameArray[i][j] = "X"
					elif ( (i>4 and j>8) and (i%4==1 or i%4==2) and (j%8==1 or j%8==2 or j%8==3 or j%8==4)):#and i<36 and j<73
						gameArray[i][j] = "X"
					else:
						gameArray[i][j] = " "
		
		return gameArray
	def drawposboard(self,state):
		state.posArray[0][0]=1
		for i in range(1,state.height+1):
			for j in range(1,state.width+1):
				if (i<=1 or i >=state.height):
					state.posArray[i][j]="X"
				elif (j<=1 or j >=state.width):
					state.posArray[i][j]="X"
				elif((i>2 and j>2) and (i%2==1) and (j%2==1)):
					state.posArray[i][j] = "X"
				else:
					state.posArray[i][j] = " "




	