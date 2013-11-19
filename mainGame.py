from gameClasses import *
import console as _console
from random import randrange
from gui import playerDialog

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
        self.default_money = 1500
        self.current_player_index = 0 # index of the current player
        self.winner = -1
        if num_players == 1:
            self.num_players = 2    #Its not a game of one
        else:    
            self.num_players = num_players
        
    
    
    def start(self):
        
        self.console.start()
        if self.players==[]:
            p_list = playerDialog().show()
            for x in p_list:
                new_player1 = player(x[0],self.default_money)
                new_player1.token_index = x[1]
                self.players.append(new_player1)
        self.board.show(self.players)    
        init_state(self.players,self.board,self.console)
                             
        self.current_player_index = randrange(len(self.players))
        self.curr_player=self.players[self.current_player_index]
        self.console.display("{} takes the first turn".format(self.curr_player.name))
        
        while not self.is_complete():
            self.console.display(" ")
            self.next_turn()
            
        if not self.winner == -1:
            self.console.show_winner(self.winner)
            
    def next_turn(self):
        # main game logic
        self.init_turn()#intiate the turn varibals
        while not self.end_turn:                        
            self.curr_player.printPlayer()
            if self.curr_player.inJail and not self.jail_try and not self.rolled_already:
                self.console.display(self.curr_player.name + " is in Jail")
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
        cmd=self.console.prompt_commands(["break","pay","end"])
        self.curr_player.inc_jail_count()
        if cmd == "break":
            self.try_jail_break()
        elif cmd=="pay":
            self.pay_jail_fine()
        elif cmd == "end":
            self.do_end_turn()                
        else:
            self.console.display("Invalid command input!")     
    def do_build(self):
        build_list=self.curr_player.get_build_assets()
        if(len(build_list)==0):
            self.console.display("nowhere to build houses")
        else:
            build_list.append("pass")
            cmd=''
            while cmd!='pass':
                self.console.display("select section:")
                cmd=self.console.prompt_commands(build_list)
                if cmd in build_list and cmd!='pass':                    
                    section=self.curr_player.assets[cmd]
                    name_list=[]
                    for s in section:
                            name_list.append(s.name)                    
                    name_list.append("pass")
                    while cmd!='pass':
                        self.console.display("select street:")                                        
                        cmd=self.console.prompt_commands_index(name_list)
                        is_street=False
                        if cmd!='pass':
                            for street in section:
                                if street.name==cmd:
                                    is_street=True
                                    if street.houses<4:
                                        self.curr_player.buy_house(street)
                                    else:
                                        self.curr_player.buy_hotel(street)
                                    cmd='pass'
                        elif is_street:
                            self.console.display('no such section plz select from the options')
                elif cmd!='pass':
                    self.console.display('no such section plz select from the options')
                
    def do_sell(self):
        sell_list=self.curr_player.house_asset_list()
        if(len(sell_list)==0):
            self.console.display("no houses to sell")
        else:
            sell_list.append("pass")
            cmd=''
            while cmd!='pass':
                self.console.display("select asset to sell houses:")                                        
                cmd=self.console.prompt_commands_index(sell_list)
                for asset in sell_list:
                    if asset!='pass':
                        if asset.name==cmd.name:
                            cmd='pass'                            
                            self.curr_player.sell_house(asset)
                
                    
            #cond is True for unMortage and False for mortage
    def do_mortage(self,cond):        
        mort_list=self.curr_player.mortage_list(cond)                
        if(len(mort_list)==0):
            if cond:
                self.console.display("no assets to unmortage")
            else:
                self.console.display("no assets to mortage")
        else:
            mort_list.append("pass")
            cmd=''
            if cond:
                self.console.display("select asset to unmortage:")
            else:
                self.console.display("select asset to mortage") 
            cmd=self.console.prompt_commands_index(mort_list)
            mort_list.remove("pass")
            for asset in mort_list:
                if asset==cmd:
                    if cond:
                        asset.unmortage(self.curr_player)
                    else:
                        asset.mortage()
                        

    def do_trade(self):
        trader=Trader(self.players[0],self.players[1])
        cmd=''
        name1=self.players[0].name
        name2=self.players[1].name
        while cmd!='pass' and cmd!='finish':
            cmd = self.console.prompt_commands(['pass','finish',name1,name2])
            if cmd==name1 or cmd==name2:
                cmd2=''
                while cmd2!='pass' and cmd2!='finish':
                    cmd2 = self.console.prompt_commands(['money','asset','pass','finish'])
                    if cmd2 == 'money':
                        ammount=int(input("enter ammount : "))
                        if cmd==name1:
                            trader.set_money1(ammount)
                        else:
                            trader.set_money2(ammount)
                    elif cmd2=='asset':
                        add_remove=self.console.prompt_commands(['add','remove'])
                        if add_remove=='add':
                            if cmd==name1:
                                asset=self.console.prompt_commands_index(self.players[0].assets_list())
                                trader.add_asset_1(asset)
                            else:
                                asset=self.console.prompt_commands_index(self.players[1].assets_list())
                                trader.add_asset_2(asset)
                        else:
                            if cmd==name1 and len(trader.player1_blocks)>0:
                                asset=self.console.prompt_commands_index(trader.player1_blocks)
                                trader.remove_asset_1(asset)
                            elif len(trader.player2_blocks)>0:
                                asset=self.console.prompt_commands_index(trader.player2_blocks)
                                trader.remove_asset_2(asset)
                            else:
                                self.console.display("no assets to remove from trader for "+cmd)
        if cmd=='finish':
            trader.make_trade()
                
    def do_all_commands(self):
        cmd = self.console.prompt_commands(self.commands)
        self.console.display(" ")            
        if cmd == "roll":
            self.do_roll()
        elif cmd == "end":
            self.do_end_turn()                
        elif cmd == "sell":    
            self.do_sell()
        elif cmd == "build":    
            self.do_build()
        elif cmd == "mortage":    
            self.do_mortage(False)
        elif cmd == "unmortage":    
            self.do_mortage(True)
        elif cmd == "trade":    
            self.do_trade()
        elif cmd == "dMode":
            self.do_debug_mode()
        else:
            self.console.display("Invalid command input!")     
    
    def try_jail_break(self):
        if not self.jail_try:
            dice = self.board.roll_dice()
            self.console.display("Dice rolled {}".format(dice))
            self.jail_try=True        
            dice_sum=dice[0]+dice[1]
            
            self.rolled_already = True
            self.curr_player.updateRoll(dice_sum)
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
                    self.curr_player.updateRoll(dice_sum)
                    
                    self.do_move(dice_sum)
                    #self.do_move(2)
                    
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
        if player.location+diceSum>=len(self.board.blocks):
            self.console.display(player.name+" went throught start, got $200")
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
    ################
    #####debug code#############
    #####################
    def do_debug_mode(self):
        cmd=""
        self.console.display("entered debug mode type exit to leave")
        while cmd!="exit":
            cmd=self.console.prompt_commands("debug mode commands")
            if not cmd=='exit':
                v=cmd.split('(')[1].replace(")",'')
                if (v!=''):
                    value =int(v)
                player=cmd.split('(')[0].split('.')[0]
                action=cmd.split('(')[0].split('.')[1]
            if player=='1':                
                self.current_player_index=0
                self.curr_player=self.players[self.current_player_index]
            elif player=='2':
                self.current_player_index=1
                self.curr_player=self.players[self.current_player_index]
            if action=='move':
                self.curr_player.updateRoll(value)
                self.do_move(value)
            elif action=='jail':                
                self.curr_player.goToJail()
            elif action=='money':
                self.curr_player.money+=value
            elif action=='assets':
                if value==-1:
                    print (self.curr_player.assets)
                else:
                    print (str(self.curr_player.how_many(value)))
            elif action=='buy':
                self.board.blocks[value].player=self.curr_player
                self.curr_player.buy(self.board.blocks[value])
            elif action=='house':
                self.curr_player.buy_house(self.board.blocks[value])
            elif action=='hotel':
                self.curr_player.buy_hotel(self.board.blocks[value])
            elif action=='build':
                self.do_build()
            elif action=='sell':
                self.do_sell()
            elif action=='mortage':
                self.do_mortage(False)
            elif action=='unmortage':
                self.do_mortage(True)
            elif action=='trade':
                self.do_trade()
                

            
            


        
