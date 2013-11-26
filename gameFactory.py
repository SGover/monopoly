from gameClasses import *
#this class initate some values from a file
ASSETS,CHESTMONEY,CHESTCOMMONEY='assets','ChestMoneyCards','ChestCommunityMoneyCards'
CHESTADV,CHESTGOOJ,CHESTRC='ChestAdvanceCards','ChestGetOutOfJail','chestRepairCard'
CHANCEADVS,CHANCEADVN='ChanceAdvanceCardSpecific','ChanceAdvanceCardNearest'
CHANCEM,CHANCECM='ChanceMoneyCards','ChanceCommunityMoneyCards'
class initFromFile():
    inObject=False
    currObject=''
    chestCards=[]
    chanceCards=[]
    def __init__(self,fileName):
        self.assets=[]
        file=open(fileName,'r')
        for line in file:
            line=line.replace('\n','')            
            if line=='{':
                self.inObject=True
            elif line=='}':
                self.inObject=False
                self.currObject=''
            else:
                if self.inObject:
                    self.updateObject(line)
                else:
                    self.currObject=line            
        file.close()
    def updateObject(self,line):
        if self.currObject==ASSETS:
            split=line.split(",")
            self.assets.append(block(split[0],split[1],int(split[2])))
        elif self.currObject==CHESTMONEY or self.currObject==CHANCEM:
            split=line.split(",")
            card=changeMoneyCard(split[0],split[1],int(split[2]))
            if self.currObject==CHESTMONEY:
                self.chestCards.append(card)
            else:
                self.chanceCards.append(card)
        elif self.currObject==CHESTCOMMONEY or self.currObject==CHANCECM:
            split=line.split(",")
            card=changeMoneyCard(split[0],split[1],int(split[2]),True)
            if self.currObject==CHESTCOMMONEY:
                self.chestCards.append(card)
            else:
                self.chanceCards.append(card)
        elif self.currObject==CHESTADV or self.currObject==CHANCEADVS:
            split=line.split(",")
            card=advanceToCard(split[0],split[1],split[2])
            if self.currObject==CHESTADV:
                self.chestCards.append(card)
            else:
                self.chanceCards.append(card)

def test():
    iff=initFromFile('gameProperties.txt')
    print ('prining assets: ')
    for asset in iff.assets:    
        print ('name : '+asset.name+', group : '+asset.groupName+', value : '+str(asset.value))
    print ('printing Chest: ')
    for card in iff.chestCards:
        print ('card : '+card.title)
        print (card.text)
    print ('printing Chance: ')
    for card in iff.chanceCards:
        print ('card : '+card.title)
        print (card.text)
        

            
   
