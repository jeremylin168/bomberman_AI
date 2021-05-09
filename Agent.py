from gamestate import Gamestate
import random

class agent():
    def __init__(self,depth=2):
        self.depth = 2
    def evaluationFunction(self,currentGameState):
        return currentGameState.getscore()

    def getAction(self, gameState):
        def tree(depth,agent,state):
            if(state.isLose()):
                return self.evaluationFunction(state)#+depth
            if(state.isWin()):
                return self.evaluationFunction(state)#-depth
            if(depth>=self.depth):
                return self.evaluationFunction(state)
            legalmove=state.getLegalActions(agent)
            if (agent>=state.getenemyNum()):
                nagent=0
                depth+=1
            else:
                nagent=agent+1
            scores=[]
            for mv in legalmove:
                mvscore=tree(depth,nagent,state.getnextstep(agent,mv))
                if mvscore!=None:
                    scores.append(mvscore)
            if len(scores)<=0:
                return None
            if(depth==0 and agent==0):
                print(legalmove)
                print(scores)
                bestScore=max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return legalmove[chosenIndex]
            elif(agent==0):
                return max(scores)#-1
            else:
                return min(scores)
        
        nextmv = tree(0,0,gameState)
        return nextmv
    def alpabetaAgent(self, gameState):
        def tree(depth,agent,state,alpha,beta):
            if(state.isLose()):
                return self.evaluationFunction(state)
            if(state.isWin()):
                return self.evaluationFunction(state)
            if(depth>=self.depth):
                return self.evaluationFunction(state)
            legalmove=state.getLegalActions(agent)
            if (agent>=state.getenemyNum()):
                nagent=0
                depth+=1
            else:
                nagent=agent+1
            if agent==0:
                v=-999999
            else:
                v=999999
            bestScore=None
            bestmv=[]
            bs=[]
            for mv in legalmove:
                mvscore= tree(depth,nagent,state.getnextstep(agent,mv),alpha,beta)
                if mvscore!=None:
                    if(agent==0):
                        if(depth==0):
                            if mvscore == v:
                                bestmv.append(mv)
                                bs.append(mvscore)
                            elif mvscore > v:
                                bestmv=[mv]
                                bs=[mvscore]
                        v=max(v,mvscore)
                        bestScore=v
                        if v > beta:
                            break
                        alpha=max(alpha,v)
                    else:
                        v=min(v,mvscore)
                        bestScore=v
                        if v< alpha:
                            break
                        beta=min(beta,v)
            if bestScore==None:
                return None
            if(depth==0 and agent==0):
                print(mv)
                print(bs)
                return random.choice(bestmv)
            elif(agent==0):
                return bestScore
            else:
                return bestScore
        nextmv = tree(0,0,gameState,-99999,99999)
        return nextmv
    def expectMax(self,gameState):
        def tree(depth,agent,state):
            """if(state.isLose()):
                return self.evaluationFunction(state)
            if(state.isWin()):
                return self.evaluationFunction(state)
            """
            if(depth>=self.depth):
                return self.evaluationFunction(state)
            legalmove=state.getLegalActions(agent)
            if (agent>=state.getenemyNum()):
                nagent=0
                depth+=1
            else:
                nagent=agent+1
            scores=[]
            for mv in legalmove:
                mvscore=tree(depth,nagent,state.getnextstep(agent,mv))
                if mvscore!=None:
                    scores.append(mvscore)
            if len(scores)<=0:
                return None
            if(depth==0 and agent==0):
                print(legalmove)
                print(scores)
                bestScore=max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return legalmove[chosenIndex]
            elif(agent==0):
                return max(scores)
            else:
                bestScore=0
                for i in scores:
                    bestScore+=i
                return bestScore/len(scores)
        nextmv = tree(0,0,gameState)
        return nextmv
