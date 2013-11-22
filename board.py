from gameClasses import *
from random import randrange
from gameFactory import initFromFile
import pygame
from pygame.locals import QUIT
from threading import Thread
import os
#from gui import guiButton, guiImageList, guiTextBox


IFF=initFromFile("gameProperties.txt")
CHANCE_DECK,CHEST_DECK=deck(IFF.chanceCards,"chance"),deck(IFF.chestCards,"chest")
CHANCE_DECK.shuffle()
CHEST_DECK.shuffle()

BLOCK_ARR = [moneyBlock("GO!", 200,(480,480)),
             assetBlock("MEDITER.RANEAN AVENUE", INDIGO,60,(430,480),50,[2,10,30,90,160,250]),      
             cardBlock("COMMUNITY CHEST", CHEST_DECK,(390,480)),
             assetBlock("BALTIC AVENUE", INDIGO,60,(345,480),50,[4,20,60,180,320,450]),
             moneyBlock("INCOME TAX", -200,(305,480)),
             utilBlock("READING RAILROAD", RW_STATION, 200,(260,480)),
             assetBlock("ORIENTAL AVENUE", WHITE,100,(215,480),50,[6,30,90,270,400,550]),
             cardBlock("CHANCE?", CHANCE_DECK,(170,480)),
             assetBlock("VERMONT AVENUE", WHITE,100,(130,480),50,[6,30,90,270,400,550]),
             assetBlock("CONNECTICUT AVENUE", WHITE,120,(90,480),50,[8,40,100,300,450,600]),
             moneyBlock("JAIL", 0,(25,480)),      #if money is zero, its land action will be ignored
             assetBlock("ST. CHARLES PLACE", PURPLE,140,(25,425),100,[10,50,150,450,625,750]),
             utilBlock("ELECTERIC COMPANY", UTILITY, 150,(25,380)),
             assetBlock("STATES AVENUE", PURPLE,140,(25,340),100,[10,50,150,450,625,750]),
             assetBlock("VIRGINIA AVENUE", PURPLE,160,(26,295),100,[12,60,180,500,700,900]),
             utilBlock("PENNSYLVANIA RAILROAD", RW_STATION, 200,(25,255)),
             assetBlock("ST. JAMES PLACE", ORANGE,180,(25,210),100,[14,70,200,550,750,950]),
             cardBlock("COMMUNITY CHEST", CHEST_DECK,(25,165)),
             assetBlock("TENNESSEE AVENUE", ORANGE,180,(25,125),100,[14,70,200,550,750,950]),
             assetBlock("NEW YORK AVENUE", ORANGE,200,(25,80),100,[16,80,220,600,800,100]),
             moneyBlock("FREE PARKING", 0,(25,25)),        #if money is zero, its land action will be ignored
             assetBlock("KENTUCKY AVENUE", RED,220,(90,25),150,[18,90,250,700,875,1050]),
             cardBlock("CHANCE?", CHANCE_DECK,(130,25)),
             assetBlock("INDIANA AVENUE", RED,220,(170,25),150,[18,90,250,700,875,1050]),
             assetBlock("ILLINOIS AVENUE", RED,240,(215,25),150,[20,100,300,750,975,1150]),
             utilBlock("B. & O. RAILROAD", RW_STATION, 200,(260,25)),
             assetBlock("ATLANTIC AVENUE", YELLOW,260,(305,25),150,[22,110,330,800,975,1150]),
             assetBlock("VENTNOR AVENUE", YELLOW,260,(345,25),150,[22,110,330,800,975,1150]),
             utilBlock("WATER WORKS", UTILITY, 150,(390,25)),
             assetBlock("MARVIN GARDENS", YELLOW,280,(430,25),150,[24,120,360,850,1025,1200]),
             goToJailBlock((480,25)),
             assetBlock("KARACHI AVENUE", GREEN,300, (480,80),200,[26,130,390,900,1100,1275]),
             assetBlock("MULTAN AVENUE", GREEN,300, (480,125),200,[26,130,390,900,1100,1275]),
             cardBlock("COMMUNITY CHEST", CHEST_DECK, (480,165)),
             assetBlock("FAISALABAD AVENUE", GREEN,320, (480,210),200,[28,150,450,1000,1200,1400]),
             utilBlock("LAHORE JUNCTION", RW_STATION, 200, (480,255)),
             cardBlock("CHANCE?", CHEST_DECK, (480,295)),
             assetBlock("PARK PLACE", BLUE,350, (480,340),200,[35,175,500,1100,1300,1500]),
             moneyBlock("LUXURY TAX", -75, (480,380)),
             assetBlock("BROAD WALK", BLUE,400, (480,425),200,[50,200,600,1400,1700,2000]),
             ]

class Board():

               
    def __init__(self):
        self.blocks = BLOCK_ARR        
        self.quit = False
    
    def roll_dice(self):
        dice1 = randrange(6) + 1
        dice2 = randrange(6) + 1
        return (dice1, dice2)
    
       
