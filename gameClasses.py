from random import shuffle as reorder


#CONSTANT VALUES
JAIL_FEE=100


#typer and colors
UTILITY = "UTILTIES"
RW_STATION = "RAILWAY STATIONS"
INDIGO = "INDIGO COLOR" # or whatever this color is #171363
WHITE = "LIGHTBLUE COLOR"
PURPLE = "PURPLE COLOR"
ORANGE = "ORANGE COLOR"
RED = "RED COLOR"
YELLOW = "YELLOW COLOR"
GREEN = "GREEN COLOR"
BLUE = "BLUE COLOR"
NOPLAYER = "I'm no body"
JAIL="JAIL"
#this class represents a deck of cards like surprize cards or punishment cards
board=None
players=[]
console = -1
###########################################################################
#dont forget to set this before each game
def init_state(newPlayers,newBoard,newConsole):
    global players,board,console
    players,board,console=newPlayers,newBoard,newConsole
########################################################################
def getAmount(aType):
    counter=0
    assetBlock1=assetBlock('test',1,1, 1,1,[])
    utilBlock1=utilBlock('name',1,1,1)
    for block in board.blocks:
        if type(block)==type(assetBlock1) or type(block)==type(utilBlock1):
            if block.color==aType:
                counter+=1
    return counter            
    
def getPlayerFromName(name):
    for player in players:
        if player.name==name:
            return player
    return None    
###################
# Cards Section
###################

class deck():
    def __init__(self,cards,name):
        self.name=name
        self.cards=cards
        self.discard=[]
        self.shuffle()
    def shuffle(self):
        """Rearranging cards and shuffling"""
        reorder(self.cards)     #importing shuffle as reorder
        
    def getCard(self):      #getting a card from the deck        
        if len(self.cards)==0:            
            self.cards=self.discard
            self.shuffle()
            self.discard=[]            
        card = self.cards.pop()
        self.discard.append(card)
        return card
    
    def addCard(self, card):
        self.cards.append(card)
        
        
class card():
    '''this class represent a card
       a card have a titile,text variables and applyToPlayer function
    '''
    def __init__(self,title,text):
        self.title=title
        self.text=text
        
    def applyToPlayer(self,player):
        pass

class changeMoneyCard(card):
    '''this card can incrase or decrease the player money
       also it could depened on all the players(commune)
    '''
    def __init__(self,title,text,amount,commune=False):
        card.__init__(self,title,text)
        self.commune=commune
        self.amount=amount # amount of money to add or subtract from player(positive value will add and negetive will subtract)
        #change from fork
    def applyToPlayer(self,player):
        if self.commune:        
            for p in players:
                if p.name!=player.name:
                    player.money+=self.amount
                    p.money-=self.amount
                    if self.amount>0:
                        console.display(player.name+" got "+str(self.amount)+" from "+p.name)
                    else:
                        console.display(player.name+" paid $"+str(-1*self.amount)+" to "+p.name)
        else:            
            player.money+=self.amount
            if self.amount>0:
                console.display(player.name+" got $"+str(self.amount)+" from bank")
            else:
                console.display(player.name+" paid $"+str(-1*self.amount)+" to bank")
class advanceToCard(card):
    def __init__(self,title,text,target,applyGo=True):
        card.__init__(self,title,text)
        self.targetName=target
        self.applyGo=applyGo
        if target==JAIL or target=='GO!':
            self.applyGo=False
    
    def applyToPlayer(self,player):
        loc=player.location        
        while board.blocks[loc].name!=self.targetName:            
            loc=(loc+1)%len(board.blocks)
            if self.applyGo:
                if loc==0:
                    player.money+=200
                    console.display("player went through start got 200")        
        player.landOn(board.blocks[loc],loc)
        if self.targetName==JAIL:
            player.inJail=True
            player.jailCounter=0
        actions=board.blocks[loc].getActions()
        if(len(actions)==1):
            for key in actions.keys():
                actions[key]()
        else:
            console.chooseFromOptions(actions)                


class moveToNearestCard(card):
    def __init__(self,title,text,targetColor,applyGo=True):
        card.__init__(self,title,text)
        self.color=targetColor 
    def applyToPlayer(self,player):
        loc=player.location
        
        while board.blocks[loc].color!=self.color:            
            loc=(loc+1)%len(board.blocks)
            if self.applyGo:
                if loc==0:
                    player.money+=200
                    console.display("player went through start got $200")        
        player.landOn(board.blocks[loc],loc)
        actions=board.blocks[loc].getActions()
        if(len(actions)==1):
            for key in actions.keys():
                actions[key]()
        else:
            console.chooseFromOptions(actions)

###################
# Blocks Section
###################


#represents a block on the board that containing an asset
#this block can belong to a player
class block():
    def __init__(self, name, position):
        self.name = name
        self.position = position
    def pass_(self):
        pass
    def getActions(self):
        pass
    
class utilBlock(block):         #utilities and railway stations
    def __init__(self, name, uType, price, position):
        block.__init__(self, name, position)
        self.color = uType    #utiltiy or railway station !see top at the file
        self.price = price
        self.owner=NOPLAYER
        self.mortaged=False
    def __str__(self):
        return self.name + " of " + self.color
    
    def __repr__(self):
        return self.name + " of " + self.color
     
    
    def pay_rent(self):
        #rent in the case of railway station
        if self.color==RW_STATION:
            player=getPlayerFromName(self.owner)
            num=player.how_many(RW_STATION)
            rent=25*(2**(num-1))
        #rent in the case of utility
        else:            
            player=getPlayerFromName(self.owner)
            diceRoll=self.player.getLatestRoll()
            num=player.how_many(UTILITY)
            if num==1:
                rent=4*diceRoll
            elif num==2:
                rent=10*diceRoll
        console.display(self.player.name+" pay rent of "+str(rent)+" to "+self.owner)
        self.player.pay(rent)
        getPlayerFromName(self.owner).money+=rent
    def purchase(self):
        self.player.buy(self)
        
    def getActions(self):
        if self.owner==NOPLAYER :
            return {"buy":self.purchase,"pass":self.pass_}            
        elif self.owner==self.player.name or self.owner=='bank':                        
            return {"pass":self.pass_}
        else:
            return {"payrent":self.pay_rent}                            
    def mortage(self):
        if not self.mortaged and not self.owner==NOPLAYER:
            player = getPlayerFromName(self.owner)
            player.money+=self.price//2
            self.mortaged=True
            console.display("{} mortaged {} for ${}".format(player.name,self.name,str((self.price//2))))
    def unmortage(self,player):
        if self.mortaged and player.name==self.owner:
            player.money-=(self.price//2)*1.1
            self.mortaged=False
            console.display("{} unmortaged {} for ${}".format(player.name,self.name,str(round((self.price//2)*1.1,2))))
        

class assetBlock(block):
    def __init__(self,name,color,price, position,house_price,rent_list):
        block.__init__(self,name, position)
        self.house_price=house_price
        self.rent_list=rent_list
        self.color=color
        self.price=price
        self.houses=0
        self.hotel=False
        self.owner=NOPLAYER
        self.mortaged=False
    def __str__(self):
        return self.name + " of " + self.color
    
    def __repr__(self):
        return self.name + " of " + self.color
    
    def pay_rent(self):
        index=self.houses
        if self.hotel:
            index+=1
        rent=self.rent_list[index]        
        self.player.pay(rent)
        getPlayerFromName(self.owner).money+=rent
        console.display(self.player.name+" paid rent of "+str(rent)+" to "+self.owner)
    
    def getActions(self):
        if self.owner==NOPLAYER :
            return {"buy":self.purchase,"pass":self.pass_}            #auction???
        elif self.owner==self.player.name or self.owner=='bank':                        
            return {"pass":self.pass_}
        else:
            return {"payrent":self.pay_rent}                        
    
    def purchase(self):      
        self.player.buy(self)
        
    def mortage(self):
        if not self.mortaged and not self.owner==NOPLAYER:
            player = getPlayerFromName(self.owner)
            player.money+=self.price//2
            self.mortaged=True
            console.display("{} mortaged {} for ${}".format(player.name,self.name,str((self.price//2))))
            
    def unmortage(self,player):
        if self.mortaged and player.name==self.owner:
            player.money-=(self.price//2)*1.1
            self.mortaged=False
            console.display("{} unmortaged {} for ${}".format(player.name,self.name,str(round((self.price//2)*1.1,2))))
    


#represent a block on the board that landing on means u need to pull a card from some deck        
class cardBlock():
    def __init__(self, name,deck, position):
        block.__init__(self, name, position)
        self.deck=deck
        self.color = -1
    def getCard(self):
        card=self.deck.getCard()
        console.display(self.player.name+" got Card : "+card.title+" , "+card.text)
        card.applyToPlayer(self.player)
    def getActions(self):
        return {"getcard":self.getCard}
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class moneyBlock():                 #Go , tax , luxury tax etc blocks which onLand
    def __init__(self, name, money, position):      # action is just adding or subtracting money
        block.__init__(self, name, position)
        self.deck=deck
        self.money = money
        self.color = -1
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def use(self):
        if not self.player==NOPLAYER:
            self.player.money+=self.money
            if self.money > 0:
                console.display("{} got ${} salary from {}".format(self.player.name,self.money,self.name))
            elif self.money < 0:
                console.display("{} paid ${} {}".format(self.player.name,self.money*-1,self.name))
    def getActions(self):
        return {"changemoney : "+str(self.money):self.use}
    
    
class goToJailBlock(block):
    def __init__(self, position, name="'Go TO Jail'"):
        block.__init__(self, name, position)
        self.color = -1

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def goToJail(self):
        console.display(self.player.name+ ", go to jail!")
        if not self.player==NOPLAYER:
            self.player.goToJail()
    def getActions(self):
        return {'Go To jail':self.goToJail}
               

###############
#trader
##############
class Trader():
    def __init__(self,player1,player2):
        self.player1=player1
        self.player2=player2
        self.player1_blocks=[]
        self.player1_money=0
        self.player2_blocks=[]
        self.player2_money=0
    def add_asset_1(self,asset):
        self.player1_blocks.append(asset)
    def add_asset_2(self,asset):
        self.player2_blocks.append(asset)
    def remove_asset_1(self,asset):
        self.player1_blocks.remove(asset)
    def remove_asset_2(self,asset):
        self.player2_blocks.remove(asset)
    def set_money1(self,ammount):
        if self.player1.money>=ammount:
            self.player1_money=ammount
    def set_money2(self,ammount):
        if self.player1.money>=ammount:
            self.player1_money=ammount            
    def make_trade(self):
        self.player2.money-=self.player2_money
        self.player2.money+=self.player1_money
        console.display("{} paid ${} and got ${} ".format(self.player2.name,self.player2_money,self.player1_money))
        for asset in self.player1_blocks:
            self.player1.remove_asset(asset)
            self.player2.add_asset(asset)
        self.player1.money-=self.player1_money
        self.player1.money+=self.player2_money
        console.display("{} paid ${} and got ${} ".format(self.player1.name,self.player1_money,self.player2_money))
        for asset in self.player2_blocks:
            self.player1.remove_asset(asset)
            self.player2.add_asset(asset)
   
    
##################
# Player Section
##################


#represent a player
#player attributes : name,money,location,assets        
class player():
    
    def __init__(self,name,money):
        self.name=name
        self.money=money
        self.assets={}
        self.location=0
        self.getOutOfJailCard=False
        self.inJail=False
        self.token_index = -1
        
    def pay(self,ammount):
        self.money-=ammount
        
    def buy(self,assetBlock):
        if assetBlock.owner==NOPLAYER :
            if self.money >= assetBlock.price:
                self.money-=assetBlock.price
                assetBlock.owner=self.name
                if(assetBlock.color in self.assets):
                    self.assets[assetBlock.color].append(assetBlock)
                else:
                    self.assets[assetBlock.color]=[assetBlock]
                console.display("{} bought the {} for ${}".format(self.name,str(assetBlock),assetBlock.price))
            else:    
                console.display("{} don't have ${} to buy {}".format(self.name,assetBlock.price,str(assetBlock)))
        else:
            console.display("this property already have an owner")
                
    def sell_house(self,block):
        if block.houses>0:
            self.money+=block.house_price//2
            block.houses-=1
            console.display("{} sold a house on {} for ${} \n now he have {} houses on this property".format(self.name,block.name,str(block.house_price//2),block.houses))
    def sell_hotel(self,block):
        if block.hotel:
            self.money+=block.house_price//2
            block.hotel=False
            console.display("{} sold the hotel on {} for ${}  ".format(self.name,block.name,str(block.house_price//2)))
    def printPlayer(self):
        console.display(self.name+" has money: "+str(self.money)+" and assets : "+str(self.assets))
        
    def landOn(self,block,location):        
        self.location=location
        block.player=self
        console.display(self.name+" lands on "+ str(block))
        
    def getHousesAndHotels(self):
        houses=0
        hotels=0
        for group in self.assets.values():
            for asset in group:
                houses+=asset.houses
                if asset.hotel==True:
                    hotels+=1
        return (houses,hotels)    
    def inc_jail_count(self):
        self.jailCounter+=1
        if self.jailCounter>=2:
            self.inJail=False
            console.display("last turn in jail next turn you are a free man")
    def goToJail(self):
        self.inJail=True
        self.jailCounter=0
        while board.blocks[self.location].name!=JAIL:            
            self.location=(self.location+1)%len(board.blocks)
    def how_many(self,aType):       
        count=0
        if aType in self.assets:   
            for block in self.assets[aType]:
                if not block.mortaged:
                    count+=1
            return count
        else:
            return 0
        
    #buying houses function
    def buy_house(self,block):
        if block.owner==self.name:
            if block.color!=UTILITY and block.color!=RW_STATION:                
                if self.how_many(block.color)==getAmount(block.color):
                    can_build=True
                    for street in self.assets[block.color]:
                        if street.houses<block.houses:
                            can_build=False
                    if can_build:
                        if block.houses<4:
                                block.houses+=1
                                self.pay(block.house_price)
                                console.display(self.name+" bought an house for $"+str(block.house_price)+" on "+block.name)
                                console.display(self.name+" have "+str(block.houses)+" houses on this property")
                        else:
                                console.display("u cant build more than 4 houses on property")                                            
                    else:
                        console.display("u cant build on this block until u developed all the properties on this section")
                            
                else:
                    console.display("u cant build until u have all properties on this block")
        else:
            console.display("u cant build this block don't belong to u")
    #buying hotel function                                
    def buy_hotel(self,block):
        if block.owner==self.name:
            if block.color!=UTILITY and block.color!=RW_STATION:
                
                if self.how_many(block.color)==getAmount(block.color):
                    can_build=True
                    for street in self.assets[block.color]:
                        if street.houses<block.houses:
                            can_build=False
                    if can_build:
                        if block.houses==4:
                                block.hotel=True
                                self.pay(block.house_price)
                                console.display(self.name+" bought an hotel for $"+str(block.house_price)+" on "+block.name)                                
                        else:
                                console.display("u need 4 houses to build an hotel")                                                
                    else:
                        console.display("u cant build on this block until u developed all the properties on this section")
                            
                else:
                    console.display("u cant build until u have all properties on this block")
        else:
            console.display("u cant build this block don't belong to u")
        
    def get_build_assets(self):
        return_list=[]
        for section in self.assets.keys():
            if section!=UTILITY and section!=RW_STATION:                
                if self.how_many(self.assets[section][0].color)==getAmount(self.assets[section][0].color):
                    return_list.append(section)
        return return_list
    def is_bankrupt(self):
        if self.money<=0:
            return True
        return False
    def add_asset(self,asset):
        if(asset.color in self.assets):
            self.assets[asset.color].append(asset)
        else:
            self.assets[asset.color]=[asset]
        console.display("{} was added to {} properties under {} group".format(asset.name,self.name,asset.color))
    def remove_asset(self,asset):
        console.display("{} was removed from {} properties ".format(asset.name,self.name))
        if asset.color in self.assets:
            self.assets[asset.color].remove(asset)
    def updateRoll(self,roll):
        self.latestRoll=roll
    def getLatestRoll(self):
        return self.latestRoll
    def assets_list(self):
        r_list=[]
        for  v in self.assets.values():
            r_list.extend(v)
        return r_list
    def mortage_list(self,condition=True):
        r_list=[]
        for  v in self.assets.values():
            for a in v:
                if a.mortaged==condition:
                    r_list.append(a)
        return r_list
    def house_asset_list(self):
        r_list=[]
        for  v in self.assets.values():
            for a in v:
                if a.houses>0:
                    r_list.append(a)
        return r_list
        
