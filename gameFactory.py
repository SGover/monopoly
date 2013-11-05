from gameClasses import *
#this class initate some values from a file
class initFromFile():
    inObject=False
    currObject=''
    cards=[]
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
        if self.currObject=='assets':
            split=line.split(",")
            self.assets.append(asset(split[0],split[1],int(split[2])))
        elif self.currObject=='cards':
            split=line.split(",")
            self.cards.append(split[0])
def test():
    iff=initFromFile('gameProperties.txt')
    print ('prining assets: ')
    for asset in iff.assets:    
        print ('name : '+asset.name+', group : '+asset.groupName+', value : '+str(asset.value))
    print ('printing cards: ')
    for card in iff.cards:
        print ('card : '+card)
        
test()
            
   
