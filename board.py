from gameClasses import *
from random import *

chance_cards = []
chest_cards = []
block_arr = []

class board():
               
    def __init__(self):
        self.chance_deck = deck(chance_cards,"chance")
        self.chest_deck = deck(chest_cards,"chest")
        self.blocks = block_arr
          
        pass
    
    def roll_dice(self):
        dice1 = randrange(6) + 1
        dice2 = randrange(6) + 1
        return (dice1, dice2)
