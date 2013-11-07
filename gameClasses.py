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
    
    def get_actions():
        pass


class utilBlock(block):         #utilities and railway stations
    def __init__(self, name, type, price):
        block.__init__(self, name)
        self.type = type    #utiltiy or railway station !see top at the file
        self.price = price        

    def purchase(self):
        self.player.buy(self.asset)
        
    def get_actions(self):
        pass
    def pass_():
        pass    
        
    def can_be_owned(self):
        return True
    
    def can_be_traded(self):
        return self.can_be_owned()
    
    def can_be_sold(self):
        return self.can_be_owned()
    
    def can_be_mortaged(self):
        return self.can_be_owned()
    
    def can_be_build(self):
        if self.can_be_owned():
            return False
        return False
        

class assetBlock(block):
<<<<<<< HEAD
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
=======
    def __init__(self, name, color, price):     #merging asset class into asset block class
        block.__init__(self, name)
        self.color=color
        self.price=price
                
    def purchase(self):
        self.player.buy(self.asset)
    def get_actions(self):
        if asset.owner==None or asset.owner==self.player.playerName:
            return {}
        else:            
            return {"Buy":self.purchase}
        
    def can_be_owned(self):
        return True
    
    def can_be_traded(self):
        return self.can_be_owned()
    
    def can_be_sold(self):
        return self.can_be_owned()
    
    def can_be_mortaged(self):
        return self.can_be_owned()
    
    def can_be_build(self):
        if self.can_be_owned():
            return True
        return False
      
>>>>>>> 67d6fc26da2572bae43e99cb100b6c52c2a58594

#represent a block on the board that landing on means u need to pull a card from some deck        
class cardBlock():
    def __init__(self, name,deck):
        block.__init__(self, name)
        self.deck=deck
    def getCard(self):
        deck.getCard().applyToPlayer(self.player)
    def get_actions(self):
        return {"Get Card":self.getCard}
    
    def can_be_owned(self):
        return False
    
    def can_be_traded(self):
        return self.can_be_owned()
    
    def can_be_sold(self):
        return self.can_be_owned()
    
    def can_be_mortaged(self):
        return self.can_be_owned()
    
    def can_be_build(self):
        if self.can_be_owned():
            return False
        return False 


class moneyBlock():                 #Go , tax , luxury tax etc blocks which onLand
    def __init__(self, name, money):      # action is just adding or subtracting money
        block.__init__(self, name)
        self.deck=deck
        self.money = money
    
    def get_actions(self):
        pass
    
    def can_be_owned(self):
        return False
    
    def can_be_traded(self):
        return self.can_be_owned()
    
    def can_be_sold(self):
        return self.can_be_owned()
    
    def can_be_mortaged(self):
        return self.can_be_owned()
    
    def can_be_build(self):
        if self.can_be_owned():
            return False
        return False 
        

class goToJailBlock(block):
    def __init__(self, name="'Go TO Jail'"):
        block.__init__(self, name)

    def get_actions(self):
        pass
    def can_be_owned(self):
        return False
    
    def can_be_traded(self):
        return self.can_be_owned()
    
    def can_be_sold(self):
        return self.can_be_owned()
    
    def can_be_mortaged(self):
        return self.can_be_owned()
    
    def can_be_build(self):
        if self.can_be_owned():
            return False
        return False




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
<<<<<<< HEAD
    def getHousesAndHotels(self):
        houses=0
        hotels=0
        for group in assets.values():
            for asset in group:
                houses+=asset.houses
                if asset.hotel=True:
                    hotels+=1
        return (houses,hotels)
=======
        #block.
>>>>>>> 67d6fc26da2572bae43e99cb100b6c52c2a58594
    def is_bankrupt(self):
        pass
