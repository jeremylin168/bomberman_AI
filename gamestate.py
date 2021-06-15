import signal,copy,sys,time,select
from random import randint
import random
import os
from gameplay import *
from getchunix import *
from person import *
from player import *
from bomb import *
from brick import *
from alarmexception import *
import math

class Gamestate():
	def __init__(self,g,posArray=[],enemyPos=[],enemyNum=2,bomPos=[],playerPos=[],brickPos=[],bricknum=10,height=11,width=11,score=0,lives=3,MovePattern=0,bombscore=0,enemyscore=0):
		self.posArray = [x[:] for x in posArray]
		self.enemyPos =  [x[:] for x in enemyPos]
		self.enemyNum = enemyNum
		self.MovePattern=MovePattern
		self.bomPos = [x for x in bomPos]
		self.playerPos = [x for x in playerPos]
		self.brickPos = [x[:] for x in brickPos]
		self.bricknum = bricknum
		self.height = height
		self.width = width
		self.score = score #=bombscore + enemyscore
		self.bombscore = bombscore #the score earn from bomb
		self.enemyscore = enemyscore #the score related to enemy
		self.lives = lives
		self.g = g
		self.alive = True
	
	def gameinit(self,height,width,lives=3,bricknum=10,enemyNum=2,score=0,MovePattern=0,bombscore=0,enemyscore=0):
		self.score=score
		self.bombscore=bombscore
		self.enemyscore=enemyscore
		self.height=height
		self.width=width
		self.lives = lives
		self.bricknum = bricknum
		self.enemyNum = enemyNum
		self.MovePattern = MovePattern
		self.posArray = [[0 for x in range(self.width+1)] for y in range(self.height+1)]
		self.brickPos = []
		self.enemyPos = []
		self.bomPos = [0,0,-2]
		self.g.bo.drawposboard(self)
		self.playerPos = [1,1]
		self.g.pl.drawposPlayer(self)
		tp=tmpbrnum=self.bricknum
		while tmpbrnum>0:
			x = randint(1,self.height-2)
			y = randint(1,self.width-2)	
			if self.posArray[x+1][y+1]!="X" and not [x,y] in self.brickPos and not [x,y] in [[1,2],[2,1]]:
				self.brickPos.append([x,y])	
				tmpbrnum-=1
			tp-=1
			if tp<=-10:
				break	
		self.g.br.drawposBricks(self)
		tp=tmpennum=self.enemyNum
		while tmpennum>0:
			x = randint(1,self.height-2)
			y = randint(1,self.width-2)	
			if self.posArray[x+1][y+1]!="X" and not [x,y] in self.enemyPos and self.posArray[x+1][y+1]!="/" and not  (x==1 and y==1):
				self.enemyPos.append([x,y])
				tmpennum-=1
			tp-=1
			if tp <=-10:
				break
		self.g.en.drawposEnemy(self)
	def getnextstep(self,agents,actions,selfmove=0):
		if selfmove==0:
			state = Gamestate( self.g ,self.posArray, self.enemyPos, self.enemyNum, self.bomPos, self.playerPos, self.brickPos, self.bricknum, self.height, self.width, self.score, self.lives, self.MovePattern,self.bombscore,self.enemyscore)
			if(agents==0): #move player
				if(actions == 's'):
					state.playerPos[0]+=1	#moves the player down on pressing 's'
				elif(actions == 'w'):
					state.playerPos[0]-=1	#moves the player up on pressing 'w'
				elif(actions == 'a'):
					state.playerPos[1]-=1	#moves the player left on pressing 'a'
				elif(actions == 'd'):
					state.playerPos[1]+=1	#moves the player right on pressing 'd'
				elif(actions == 'b'):	#spawn a bomb on pressing 'b'
					if(state.bomPos[2] <= -1):
						state.bomPos[0] = state.playerPos[0]
						state.bomPos[1] = state.playerPos[1]
						state.bomPos[2] = self.g.posbo.timer
			elif(agents>0): # move enemy
				#print("move"+actions)
				#print(agents)
				#print(self.enemyNum)
				if(actions == 's'):
					state.enemyPos[agents-1][0]+=1	
				elif(actions == 'w'):
					state.enemyPos[agents-1][0]-=1	
				elif(actions == 'a'):
					state.enemyPos[agents-1][1]-=1	
				elif(actions == 'd'):
					state.enemyPos[agents-1][1]+=1
				if(agents==self.enemyNum):

					state.updatestate()
			return state
		else:
			if(agents==0):
				if(actions == 's'):
					self.playerPos[0]+=1	#moves the player down on pressing 's'
				elif(actions == 'w'):
					self.playerPos[0]-=1	#moves the player up on pressing 'w'
				elif(actions == 'a'):
					self.playerPos[1]-=1	#moves the player left on pressing 'a'
				elif(actions == 'd'):
					self.playerPos[1]+=1	#moves the player right on pressing 'd'
				elif(actions == 'b'):	#spawn a bomb on pressing 'b'
					if(self.bomPos[2] <= -1):
						self.bomPos[0] = self.playerPos[0]
						self.bomPos[1] = self.playerPos[1]
						self.bomPos[2] = self.g.posbo.timer
				self.enemyMove(self.MovePattern)
				self.updatestate()
			elif(agents>0):
				if(actions == 's'):
					self.enemyPos[agents-1][0]+=1	
				elif(actions == 'w'):
					self.enemyPos[agents-1][0]-=1	
				elif(actions == 'a'):
					self.enemyPos[agents-1][1]-=1	
				elif(actions == 'd'):
					self.enemyPos[agents-1][1]+=1
	def updatestate(self):
		self.alive =True
		self.g.bo.drawposboard(self)
		self.g.pl.drawposPlayer(self)
		self.g.br.drawposBricks(self)
		self.g.en.drawposEnemy(self)
		#self.bomPos[2]-=1
		self.g.posbo.drawBomb(self)
		if not self.alive:
			self.g.pl.drawposPlayer(self)
		self.updatescore()
	def updateEnemystate(self):
		self.alive =True
		self.g.bo.drawposboard(self)
		self.g.pl.drawposPlayer(self)
		self.g.br.drawposBricks(self)
		self.g.en.drawposEnemy(self)
		if not self.alive:
			self.g.pl.drawposPlayer(self)
	def getLegalActions(self,agents):
		li = ['x'] # x =stop
		if agents==0:
			if (self.bomPos[2] <= -1):
				li.append('b')
			if(self.posArray[self.playerPos[0]+2][self.playerPos[1]+1]!="X" and self.posArray[self.playerPos[0]+2][self.playerPos[1]+1]!="/"):
				li.append('s')
			if(self.posArray[self.playerPos[0]][self.playerPos[1]+1]!="X" and self.posArray[self.playerPos[0]][self.playerPos[1]+1]!="/"):
				li.append('w')
			if(self.posArray[self.playerPos[0]+1][self.playerPos[1]+2]!="X" and self.posArray[self.playerPos[0]+1][self.playerPos[1]+2]!="/"):
				li.append('d')
			if(self.posArray[self.playerPos[0]+1][self.playerPos[1]]!="X" and self.posArray[self.playerPos[0]+1][self.playerPos[1]]!="/"):
				li.append('a')
			#self.li[0].append(li)
			return li
		elif(agents>0):
			agents-=1
			if(self.posArray[self.enemyPos[agents][0]+2][self.enemyPos[agents][1]+1]!="X" and self.posArray[self.enemyPos[agents][0]+2][self.enemyPos[agents][1]+1]!="/"  and [self.enemyPos[agents][0]+1,self.enemyPos[agents][1]] not in self.enemyPos):
				li.append('s')
			if(self.posArray[self.enemyPos[agents][0]][self.enemyPos[agents][1]+1]!="X" and self.posArray[self.enemyPos[agents][0]][self.enemyPos[agents][1]+1]!="/" and [self.enemyPos[agents][0]-1,self.enemyPos[agents][1]]not in self.enemyPos):
				li.append('w')
			if(self.posArray[self.enemyPos[agents][0]+1][self.enemyPos[agents][1]+2]!="X" and self.posArray[self.enemyPos[agents][0]+1][self.enemyPos[agents][1]+2]!="/" and [self.enemyPos[agents][0],self.enemyPos[agents][1]+1]not in self.enemyPos):
				li.append('d')
			if(self.posArray[self.enemyPos[agents][0]+1][self.enemyPos[agents][1]]!="X" and self.posArray[self.enemyPos[agents][0]+1][self.enemyPos[agents][1]]!="/" and [self.enemyPos[agents][0],self.enemyPos[agents][1]-1] not in self.enemyPos):
				li.append('a')
			#print("legalmove:")
			#print(agents)
			#self.li[agents].append(li)
			return li
	def enemyMove(self,pattern=0):
		if pattern==1:
			self.enemySmartMove()
		else:
			self.enemyRamdomMove()
	def enemyRamdomMove(self):
		for i in range(self.enemyNum):
			li = self.getLegalActions(i+1)
			action = random.choice(li)
			self.getnextstep(i+1, action,1)
	def enemySmartMove(self):
		for i in range(self.enemyNum):
			li = self.getLegalActions(i+1)
			action='x'
			dis = 10000
			for ac in li:
				if(ac == 's'):
					ndis = min(pow(self.enemyPos[i][0]+1-self.playerPos[0],2)+pow(self.enemyPos[i][1]-self.playerPos[1],2),dis)
				elif(ac == 'w'):
					ndis = min(pow(self.enemyPos[i][0]-1-self.playerPos[0],2)+pow(self.enemyPos[i][1]-self.playerPos[1],2),dis)
				elif(ac == 'a'):
					ndis = min(pow(self.enemyPos[i][0]-self.playerPos[0],2)+pow(self.enemyPos[i][1]-1-self.playerPos[1],2),dis)
				elif(ac == 'd'):
					ndis = min(pow(self.enemyPos[i][0]-self.playerPos[0],2)+pow(self.enemyPos[i][1]+1-self.playerPos[1],2),dis)
				else:
					ndis = min(pow(self.enemyPos[i][0]-self.playerPos[0],2)+pow(self.enemyPos[i][1]-self.playerPos[1],2),dis)
				#print(ac)
				#print(ndis)
				#print(dis)
				if(ndis!=dis):
					dis = ndis
					action=ac
			#action = random.choice(['x',action])
			self.getnextstep(i+1, action,1)
	def getenemyNum(self):
		return self.enemyNum
	def isLose(self):
		if self.lives <=0:
			return True
		else:
			return False
	def isWin(self):
		if self.enemyNum <=0:
			return True
		else:
			return False
	def getscore(self):
		self.updatescore()
		if self.isLose():
			return None
		else:
			return self.score
	def updatescore(self):
		self.score = self.bombscore + self.enemyscore
			