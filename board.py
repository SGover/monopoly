from gameClasses import *
from random import *

chance_cards = []
chest_cards = []

chance_deck = deck(chance_cards,"chance")
chest_deck = deck(chest_cards,"chest")

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
             moneyBlock("JAIL, JUST VISITING", 0),      #if money is zero, its land action will be ignored
             assetBlock("ST. CHARLES PLACE", PURPLE,-140),
             utilBlock("ELECTERIC COMPANY", UTILITY, -150),
             #work undergoing ....!!
             
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
