from gameClasses import *
from random import *
from gameFactory import initFromFile

iff=initFromFile("gameProperties.txt")
chance_deck,chest_deck=deck(iff.chanceCards,"chance"),deck(iff.chestCards,"chest")

block_arr = [moneyBlock("GO!", 200),
             assetBlock("MEDITER. RANEAN AVENUE", INDIGO,-60),      #price should be always a negetive value to decrease confusion
             cardBlock("COMMUNITY CHEST", chest_deck),
             assetBlock("BALTIC AVENUE", INDIGO,-60),
             moneyBlock("INCOME TAX", -200),
             utilBlock("READING RAILROAD", RW_STATION, -200),
             assetBlock("ORIENTAL AVENUE", WHITE,-100),
             cardBlock("CHANCE?", chance_deck),
             assetBlock("VERMONT AVENUE", WHITE,-100),
             assetBlock("CONNECTICUT AVENUE", WHITE,-120),
             moneyBlock("JAIL", 0),      #if money is zero, its land action will be ignored
             assetBlock("ST. CHARLES PLACE", PURPLE,-140),
             utilBlock("ELECTERIC COMPANY", UTILITY, -150),
             assetBlock("STATES AVENUE", PURPLE,-140),
             assetBlock("VIRGINIA AVENUE", PURPLE,-160),
             utilBlock("PENNSYLVANIA RAILROAD", RW_STATION, -200),
             assetBlock("ST. JAMES PLACE", ORANGE,-180),
             cardBlock("COMMUNITY CHEST", chest_deck),
             assetBlock("TENNESSEE AVENUE", ORANGE,-180),
             assetBlock("NEW YORK AVENUE", ORANGE,-200),
             moneyBlock("FREE PARKING", 0),        #if money is zero, its land action will be ignored
             assetBlock("KENTUCKY AVENUE", RED,-220),
             cardBlock("CHANCE?", chance_deck),
             assetBlock("INDIANA AVENUE", RED,-220),
             assetBlock("ILLINOIS AVENUE", RED,-240),
             utilBlock("B. & O. RAILROAD", RW_STATION, -200),
             assetBlock("ATLANTIC AVENUE", YELLOW,-260),
             assetBlock("VENTNOR AVENUE", YELLOW,-260),
             utilBlock("WATER WORKS", UTILITY, -150),
             assetBlock("MARVIN GARDENS", YELLOW,-280),
             goToJailBlock(),
             assetBlock("PACIFIC AVENUE", GREEN,-300),
             assetBlock("NORTH CAROLINA AVENUE", GREEN,-300),
             cardBlock("COMMUNITY CHEST", chest_deck),
             assetBlock("PENNSYLVANIA AVENUE", GREEN,-320),
             utilBlock("SHORT LINE", RW_STATION, -200),
             cardBlock("CHANCE?", chance_deck),
             assetBlock("PARK PLACE", BLUE,-350),
             moneyBlock("LUXURY TAX", -75),
             assetBlock("BROAD WALK", BLUE,-400),
             ]

class board():

               
    def __init__(self):
        self.chance_deck = chance_deck
        self.chest_deck = chest_deck
        self.blocks = block_arr
        pass
    
    def roll_dice(self):
        dice1 = randrange(6) + 1
        dice2 = randrange(6) + 1
        return (dice1, dice2)
