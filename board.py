from gameClasses import *
from random import randrange
from gameFactory import initFromFile
import pygame
from pygame.locals import QUIT
import threading
import os

P_COLORS = [(255,255,25),(255,25,255),
            (25,255,255),(255,25,25),
            (25,25,255),(25,255,25)]
IFF=initFromFile("gameProperties.txt")
CHANCE_DECK,CHEST_DECK=deck(IFF.chanceCards,"chance"),deck(IFF.chestCards,"chest")
CHANCE_DECK.shuffle()
CHEST_DECK.shuffle()

BLOCK_ARR = [moneyBlock("GO!", 200,(480,480)),
             assetBlock("MEDITER. RANEAN AVENUE", INDIGO,60,(430,480)),      #price should be always a negetive value to decrease confusion
             cardBlock("COMMUNITY CHEST", CHEST_DECK,(390,480)),
             assetBlock("BALTIC AVENUE", INDIGO,60,(345,480)),
             moneyBlock("INCOME TAX", -200,(305,480)),
             utilBlock("READING RAILROAD", RW_STATION, 200,(260,480)),
             assetBlock("ORIENTAL AVENUE", WHITE,100,(215,480)),
             cardBlock("CHANCE?", CHANCE_DECK,(170,480)),
             assetBlock("VERMONT AVENUE", WHITE,100,(130,480)),
             assetBlock("CONNECTICUT AVENUE", WHITE,120,(90,480)),
             moneyBlock("JAIL", 0,(25,480)),      #if money is zero, its land action will be ignored
             assetBlock("ST. CHARLES PLACE", PURPLE,140,(25,425)),
             utilBlock("ELECTERIC COMPANY", UTILITY, 150,(25,380)),
             assetBlock("STATES AVENUE", PURPLE,140,(25,340)),
             assetBlock("VIRGINIA AVENUE", PURPLE,160,(26,295)),
             utilBlock("PENNSYLVANIA RAILROAD", RW_STATION, 200,(25,255)),
             assetBlock("ST. JAMES PLACE", ORANGE,180,(25,210)),
             cardBlock("COMMUNITY CHEST", CHEST_DECK,(25,165)),
             assetBlock("TENNESSEE AVENUE", ORANGE,180,(25,125)),
             assetBlock("NEW YORK AVENUE", ORANGE,200,(25,80)),
             moneyBlock("FREE PARKING", 0,(25,25)),        #if money is zero, its land action will be ignored
             assetBlock("KENTUCKY AVENUE", RED,220,(90,25)),
             cardBlock("CHANCE?", CHANCE_DECK,(130,25)),
             assetBlock("INDIANA AVENUE", RED,220,(170,25)),
             assetBlock("ILLINOIS AVENUE", RED,240,(215,25)),
             utilBlock("B. & O. RAILROAD", RW_STATION, 200,(260,25)),
             assetBlock("ATLANTIC AVENUE", YELLOW,260,(305,25)),
             assetBlock("VENTNOR AVENUE", YELLOW,260,(345,25)),
             utilBlock("WATER WORKS", UTILITY, 150,(390,25)),
             assetBlock("MARVIN GARDENS", YELLOW,280,(430,25)),
             goToJailBlock((480,25)),
             assetBlock("PACIFIC AVENUE", GREEN,300, (480,80)),
             assetBlock("NORTH CAROLINA AVENUE", GREEN,300, (480,125)),
             cardBlock("COMMUNITY CHEST", CHEST_DECK, (480,165)),
             assetBlock("PENNSYLVANIA AVENUE", GREEN,320, (480,210)),
             utilBlock("SHORT LINE", RW_STATION, 200, (480,255)),
             cardBlock("CHANCE?", CHEST_DECK, (480,295)),
             assetBlock("PARK PLACE", BLUE,350, (480,340)),
             moneyBlock("LUXURY TAX", -75, (480,380)),
             assetBlock("BROAD WALK", BLUE,400, (480,425)),
             ]

class board():

               
    def __init__(self, statusW):
        self.blocks = BLOCK_ARR
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
        screen = pygame.display.set_mode((950, 550))       #witdth and height
        pygame.display.set_caption('Monopoly')
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
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
            player_pos = []
            for p in self.players:
                player_pos.append(self.blocks[p.location].position)
            i = 0
            for pos in player_pos:
                if not i == 0:
                    if pos==player_pos[i-1]:
                        pos = (pos[0]+20,pos[1]+20) 
                pygame.draw.rect(brd_img, P_COLORS[i], [pos[0],pos[1],20,20])
                i += 1
            
            background.blit(brd_img, (5,5))            
            
            screen.blit(background, (0, 0))
            pygame.display.flip()
            
    def stop(self):
        self.quit = True
