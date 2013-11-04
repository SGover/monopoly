
#this class represents a deck of cards like surprize cards or punishment cards
class deck():
    def __init__(self,cards):
        self.cards=cards
        self.discard=[]
    def shuffle(self):
        pass
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
#represents a block on the board that containing an asset
#this block can belong to a player    
class assetBlock():
    def __init__(self,asset):
        self.asset=asset
        self.owner=None
    def purchase(self,name):
        self.owner=name
        
#represent a block on the board that landing on means u need to pull a card from some deck        
class cardBlock():
    def __init__(self,deck):
        self.deck=deck
    def getCard():
        self.deck.getCard()
        
#represents an asset
#asset have a name a group name and a value       
class asset():
    def __init__(self,name,groupName,value):
        self.name=name
        self.groupName=groupName
        self.value=value
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
        if(assets.has_key(asset.fatherName)):
            assets[fatherName].append(asset)
        else:
            assets[fatherName]=[asset]

    
