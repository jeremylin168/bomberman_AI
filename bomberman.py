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
lives = 1
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

record_mod = 0
testcase = 20

if	len(sys.argv)==1:
	ai= False
elif sys.argv[1] == "1":
	ai = True
else:
	ai = False

try:
	payload = sys.argv[2]
expect:
	payload = ""
fp = open("./record_"+payload+".txt",'w')
fp.write("width: %d, height: %d, enemyNum: %d, bricknum: %d, mxlevel: %d, explosion power: %d, timer: %d, expect depth: %d, Smart enemy: %d\n" % (width,height,enemyNum,bricknum,mxlevel,explosion_power,timer,expect_depth,Smartenemy)	)

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

case=1
die = False

while(1):
	loop +=1
	os.system("cls") #if don't want to flush window, => os.system("")
	print(loop)
	if(uu.lives<=0):
		print("Game Over")
		print("Score: ",uu.score)
		#sys.exit(1)
	elif(uu.enemyNum == 0 and level <= mxlevel):
		level+=1
		if(level>mxlevel):
			print("You WIN")
			print("Score: ",uu.score)
			#sys.exit(1)
		if record_mod !=0:
			uu.gameinit(uu.height+2, uu.width+2,lives,bricknum+(level-1)*5,enemyNum+(level-1)*2,uu.score,MovePattern=Smartenemy)
	else:
		print("Level      :",level)
	if record_mod ==0:
		print("record mode active")
		print("The "+str(case)+"-th case")
		if(uu.lives<=0):
			fp.write("\ncase: "+str(case)+"\n")
			fp.write("loop: "+str(loop)+'\n')
			fp.write("Game Over\n")
			fp.write("Score: "+str(uu.score)+"\n")
			die = True		
		elif(loop >150):
			fp.write("\ncase: "+str(case)+"\n")
			fp.write("loop: "+str(loop)+'\n')
			fp.write("Wait too long\n")
			fp.write("Score: "+str(uu.score)+"\n")
			die = True
		elif(uu.enemyNum == 0):
			if(level>mxlevel):
				fp.write("\ncase: "+str(case)+"\n")
				fp.write("loop: "+str(loop)+'\n')
				fp.write("You WIN\n")
				fp.write("Score: "+str(uu.score)+"\n")
				die = True			

		if die:
			case+=1
			if case > testcase:
				break
			die=False
			loop=0
			level = 1
			del uu
			uu = Gamestate(g)
			uu.gameinit(height, width,lives,bricknum,enemyNum,MovePattern=Smartenemy)
		

	

	g.drawRawboard(uu)
	
	if ai:
		print("AI")
		state = Gamestate( uu.g ,uu.posArray, uu.enemyPos, uu.enemyNum, uu.bomPos, uu.playerPos, uu.brickPos, uu.bricknum, uu.height, uu.width, uu.score, uu.lives, uu.MovePattern,uu.bombscore,uu.enemyscore)
		#different AI agent
		inp = AI_agent.expectMax(uu) 
		#inp = AI_agent.getAction(uu)
		#inp = AI_agent.alpabetaAgent(uu)
		del state
		#input("") #if needed, this can plause program
		uu.getnextstep(0, inp,1)
		#time.sleep(1)
	else:
		inp = input_char()
		if(inp == 'q'):
			sys.exit(0)
		li=uu.getLegalActions(0)
		if inp in li:
			uu.getnextstep(0, inp,1)

fp.close()


	



