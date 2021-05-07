from __future__ import print_function
import signal,copy,sys,time
from random import randint
from termcolor import colored
from board import *
from brick import *
from person import *
from player import *
from enemy import *
from bomb import *




class Gameplay():
	def __init__(self,height,width,bo,br,pl,en,bom,posbo):
		self.cur_time = time.time()
		self.width = width
		self.height = height
		self.br = br
		self.pl = pl
		self.en = en
		self.bom = bom
		self.bo = bo
		self.posbo = posbo
	def printboard(self,close=0):
		self.pl.close = close
		gameArray = self.bo.gameBoard()
		#gg = bo.gameBoard(1,1)
		self.br.drawBricks()
		self.pl.updatePlayer()

		run_time = time.time() - self.cur_time
		if(run_time > 1):
			self.en.updatePos()
			self.cur_time = time.time()
			self.en.drawEnemy()
		else:
			self.en.drawEnemy()

		
		if(run_time > 1 and bomPos[2] >= 0):
			self.bom.drawBomb()
			pass
		if close==0:
			for i in range(1,self.height*2+1):#39
				for j in range(1,self.width*4+1):#77
					if(gameArray[i][j]=="X"):
						print(colored(gameArray[i][j],"blue"),end="")
					elif(gameArray[i][j]=="E"):
						print(colored(gameArray[i][j],"red"),end="")
					elif(gameArray[i][j]=="/"):
						print(colored(gameArray[i][j],"green"),end="")
					elif bimbo and [i,j] in bimbo:
						print(bomPos[2],end="")
					else:
						print(gameArray[i][j],end="")
				print("\n",end="")
			#print(gameArray)
			print("Press 'q' to quit the game")	
	def drawRawboard(self,state):
		#gg = bo.gameBoard(1,1)
		printArray = [[0 for x in range(state.width*4+4)] for y in range(state.height*2+4)]
		for i in range(1,state.height*2+1):#39 23 
			for j in range(1,state.width*4+1):
				printArray[i][j]=state.posArray[int((i+1)/2)][int((j+3)/4)]
		for i in range(1,state.height*2+1):#39
			for j in range(1,state.width*4+1):#77
				if(printArray[i][j]=="X"):
					print(colored(printArray[i][j],"blue"),end="")
				elif(printArray[i][j]=="E"):
					print(colored(printArray[i][j],"red"),end="")
				elif(printArray[i][j]=="/"):
					print(colored(printArray[i][j],"green"),end="")
				else:
					print(printArray[i][j],end="")
			print("\n",end="")
		#print(gameArray)
		print("Press 'q' to quit the game")
		print("Score      :",state.score,"\t\t\t\t\t\t","Lives left :",state.lives)

		return
	"""def nextstep(self,posArray):
		self.bo.drawposboard(posArray)
		self.pl.drawposPlayer(posArray)
		self.br.drawposBricks(posArray)
		self.en.drawposEnemy(posArray)
		self.posbo.drawBomb(posArray)"""

