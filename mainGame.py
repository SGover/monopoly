from gameClasses import player
import console as _console
from statusWindow import *
from random import *

START='start'
INGAME='ingame'
FINISH='finish'
ROLL,BUY,BUILD,MORTAGE,UNMORTAGE,TRADE,END = "roll","buy","build","mortage","unmortage","trade","end"
allComands=[ROLL,BUY,BUILD,MORTAGE,UNMORTAGE,TRADE,END]
class monoGame():
    commands=allComands
    gameState=START
    curr_turn=0
    def __init__(self,board,num_players=2,players=[]):
        self.players=players
        self.board=board
        self.console=_console.console()
        self.statusWindow=statusWindow()
        self.default_money = 1500
        self.current_player = 0 # index of the current player
        self.winner = -1;
        self.num_players = num_players
        
#     def do_move(diceSum):
#         player=self.players[curr_turn]        
#         currBlock=self.board[(player.location+diceSum)%(len(board)-1)]
#         currBlock.landOn(player)
#         actions=currBlock.getActions()
#         if(len(actions)==1):
#             actions[0]()
#         else:
#             self.chooseFromOptions(actions)
#         self.curr_turn=(self.curr_turn+1)%(len(players)-1)
    
    def start(self):
        self.console.start()
        
        name_player = self.console.get_player_name()
        new_player1 = player(name_player,self.default_money)
        self.players.append(new_player1)
        
        name_player = self.console.get_player_name()
        new_player2 = player(name_player,self.default_money)
        self.players.append(new_player2)
        
        self.current_player = randrange(len(self.players))
        self.console.display("{} takes the first turn".format(self.players[self.current_player].name))
        
        while not self.is_complete():
            self.commands=allComands
            self.next_turn()
            
        if not winner == -1:
            self.console.show_winner(winner)
            
            

    def next_turn(self):
        # main game logic
        self.rolled_already = False
        self.end_turn = False
        self.curr_player_name = self.players[self.current_player].name
        self.console.display(self.curr_player_name)
        while not self.end_turn:
            cmd = self.console.prompt_commands(self.commands)
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
                    self.commands.remove(ROLL)
                    dice = self.board.roll_dice()
                    self.console.display("Dice rolled {}".format(dice))
                    self.rolled_already = True
                    # movement around the board and actions on landing
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
            winner = w
            gameState=FINISH
            return True
        elif c == 0:
            gameState=FINISH
            return True
        gameState=INGAME
        return False    
