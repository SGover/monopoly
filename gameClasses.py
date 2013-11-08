#typer and colors
UTILITY = 0
RW_STATION = 1
INDIGO = 2 # or whatever this color is #171363
WHITE = 3
PURPLE = 4
ORANGE = 5
RED = 6
YELLOW = 7
GREEN = 8
BLUE = 9
NOPLAYER = 10

#this class represents a deck of cards like surprize cards or punishment cards
board=None
players=[]
console=None
###########################################################################
#dont forget to set this before each game
def init_state(newPlayers,newBoard,newConsole):
    global players,board,console
    players,board,console=newPlayers,newBoard,newConsole
########################################################################

    
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
    def shuffle(self):
        pass
    #getting a card from the deck
    def getCard(self):        
        if len(deck)==0:            
            deck=self.discard
            self.shuffle()
            discard=[]            
        card=deck.pop
        discard.append(card)
        return card
    def addCard(self, card):
        self.cards.append(card)
        
        
        
class card():
    def __init__(self,title,text):
        self.title=title
        self.text=text
        
    def applyToPlayer(self,player):
        pass

class changeMoneyCard(card):
    def __init__(self,title,text,amount,commune=False):
        card.__init__(self,title,text)
        self.commune=commune
        self.amount=amount # amount of money to add or subtract from player(positive value will add and negetive will subtract)
		#change from fork
    def applyToPlayer(self,player):
        if self.commune:
            for p in players:
                if p.name!=player.name:
                    player.money+=self.ammount
                    p.money-=self.ammount
        else:            
            player.money+=self.amount
        
class advanceToCard(card):
    def __init__(self,title,text,target,applyGo=True):
        card.__init__(self,title,text)
        self.targetName=target
        self.applyGo=applyGo
    def applyToPlayer(self,player):
        loc=player.location
        while board.blocks[loc].name!=self.targetName:            
            loc=(loc+1)%len(board.blocks)
            if applyGo:
                if loc==0:
                    player.money+=200
        player.landOn(board.blocks[loc])
                


class moveToNearestCard(card):
    def __init__(self,title,text,targetColor,applyGo=True):
        card.__init__(self,title,text)
        self.color=targetColor 
    def applyToPlayer(self,player):
        loc=player.location
        while board.blocks[loc].color!=self.color:            
            loc=(loc+1)%len(board.blocks)
            if applyGo:
                if loc==0:
                    player.money+=200
        player.landOn(board.blocks[loc])
    

###################
# Blocks Section
###################


#represents a block on the board that containing an asset
#this block can belong to a player
class block():
    def __init__(self, name):
        self.name = name
    
    def getActions():
        pass
    
class utilBlock(block):         #utilities and railway stations
    def __init__(self, name, uType, price):
        block.__init__(self, name)
        self.color = uType    #utiltiy or railway station !see top at the file
        self.price = price
        self.owner=None
    def __str__(self):
        return self.name
     
    def pass_(self):
        pass
    def payRent(self):
        if self.color==0:
            self.player.pay(20)
        else:
            self.player.pay(50)
    def purchase(self):
        if not self.player==NOPLAYER:
            self.player.buy(self)        
    def getActions(self):
        if self.owner==None :
            return {"buy":self.purchase,"pass":self.pass_}            
        elif self.owner==self.player.playerName or self.owner=='bank':                        
            return {"pass",self.pass_}
        else:
            return {"Pay Rent",self.pay_rent()}                            
    def mortage(self):
        if(self.owner!='bank' and self.owner!=None):
            #player=getPlayerFromName(self.owner)
            player.money+=self.price/2
            self.owner='bank'
    def reMortage(self,player):
        if self.owner=='bank':
            player.buy(self)
        

class assetBlock(block):
    def __init__(self,name,color,price):
        block.__init__(self,name)        
        self.color=color
        self.price=price
        self.houses=0
        self.hotel=False
        self.owner=None
    def purchase(self):
        self.player.buy(self)
        
    def __str__(self):
        return self.name
    
    def payRent(self):
        rent=self.price//30
        self.player.pay(rent)
        
    def pass_(self):
        pass
    def getActions(self):
        if self.owner==None :
            return {"Buy":self.purchase,"pass":self.pass_}            #auction???
        elif self.owner==self.player.playerName or self.owner=='bank':                        
            return {"pass",self.pass_}
        else:
            return {"Pay Rent",self.pay_rent()}                        
    
    def purchase(self, console):            #buy function should not exist, whole process should be in purchase
        if not self.player==NOPLAYER:       #And believe me is against principles! both classes are mutuly dependent, 
            self.player.buy(self)           #only one class should be calling other class!
            console.display("{} bought the {} for {}$".format(self.player.name,self.name,self.price*-1))
        
    def mortage(self):
        if(self.owner!='bank' and self.owner!=None):
            #player = getPlayerFromName(self.owner)
            player.money+=self.price/2
            self.owner='bank'
    def reMortage(self,player):
        if self.owner=='bank':
            player.buy(self)
    def buildHouse(self):
        pass
    def buildHotel(self):
        pass


#represent a block on the board that landing on means u need to pull a card from some deck        
class cardBlock():
    def __init__(self, name,deck):
        block.__init__(self, name)
        self.deck=deck
    def getCard(self):
        card=self.deck.getCard()
        card.applyToPlayer(self.player)
    def getActions(self):
        return {"Get Card":self.getCard}
    

class moneyBlock():                 #Go , tax , luxury tax etc blocks which onLand
    def __init__(self, name, money):      # action is just adding or subtracting money
        block.__init__(self, name)
        self.deck=deck
        self.money = money
    def use(self):
        if not self.player==NOPLAYER:
            self.player.money+=self.money
    def getActions(self):
        return {"Change money : "+str(self.money):self.use}
    
    
class goToJailBlock(block):
    def __init__(self, name="'Go TO Jail'"):
        block.__init__(self, name)

    def goToJail(self):
        if not self.player==NOPLAYER:
            self.player.goToJail()
    def getActions(self):
        return {'Go To jail':self.goToJail}
               
            
    



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
        
    def pay(self,ammount):
        self.money-=ammount
        
    def buy(self,assetBlock):
        self.money-=assetBlock.price
        assetBlock.owner=self.name
        if(assetBlock.color in self.assets):
            self.assets[assetBlock.color].append(assetBlock)
        else:
            self.assets[assetBlock.color]=[assetBlock]
    def printPlayer(self):
        console.display(self.name+" money: "+str(self.money)+" assets : "+str(self.assets))
    def landOn(self,block,location):        
        self.location=location
        block.player=self
        console.display(self.name+" lands on "+block.name)
    def getHousesAndHotels(self):
        houses=0
        hotels=0
        for group in self.assets.values():
            for asset in group:
                houses+=asset.houses
                if asset.hotel==True:
                    hotels+=1
        return (houses,hotels)
    def goToJail(self):
        self.inJail=True
        while board.blocks[self.location].name!='jail':            
            self.location=(self.location+1)%len(board.blocks)
    def is_bankrupt(self):
        if self.money<=0:
            return True
        return False
