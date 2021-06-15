from __future__ import print_function
import signal,copy,sys,time,select
from random import randint
import random
import os
import sys
from gameplay import *
from getchunix import *
from person import *
from player import *
from bomb import *
from brick import *
from alarmexception import *
from gamestate import Gamestate
from Agent import agent

getch = GetchUnix(1)

def alarmHandler(signum, frame):
    raise AlarmException

def input_char():
	return getch()
#arena size
width = 9
height = 9
#enemy and brick number, they will be generated randomly
enemyNum = 1
bricknum = 10
#score broad
score = 0
lives = 3
mxlevel =1
#bomb setting
explosion_power=2
timer = 3

#AI setting
expect_depth = 4
Smartenemy=0 #smart enemy will gradually come close to player . smart =1 ,random =0

#better expect_depth=3 explosion_power=1 timer = 2 
#or expect_depth=3 explosion_power=2 timer = 2
#or expect_depth=4 explosion_power=2 timer = 3

if	len(sys.argv)==1:
	ai= False
elif sys.argv[1] == "1":
	ai = True
else:
	ai = False


bo = Board(height,width)
br= Brick(height,width)
pl = Player(height,width,score,lives)
en = Enemy(height, width,enemyNum,pl)
bom = Bomb(height,width,pl,en)
posbo = posBomb(height, width,explosion_power,timer)
g=Gameplay(height,width,bo,br,pl,en,bom,posbo)
AI_agent = agent(expect_depth)


uu = Gamestate(g)
uu.gameinit(height, width,lives,bricknum,enemyNum,MovePattern=Smartenemy)

level = 1
loop = 0
while(1):
	loop +=1
	os.system("cls") #if don't want to flush window, => os.system("")
	print(loop)
	if(uu.lives<=0):
		print("Game Over")
		print("Score:",uu.score)
		sys.exit(1)
		
	if(uu.enemyNum == 0 and level <= mxlevel):
		level+=1
		if(level>mxlevel):
			print("You WIN")
			print("Score:",uu.score)
			sys.exit(1)
		uu.gameinit(uu.height+2, uu.width+2,lives,bricknum+(level-1)*5,enemyNum+(level-1)*2,uu.score,MovePattern=Smartenemy)
	print("Level      :",level)

	

	g.drawRawboard(uu)
	
	if ai:
		print("AI")
		#different AI agent
		#inp = AI_agent.expectMax(uu)
		#inp = AI_agent.getAction(uu)
		inp = AI_agent.alpabetaAgent(uu)

		#input("") #if needed, this can plause program
		uu.getnextstep(0, inp,1)
		time.sleep(1)
	else:
		inp = input_char()
		if(inp == 'q'):
			sys.exit(0)
		li=uu.getLegalActions(0)
		if inp in li:
			uu.getnextstep(0, inp,1)
	


	



