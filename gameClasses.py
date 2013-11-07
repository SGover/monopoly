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

#this class represents a deck of cards like surprize cards or punishment cards

players=[]
#dont forget to set this before each game
def setPlayers(newPlayers):
    global players
    players=newPlayers


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
            deck=discard
            self.shuffle()
            discard=[]            
        card=deck.pop
        discard.append(card)
        return card
    def addCard(card):
        cards.append(card)
        
        
        
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
    def __init__(self,title,text,target):
        card.__init__(self,title,text)


class moveToNearestCard(card):
    def __init__(self,title,text,groupName,blocks):
        card.__init__(self,title,text)
        self.target=target     
    def applyToPlayer(self,player):
        player.location=target
    

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
    def __init__(self, name, type, price):
        block.__init__(self, name)
        self.type = type    #utiltiy or railway station !see top at the file
        self.price = price        

    def purchase(self):
        self.player.buy(self)        
  
    def mortage(self):
        if(owner!='bank' and owner!=None):
            player=getPlayerFromName(self.owner)
            player.money+=self.price/2
            self.owner='bank'
    def reMortage(self,player):
        if owner=='bank':
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
    def payRent(self):
        rent=self.price//30
        self.player.pay(rent)
    def pass_(self):
        pass
    def getActions(self):
        if self.owner==None :
            return {"Buy":self.purchase,"pass":self.pass_}            
        elif self.owner==self.player.playerName or self.owner=='bank':                        
            return {"pass",self.pass_}
        else:
            return {"Pay Rent",self.pay_rent()}                        
    def purchase(self):
        self.player.buy(self.asset)
    def mortage(self):
        if(owner!='bank' and owner!=None):
            player=getPlayerFromName(self.owner)
            player.money+=self.price/2
            self.owner='bank'
    def reMortage(self,player):
        if owner=='bank':
            player.buy(self)
    def buildHouse():
        pass
    def buildHotel():
        pass


#represent a block on the board that landing on means u need to pull a card from some deck        
class cardBlock():
    def __init__(self, name,deck):
        block.__init__(self, name)
        self.deck=deck
    def getCard(self):
        deck.getCard().applyToPlayer(self.player)
    def get_actions(self):
        return {"Get Card":self.getCard}
    

class moneyBlock():                 #Go , tax , luxury tax etc blocks which onLand
    def __init__(self, name, money):      # action is just adding or subtracting money
        block.__init__(self, name)
        self.deck=deck
        self.money = money    
    def getActions(self):
        pass
    
    
class goToJailBlock(block):
    def __init__(self, name="'Go TO Jail'"):
        block.__init__(self, name)

    def getActions(self):
        pass
    



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
        
    def pay(self,ammount):
        self.money-=ammount
        
    def buy(self,assetBlock):
        self.money-=assetBlock.price
        assetBlock.owner=self.name
        if(assets.has_key(assetBlock.color)):
            assets[assetBlock.color].append(assetBlock)
        else:
            assets[assetBlock.color]=[assetBlock]
            
    def landOn(self,block,location):        
        self.location=location
        block.player=player

    def getHousesAndHotels(self):
        houses=0
        hotels=0
        for group in assets.values():
            for asset in group:
                houses+=asset.houses
                if asset.hotel==True:
                    hotels+=1
        return (houses,hotels)
        
    def is_bankrupt(self):
        if self.money<=0:
            return True
        return False
