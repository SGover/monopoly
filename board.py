from gameClasses import *
from random import *
from gameFactory import initFromFile
import pygame
from pygame.locals import *
import threading
import os


#comment from Boaz branch

iff=initFromFile("gameProperties.txt")
chance_deck,chest_deck=deck(iff.chanceCards,"chance"),deck(iff.chestCards,"chest")
chance_deck.shuffle()
chest_deck.shuffle()

block_arr = [moneyBlock("GO!", 200),
             assetBlock("MEDITER. RANEAN AVENUE", INDIGO,60),      #price should be always a negetive value to decrease confusion
             cardBlock("COMMUNITY CHEST", chest_deck),
             assetBlock("BALTIC AVENUE", INDIGO,60),
             moneyBlock("INCOME TAX", -200),
             utilBlock("READING RAILROAD", RW_STATION, 200),
             assetBlock("ORIENTAL AVENUE", WHITE,100),
             cardBlock("CHANCE?", chance_deck),
             assetBlock("VERMONT AVENUE", WHITE,100),
             assetBlock("CONNECTICUT AVENUE", WHITE,120),
             moneyBlock("JAIL", 0),      #if money is zero, its land action will be ignored
             assetBlock("ST. CHARLES PLACE", PURPLE,140),
             utilBlock("ELECTERIC COMPANY", UTILITY, 150),
             assetBlock("STATES AVENUE", PURPLE,140),
             assetBlock("VIRGINIA AVENUE", PURPLE,160),
             utilBlock("PENNSYLVANIA RAILROAD", RW_STATION, 200),
             assetBlock("ST. JAMES PLACE", ORANGE,180),
             cardBlock("COMMUNITY CHEST", chest_deck),
             assetBlock("TENNESSEE AVENUE", ORANGE,180),
             assetBlock("NEW YORK AVENUE", ORANGE,200),
             moneyBlock("FREE PARKING", 0),        #if money is zero, its land action will be ignored
             assetBlock("KENTUCKY AVENUE", RED,220),
             cardBlock("CHANCE?", chance_deck),
             assetBlock("INDIANA AVENUE", RED,220),
             assetBlock("ILLINOIS AVENUE", RED,240),
             utilBlock("B. & O. RAILROAD", RW_STATION, 200),
             assetBlock("ATLANTIC AVENUE", YELLOW,260),
             assetBlock("VENTNOR AVENUE", YELLOW,260),
             utilBlock("WATER WORKS", UTILITY, 150),
             assetBlock("MARVIN GARDENS", YELLOW,280),
             goToJailBlock(),
             assetBlock("PACIFIC AVENUE", GREEN,300),
             assetBlock("NORTH CAROLINA AVENUE", GREEN,300),
             cardBlock("COMMUNITY CHEST", chest_deck),
             assetBlock("PENNSYLVANIA AVENUE", GREEN,320),
             utilBlock("SHORT LINE", RW_STATION, 200),
             cardBlock("CHANCE?", chance_deck),
             assetBlock("PARK PLACE", BLUE,350),
             moneyBlock("LUXURY TAX", -75),
             assetBlock("BROAD WALK", BLUE,400),
             ]

class board():

               
    def __init__(self, statusW):
        self.chance_deck = chance_deck
        self.chest_deck = chest_deck
        self.blocks = block_arr
        self.statusWin = statusW
        self.quit = False
    
    def roll_dice(self):
        dice1 = randrange(6) + 1
        dice2 = randrange(6) + 1
        return (dice1, dice2)
    
    def show(self, players):
        self.players = players
        self.statusWin.start(self.players)
        thread = threading.Thread(target=self.draw)
        thread.start()
    
    def draw(self):
        # Initialise screen
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(50,50)  # x,y position of the screen
        screen = pygame.display.set_mode((1000, 550))       #witdth and height
        pygame.display.set_caption('Monopoly')
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        point = (400,400)
        clock = pygame.time.Clock()
        # Event loop
        while 1:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT or self.quit:
                    return
            background.fill((180, 190, 180))
            background = self.statusWin.draw(background)
            brd_img = pygame.image.load("monopoly.png")
            brd_img = brd_img.convert()
            pygame.draw.rect(brd_img, (255,0,255), [point[0],point[1],20,20],0)
            background.blit(brd_img, (5,5))            
            
            screen.blit(background, (0, 0))
            pygame.display.flip()
            
    def stop(self):
        self.quit = True
