#this class represents a deck of cards like surprize cards or punishment cards
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
    def __init__(self,title,text,amount):
        card.__init__(self,title,text)
        self.amount=amount # amount of money to add or subtract from player(positive value will add and negetive will subtract)
		#change from fork
    def applyToPlayer(self,player):
        player.money+=self.amount
        
class advanceToCard(card):
    def __init__(self,title,text,target):
        player.money+=self.amount #negetive and positive values will automatically take care of addition and deductions
class moveToNearestCard(card):
    def __init__(self,title,text,groupName,blocks):
        card.__init__(self,title,text)
        self.target=target     
    def applyToPlayer(self,player):
        player.location=target
    
#represents a block on the board that containing an asset
#this block can belong to a player
class block():
    def __init__(self):
        self.player=None
    
    def getActions():
        pass
        
class assetBlock(block):
    def __init__(self,asset):
        block.__init__(self)
        self.asset=asset        
    def purchase(self):
        self.player.buy(self.asset)
    def getActions(self):
        if asset.owner==None or asset.owner==self.player.playerName:
            return {}
        else:            
            return {"Buy":self.purchase}
      
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
    def __init__(self,name,groupName,value):
        self.name=name
        self.groupName=groupName
        self.value=value
        self.owner=None
#represent a player
#player attributes : name,money,location,assets        
class player():
    def __init__(self,name,money):
        self.name=name
        self.money=money
        self.assets={}
        self.location=0
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
        block.
    def is_bankrupt(self):
        pass
