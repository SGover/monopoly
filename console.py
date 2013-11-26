import gameClasses
import pygame

from unittest.test.test_result import __init__

class console():
    init=False
    
    def __init__(self):
        self.massege_list=['']        
        self.clicked=False
        
    def setGameWindow(self,gameWindow):
        self.gameWindow=gameWindow
        
    def display(self, string):
        print(string)
        self.massege_list.append(string)
        
    def start(self):
        string = "******************************\n    New Game of Monopoly!\n******************************" 
        print(string)
        string = string.split("\n")
        for s in string: self.massege_list.append(s)
        
    def draw(self,surface):
        if not self.init:
            pygame.font.init()
            self.font = pygame.font.Font("fonts\consola.ttf", 14)
        size=len(self.massege_list)    
        for i in range(1,9):
            if (size-i)>=0 and size-i<size:
                txt = self.font.render('>> '+self.massege_list[size-i], True, (0,0,0))
                text_pos = txt.get_rect().move(5,690-i*16)
                surface.blit(txt, text_pos)                
        return surface
    
    #passing events from the main pygame thread(currently in gameWindow) 
    def handle_event(self,event):
        pass
#         self.buttons.handle_event(event)
        
    def get_player_name(self):
        name = input("Enter the Player name :_ ");
        while name=="":            
            name = input("Empty input string, Please Enter the Player name :_ ");
        print (name)
        return name 
    
    def show_winner(self, winner):
        print(winner,"is the winner!")
        
    def prompt_commands_index(self,list_cmds):
        return self.create_selection_menu(list_cmds)
        
    def printBoard(self,board):
        for block in board.blocks:
            bType=type(block)
            if bType==type(gameClasses.block):
                if bType==type(gameClasses.assetBlock):
                    print (block.asset.name+" in : "+block.asset.groupName)
                elif bType==type(gameClasses.cardBlock):
                    print ("Deck : "+block.deck.name)
                    