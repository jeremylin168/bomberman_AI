from __future__ import print_function
import signal,copy,sys,time
from random import randint
from person import * 
from board import *


playerPos = [1,1]



class Player(Person):
	def __init__(self,height,width,score,lives):
		self.height = height
		self.width = width
		self.score = score
		self.lives = lives
		self.close =0
	def drawPlayer(self,x,y):
		if(gameArray[2*x+1][4*y+1]!="X" and gameArray[2*x+1][4*y+1]!="/"):
				gameArray[2*x+1][4*y+1] = "B" 
				gameArray[2*x+1][4*y+2] = "B"
				gameArray[2*x+1][4*y+3] = "B"
				gameArray[2*x+1][4*y+4] = "B"
				gameArray[2*x+2][4*y+1] = "B" 
				gameArray[2*x+2][4*y+2] = "B"
				gameArray[2*x+2][4*y+3] = "B"
				gameArray[2*x+2][4*y+4] = "B"
		return

	def checkPos(self,x,y):
		if(gameArray[2*x+1][4*y+1]=="X" or gameArray[2*x+1][4*y+1]=="/"):
			return -1
		return 1

	def checkEnemy(self,x,y):
		if(gameArray[2*x+1][4*y+1]=="E"):
			return -1
		return 1	

	def updatePlayer(self):
		x = playerPos[0]
		y = playerPos[1]
		self.drawPlayer(x,y)
		if(self.lives <= 0):
			print("Game Over")
			print("Score:",self.score)
			sys.exit(1)
		if self.close==0:
			print("Score      :",self.score,"\t\t\t\t\t\t","Lives left :",self.lives)
		#print("Lives left :",lives)
		return		
	def drawposPlayer(self,state):
		x = state.playerPos[0]
		y = state.playerPos[1]
		if(state.posArray[x+1][y+1]!="X" and state.posArray[x+1][y+1]!="/"):
			state.posArray[x+1][y+1]="B"			

	def playerInit(self):
		playerPos[0] = 1
		playerPos[1] = 1
		x = playerPos[0]
		y = playerPos[1]
		return

	def moveDown(self):
		x = playerPos[0]
		y = playerPos[1]
		if(self.checkEnemy(x+1,y)>0):
			if(self.checkPos(x+1,y)>0):
				playerPos[0] += 1
				self.drawPlayer(playerPos[0],playerPos[1])
		else:
			self.updateLife()
		return

	def moveUp(self):
		x = playerPos[0]
		y = playerPos[1]	
		if(self.checkEnemy(x-1,y)>0):
			if(self.checkPos(x-1,y)>0):
				playerPos[0] -= 1
				self.drawPlayer(playerPos[0],playerPos[1])
		else:
			self.updateLife()	
		return

	def moveLeft(self):
		x = playerPos[0]
		y = playerPos[1]		
		if(self.checkEnemy(x,y-1)>0):
			if(self.checkPos(x,y-1)>0):
				playerPos[1] -= 1
				self.drawPlayer(playerPos[0],playerPos[1])
		else:
			self.updateLife()
		return

	def moveRight(self):
		x = playerPos[0]
		y = playerPos[1]		
		if(self.checkEnemy(x,y+1)>0):
			if(self.checkPos(x,y+1)>0):
				playerPos[1] += 1
				self.drawPlayer(playerPos[0],playerPos[1])
		else:
			self.updateLife()
		return

	def updateScore(self, update):
		#global score
		self.bombscore += update
		return 

	def updateLife(self):
		#global lives
		self.lives -= 1
		playerPos[0] = 1
		playerPos[1] = 1
		return