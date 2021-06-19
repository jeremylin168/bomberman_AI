from gamestate import Gamestate
import random
import time

class agent():
    def __init__(self,depth=2):
        self.depth = depth
    def evaluationFunction(self,currentGameState):
        return currentGameState.getscore()

    def getAction(self, gameState): #Min_Max
        def tree(depth,agent,state):
            if (agent>=state.getenemyNum()):
                if(agent>state.enemyNum):
                    return self.evaluationFunction(state)
                nagent=0
                ndepth=depth+1
            else:
                nagent=agent+1
                ndepth = depth
            if(state.isLose()):
                return self.evaluationFunction(state)#+depth
            if(state.isWin()):
                return self.evaluationFunction(state)#-depth
            if(depth>=self.depth):
                return self.evaluationFunction(state)
            legalmove=state.getLegalActions(agent)

            scores=[]
            for mv in legalmove:
                u = state.getnextstep(agent,mv)
                mvscore=tree(ndepth,nagent,u)
                del u
                if mvscore!=None:
                    scores.append(mvscore)
            if len(scores)<=0:
                return None
            if(depth==0 and agent==0):
                print(legalmove)
                print(scores)
                bestScore=self.scorechoose(scores, state)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return legalmove[chosenIndex]
            elif(agent==0):
                return self.scorechoose(scores, state)
            else:
                return min(scores)
        
        nextmv = tree(0,0,gameState)
        return nextmv
    def alpabetaAgent(self, gameState):
        def tree(depth,agent,state,alpha,beta):
            if (agent>=state.getenemyNum()):
                if(agent>state.enemyNum):
                    return self.evaluationFunction(state)
                nagent=0
                ndepth=depth+1
            else:
                nagent=agent+1
                ndepth = depth
            if(state.isLose()):
                return self.evaluationFunction(state)
            if(state.isWin()):
                return self.evaluationFunction(state)
            if(depth>=self.depth):
                return self.evaluationFunction(state)
            legalmove=state.getLegalActions(agent)

            if agent==0:
                v=-999999
            else:
                v=999999
            bestScore=None
            bestmv=[]
            bs=[]
            for mv in legalmove:
                u = state.getnextstep(agent,mv)
                mvscore= tree(ndepth,nagent,u,alpha,beta)
                del u
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
                print(bestmv)
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
            if (agent>=state.getenemyNum()):
                if(agent>state.enemyNum):
                    return self.evaluationFunction(state)
                nagent=0
                ndepth=depth+1
            else:
                nagent=agent+1
                ndepth = depth
            if(state.isLose()):
                return self.evaluationFunction(state)
            if(state.isWin()):
                return self.evaluationFunction(state)
            if(depth>=self.depth):
                return self.evaluationFunction(state)
            legalmove=state.getLegalActions(agent)
            scores=[]
            for mv in legalmove:
                u = state.getnextstep(agent,mv)
                mvscore=tree(ndepth,nagent,u)
                del u
                if mvscore!=None:
                    scores.append(mvscore)
            if len(scores)<=0:
                return None
            if(depth==0 and agent==0):
                print(legalmove)
                print(scores)
                bestScore=self.scorechoose(scores, state)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return legalmove[chosenIndex]
            elif(agent==0):
                return self.scorechoose(scores, state)
            else:
                bestScore=0
                for i in scores:
                    bestScore+=i
                return bestScore/len(scores)
        nextmv = tree(0,0,gameState)
        return nextmv
    def scorechoose(self,score,state):
        return max(score)
        
        t = True
        rescore = min(score)
        for x in score:
            if x!=state.score and x!=state.score-200:
                t=False
                rescore = max(x,rescore)
        if t:
            return max(score)
        else:
            return rescore
