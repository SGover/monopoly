from gameClasses import *
START='start'
INGAME='ingame'
FINISH='finish'
class monoGame():
    gameState=START
    curr_turn=0
    def __init__(self,players,board,surpriseDeck,chanceDeck):
        self.players=players
        self.board=board
        self.surpriseDeck=surpriseDeck
        self.chanceDeck=chanceDeck
    def doMove(diceSum):
        player=self.players[curr_turn]        
        currBlock=self.board[(player.location+diceSum)%(len(board)-1)]
        currBlock.landOn(player)
        actions=currBlock.getActions()
        if(len(actions)==1):
            actions[0]()
        else:
            self.chooseFromOptions(actions)
        self.curr_turn=(self.curr_turn+1)%(len(players)-1)
    
        
