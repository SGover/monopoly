import gameClasses
import pygame

class console():
    init=False
    
    def __init__(self):
        self.massege_list=['']        
        self.clicked=False
        
    def display(self, string):
        print(string)
        str_lst = []
        str_lst.append(string)
        while len(str_lst[-1])>60:
            temp1 = str_lst[-1]
            n = temp1.rfind(" ",0,60)
            n = n if not n==-1 else len(temp1)-1
            str_lst[-1] = temp1[0:n]
            temp2 = temp1[n:]
            str_lst.append(temp2)
        for str in str_lst:        
            self.massege_list.append(str)
         
    def start(self):
        string = "******************************\n    New Game of Monopoly!\n******************************" 
        print(string)
        string = string.split("\n")
        for s in string: self.massege_list.append(s)
        
    def draw(self,surface):
        if not self.init:
            pygame.font.init()
            self.font = pygame.font.Font("fonts//UbuntuMono-R.ttf", 16)
        size=len(self.massege_list)
        frame = pygame.Surface((1015,145))
        frame.fill((250,250,250))
        surface.blit(frame,(5,550))
        line = pygame.Surface((7,170))
        line.fill((50,50,50))
        surface.blit(line,(599,545))    
        for i in range(1,9):
            if (size-i)>=0 and size-i<size:
                txt = self.font.render('>> '+self.massege_list[size-i], True, (0,0,0))
                text_pos = txt.get_rect().move(5,690-i*16)
                surface.blit(txt, text_pos)                
        return surface
    
    def get_player_name(self):
        name = input("Enter the Player name :_ ");
        while name=="":            
            name = input("Empty input string, Please Enter the Player name :_ ");
        print (name)
        return name 
    
    def show_winner(self, winner):
        print(winner.name,"is the winner!")
        
    def printBoard(self,board):
        for block in board.blocks:
            bType=type(block)
            if bType==type(gameClasses.block):
                if bType==type(gameClasses.assetBlock):
                    print (block.asset.name+" in : "+block.asset.groupName)
                elif bType==type(gameClasses.cardBlock):
                    print ("Deck : "+block.deck.name)
                    
