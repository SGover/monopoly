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
    def __init__(self):
        self.player=None
    
    def getActions():
        pass
    def pass_():
        pass    
        

class assetBlock(block):
    def __init__(self,asset):
        block.__init__(self)
        self.asset=asset
        self.houses=0
        self.hotel=False
    def purchase(self):
        self.player.buy(self.asset)
    def payRent(self):
        rent=self.asset.value//30
        self.player.pay(rent)
    def getActions(self):
        if asset.owner==None :
            return {"Buy":self.purchase,"pass",self.pass_}            
        elif asset.owner==self.player.playerName:                        
            return {"pass",self.pass_}
        else:
            return {"Pay Rent",self.pay_rent()}

#represent a block on the board that landing on means u need to pull a card from some deck        
class cardBlock():
    def __init__(self,deck):
        block.__init__(self)
        self.deck=deck
    def getCard(self):
        deck.getCard().applyToPlayer(self.player)
    def getActions(self):
        return {"Get Card":self.getCard}
        




#represents an asset
#asset have a name a group name and a value       
class asset():
    def __init__(self,name,groupName,value,utilty=False,railRoad=False):
        self.name=name
        self.groupName=groupName
        self.value=value
        self.owner=None
        self.utility=utility
        self.railRoad=railRoad


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
    def pay(self,ammount):
        self.money-=ammount
    def buy(self,asset):
        self.money-=asset.value
        asset.owner=self.name
        if(assets.has_key(asset.fatherName)):
            assets[fatherName].append(asset)
        else:
            assets[fatherName]=[asset]
    def landOn(self,block,location):        
        self.location=location
        block.player=player
    def getHousesAndHotels(self):
        houses=0
        hotels=0
        for group in assets.values():
            for asset in group:
                houses+=asset.houses
                if asset.hotel=True:
                    hotels+=1
        return (houses,hotels)
    def is_bankrupt(self):
        pass
