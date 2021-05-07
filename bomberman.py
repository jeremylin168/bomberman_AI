from __future__ import print_function
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
from gamestate import Gamestate

getch = GetchUnix(1)

def alarmHandler(signum, frame):
    raise AlarmException

def input_char():
	return getch()

width = 9
height = 9
enemyNum = 3
bricknum = 10
score = 0
lives = 3
explosion_power=2


bo = Board(height,width)
br= Brick(height,width)
pl = Player(height,width,score,lives)
en = Enemy(height, width,enemyNum,pl)
bom = Bomb(height,width,pl,en)
posbo = posBomb(height, width,explosion_power)
g=Gameplay(height,width,bo,br,pl,en,bom,posbo)


uu = Gamestate(g)
uu.gameinit(height, width,lives,bricknum,enemyNum)

level = 1

while(1):
	os.system("cls")
	if(uu.lives<=0):
		print("Game Over")
		print("Score:",uu.score)
		sys.exit(1)
		
	if(uu.enemyNum == 0 and level <= 3):
		level+=1
		if(level>3):
			print("You WIN")
			print("Score:",uu.score)
			sys.exit(1)
		uu.gameinit(uu.height+2, uu.width+2,lives,bricknum+(level-1)*5,enemyNum+(level-1)*2,uu.score)
	print("Level      :",level)

	

	g.drawRawboard(uu)
	inp = input_char()
	if(inp == 'q'):
		sys.exit(0)
	li=uu.getLegalActions(0)
	if inp =='b':
		uu.getnextstep(0, 'b',1)
	elif inp in li:
		uu.getnextstep(0, inp,1)

