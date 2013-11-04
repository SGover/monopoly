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
class assetBlock():
    def __init__(self,asset):
        self.asset=asset
        self.owner=None
    def purchase(self,name):
        self.owner=name
class cardBlock():
    def __init__(self,deck):
        self.deck=deck
    def getCard():
        self.deck.getCard()
class asset():
    def __init__(self,name,fatherName,value):
        self.name=name
        self.fatherName=fatherName
        self.value=value        
class player():
    def __init__(self,name,money):
        self.name=name
        self.money=money
        self.assets={}
    def buy(self,asset):
        self.money-=asset.value
        if(assets.has_key(asset.fatherName)):
            assets[fatherName].append(asset)
        else:
            assets[fatherName]=[asset]

    
