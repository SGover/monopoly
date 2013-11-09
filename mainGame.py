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
        self.statusWin=statusWindow()
        self.default_money = 1500
        self.current_player_index = 0 # index of the current player
        self.winner = -1
        self.num_players = num_players
        
    
    
    def start(self):
        self.console.start()
        i = 0
        while i < self.num_players:
            name_player = self.console.get_player_name()
            new_player1 = player(name_player,self.default_money)
            self.players.append(new_player1)
            i += 1
            
        init_state(self.players,self.board,self.console)
        self.statusWin.start(self.players);                      
        self.current_player_index = randrange(len(self.players))
        self.curr_player=self.players[self.current_player_index]
        self.console.display("{} takes the first turn".format(self.curr_player.name))
        
        while not self.is_complete():
            
            self.next_turn()
            
        if not self.winner == -1:
            self.console.show_winner(self.winner)
            
    def next_turn(self):
        # main game logic
        self.init_turn()#intiate the turn varibals
        while not self.end_turn:                        
            self.curr_player.printPlayer()            
            if self.curr_player.inJail and not self.jail_try and not self.rolled_already:
                self.console.display(self.curr_player+" is in Jail")
                self.do_in_jail_commands()                
            else:
                self.do_all_commands()
        #complete the turn than change to next player
        self.change_next_player()

    def init_turn(self):
        self.commands=allComands
        self.rolled_already = False
        self.end_turn = False
        self.jail_try=False
        self.curr_player_name = self.players[self.current_player_index].name
        self.console.display("{} takes the turn!".format(self.curr_player_name))    

    def do_in_jail_commands(self):
        cmd=self.console.propmpt_commands(["break","pay","end"])
        self.curr_player.inc_jail_count()
        if cmd == "break":
            self.try_jail_break()
        elif cmd=="pay":
            self.pay_jail_fine()
        elif cmd == "end":
            self.do_end_turn()                
        else:
            self.console.display("Invalid command input!")     
            
    def do_all_commands(self):
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
    
    def try_jail_break(self):
        if not self.jail_try:
            dice = self.board.roll_dice()
            self.console.display("Dice rolled {}".format(dice))
            self.jail_try=True        
            dice_sum=dice[0]+dice[1]
            self.rolled_allready=True
            if dice[0]==dice[1]:
                self.console.display("Double! you are out of jail")
                self.do_move(dice_sum)            
            else:
                self.console.display("no Double. try again next time")
        else:
            self.console.display("Already tried to break out of jail")
    
    def pay_jail_fine(self):
        player=self.curr_player
        player.inJail=False
        player.money-=100
        self.console.display(player.name+" paid a 100$ fine for getting out of jail")
        self.do_all_commands()
    
    def do_roll(self):
        if not self.rolled_already:
                    
                    dice = self.board.roll_dice()
                    self.console.display("Dice rolled {}".format(dice))
                    self.rolled_already = True
                    # movement around the board and actions on landing
                    dice_sum=dice[0]+dice[1]
                    #self.do_move(dice_sum)    
                    self.do_move(val)
                    self.rolled_already = False
        else:
                    self.console.display("You have already rolled the dice")
    
    def do_end_turn(self):
        if not self.rolled_already:
                    self.console.display("You first have to roll the dice")
        else:
                    self.end_turn = True
                    self.console.display("{} ends his turn".format(self.curr_player_name))
                    
    def do_move(self,diceSum):
        player=self.players[self.current_player_index]        
        prevBlock=self.board.blocks[player.location]
        prevBlock.player = NOPLAYER
        targetMove=(player.location+diceSum)%len(self.board.blocks)
        currBlock=self.board.blocks[targetMove]
        player.landOn(currBlock,targetMove)
        actions=currBlock.getActions()
        if(len(actions)==1):
            for key in actions.keys():
                actions[key]()
        else:
            self.console.chooseFromOptions(actions)
                                        
    def change_next_player(self):
        self.current_player_index = (self.current_player_index+1)%len(self.players)
        self.curr_player=self.players[self.current_player_index]
    
    
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
