from __future__ import print_function
import signal,copy,sys,time
from random import randint
from board import *
from player import *
from enemy import *
from brick import *

bomPos = [0,0,-1]
bombThrown = 0
bimbo=[]

class Bomb():
	def __init__(self,height,width,pl,en):
		self.width = width
		self.height = height
		self.pl = pl
		self.en = en
	def drawBomb(self):
		x = bomPos[0]
		y = bomPos[1]
		#print(bomPos[0],bomPos[1],bomPos[2])

		if(bomPos[2] > -1):
			if not bimbo:
				for i in range(1,3):
					for j in range(1,5):
						bimbo.append([2*x+i,4*y+j])

			gameArray[2*x+1][4*y+1] = bomPos[2]
			gameArray[2*x+1][4*y+2] = bomPos[2]
			gameArray[2*x+1][4*y+3] = bomPos[2]
			gameArray[2*x+1][4*y+4] = bomPos[2]
			gameArray[2*x+2][4*y+1] = bomPos[2]
			gameArray[2*x+2][4*y+2] = bomPos[2]
			gameArray[2*x+2][4*y+3] = bomPos[2]
			gameArray[2*x+2][4*y+4] = bomPos[2]
		bomPos[2] -= 1
		if(bomPos[2] == -1):
			self.explosion()
		return

	def drawExplosion(self,x,y):

		gameArray[2*x+1][4*y+1] = "e"
		gameArray[2*x+1][4*y+2] = "e"
		gameArray[2*x+1][4*y+3] = "e"
		gameArray[2*x+1][4*y+4] = "e"
		gameArray[2*x+2][4*y+1] = "e"
		gameArray[2*x+2][4*y+2] = "e"
		gameArray[2*x+2][4*y+3] = "e"
		gameArray[2*x+2][4*y+4] = "e"		
		return

	def afterExplosion(self,x,y):

		if(x == playerPos[0] and y == playerPos[1]):
		#	print("pakad gya")
			self.pl.updateLife()

		if(enemyNum>0 and [x,y] in enemyPos):
			enemyPos.remove([x,y])
			self.pl.updateScore(100)
			self.en.updateNum(-1)
		if([x,y] in brickPos):
			brickPos.remove([x,y])
			self.pl.updateScore(20)	

		bimbo[:]=[]
		return

	def checkPos(self,x,y):
		if(gameArray[2*x+1][4*y+1]=="X" ):
			return -1
		return 1


	def explosion(self):
		x = bomPos[0]
		y = bomPos[1]
		self.drawExplosion(x,y)
		self.afterExplosion(x,y)

		if(self.checkPos(x-1,y)>0):
			self.drawExplosion(x-1,y)
			self.afterExplosion(x-1,y)

		if(self.checkPos(x+1,y)>0):
			self.drawExplosion(x+1,y)
			self.afterExplosion(x+1,y)

		if(self.checkPos(x,y-1)>0):
			self.drawExplosion(x,y-1)
			self.afterExplosion(x,y-1)

		if(self.checkPos(x,y+1)>0):
			self.drawExplosion(x,y+1)
			self.afterExplosion(x,y+1)
		return
class posBomb():
	def __init__(self,height,width,power=1,timer=3):
		self.width = width
		self.height = height
		self.power = power
		self.timer = timer
	def drawBomb(self,state):
		x = state.bomPos[0]
		y = state.bomPos[1]
		if(state.bomPos[2] > -1):
			state.posArray[x+1][y+1] = state.bomPos[2]
		state.bomPos[2] -= 1
		if(state.bomPos[2] == -1):
			self.explosion(state)
			state.bomPos[2] -= 1
	def explosion(self,state):
		x = state.bomPos[0]
		y = state.bomPos[1]
		state.posArray[x+1][y+1] = "e"
		self.afterExplosion(x, y, state)
		for i in range(1,self.power+1):
			if(self.checkPos(x-i,y,state)):
				state.posArray[x+1-i][y+1] = "e"
				self.afterExplosion(x-i,y,state)
			else:
				break
		for i in range(1,self.power+1):
			if(self.checkPos(x+i,y,state)):
				state.posArray[x+1+i][y+1] = "e"
				self.afterExplosion(x+i,y,state)
			else:
				break
		for i in range(1,self.power+1):
			if(self.checkPos(x,y-i,state)):
				state.posArray[x+1][y+1-i] = "e"
				self.afterExplosion(x,y-i,state)
			else:
				break
		for i in range(1,self.power+1):
			if(self.checkPos(x,y+i,state)):
				state.posArray[x+1][y+1+i] = "e"
				self.afterExplosion(x,y+i,state)
			else:
				break
	def checkPos(self,x,y,state):
		if(state.posArray[x+1][y+1]=="X" ):
			return False
		return True
	def afterExplosion(self,x,y,state):
		if(x == state.playerPos[0] and y == state.playerPos[1] and state.alive):
			state.bombscore -=200
			state.lives-=1
			state.playerPos = [1,1]
			state.alive = False
		if([x,y] in state.enemyPos):
			state.enemyPos.remove([x,y])
			state.bombscore+=200
			state.enemyNum-=1
		if([x,y] in state.brickPos):
			state.brickPos.remove([x,y])
			state.bombscore	+=20