from gameClasses import *
import console as _console
from statusWindow import *
from random import *

START='start'
INGAME='ingame'
FINISH='finish'
val = 1

ROLL,SELL,BUILD,MORTAGE,UNMORTAGE,TRADE,END = "roll","sell","build","mortage","unmortage","trade","end"
allComands=[ROLL,SELL,BUILD,MORTAGE,UNMORTAGE,TRADE,END] # player can sell its properties back to bank..

BUY,AUCTION = "buy","auction"
purchaseCmds = [BUY,AUCTION]

class monoGame():
    commands=allComands
    gameState=START
    
    def __init__(self,board,num_players=2,players=[]):
        self.players=players
        self.board=board
        self.console=_console.console()
        self.statusWindow=statusWindow()
        self.default_money = 1500
        self.current_player = 0 # index of the current player
        self.winner = -1
        self.num_players = num_players
        
    def do_move(self,diceSum):
        player=self.players[self.current_player]        
        prevBlock=self.board.blocks[player.location]
        prevBlock.player = NOPLAYER
        targetMove=(player.location+diceSum)%len(self.board.blocks)
        currBlock=self.board.blocks[targetMove]
        player.landOn(currBlock,targetMove)
        actions=currBlock.getActions()
        if(len(actions)==1):
            for key in actions.keys():
                actions[key](self.console)
        else:
            self.console.chooseFromOptions(actions)
    
    
    def start(self):
        self.console.start()
        i = 0
        while i < self.num_players:
            name_player = self.console.get_player_name()
            new_player1 = player(name_player,self.default_money)
            self.players.append(new_player1)
            i += 1
            
        init_state(self.players,self.board,self.console)
                              
        self.current_player = randrange(len(self.players))
        self.console.display("{} takes the first turn".format(self.players[self.current_player].name))
        
        while not self.is_complete():
            
            self.next_turn()
            
        if not self.winner == -1:
            self.console.show_winner(self.winner)
            
            

    def next_turn(self):
        # main game logic
        self.commands=allComands
        self.rolled_already = False
        self.end_turn = False
        self.curr_player_name = self.players[self.current_player].name
        self.console.display("{} takes the turn!".format(self.curr_player_name))
        while not self.end_turn:
            cmd = self.console.prompt_commands(self.commands)
            self.players[self.current_player].printPlayer()
            if cmd == "roll":
                self.do_roll()
            elif cmd == "end":
                self.do_end_turn()                
            elif cmd == "build":    
                pass
            elif cmd == "mortage":    
                pass
            elif cmd == "unmortage":    
                pass
            elif cmd == "trade":    
                pass
            else:
                self.console.display("Invalid command input!")     
        #complete the turn than change to next player
        self.current_player = self.next_player(self.current_player)
        pass
    

    def do_roll(self):
        if not self.rolled_already:
                    
                    dice = self.board.roll_dice()
                    self.console.display("Dice rolled {}".format(dice))
                    self.rolled_already = True
                    # movement around the board and actions on landing
                    dice_sum=dice[0]+dice[1]
                    #self.do_move(dice_sum)    #commenting for testing!
                    self.do_move(val)      #testing
                    self.rolled_already = False  #testing
                    
        else:
                    self.console.display("You have already rolled the dice")
                    
                                
    def do_end_turn(self):
        if not self.rolled_already:
                    self.console.display("You first have to roll the dice")
        else:
                    self.end_turn = True
                    self.console.display("{} ends his turn".format(self.curr_player_name))
    
    
    
    def next_player(self, index):        
        return (index+1)%len(self.players)
    
    
    def is_complete(self):  # check if anyone wins, 
        c = 0
        w = 0
        for p in self.players :
            if not p.is_bankrupt():
                c+=1
                w = p
        if c == 1:
            self.winner = w
            self.gameState=FINISH
            return True
        elif c == 0:
            self.gameState=FINISH
            return True
        self.gameState=INGAME
        return False    
