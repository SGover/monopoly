import gameClasses
import pygame
P_COLORS = [(255,25,255),
            (25,255,255),(255,25,25),
            (25,25,255),(25,255,25)]
    
class console():
    init=False
    def __init__(self):
        self.massage='New Game of Monopoly!'
        self.massege_list=['New Game of Monopoly!']
    def display(self, string):
        print(string)
        self.massege_list.append(string)
    def start(self):
        
        print("******************************\n    New Game of Monopoly!\n******************************")
    def draw(self,surface):
        if not self.init:
            pygame.font.init()
            self.font = pygame.font.Font("fonts\Kabel-Heavy.ttf", 28)
        size=len(self.massege_list)    
        for i in range(1,9):
            if (size-i)>=0 and size-i<size:
                txt = self.font.render('>> '+self.massege_list[size-i], True, (0,0,0))
                text_pos = txt.get_rect().move(55,800-i*30)
                surface.blit(txt, text_pos)                
        
        return surface
    def get_player_name(self):
        name = input("Enter the Player name :_ ");
        while name=="":
            name = input("Empty input string, Please Enter the Player name :_ ");
        return name 
    
    def show_winner(self, winner):
        
        print(winner,"is the winner!")
        
    def prompt_commands(self, list_cmds):
        self.massage="Select a command:"
        print("\nSelect a command:")
        return input(" {} : ".format(list_cmds))
    
    def prompt_commands_index(self,list_cmds):
        print ("use the number to select an option from the following options:")
        str1=''
        for cmd in list_cmds:
            str1+=" "+str(list_cmds.index(cmd)+1)+". "+str(cmd)
        index = -1
        while index<0 or index>=len(list_cmds):
            index= int(input(str1+'\n'))-1
        return list_cmds[index]
            
        
    def printBoard(self,board):
        for block in board.blocks:
            bType=type(block)
            if bType==type(gameClasses.block):
                if bType==type(gameClasses.assetBlock):
                    print (block.asset.name+" in : "+block.asset.groupName)
                elif bType==type(gameClasses.cardBlock):
                    print ("Deck : "+block.deck.name)
    
    def chooseFromOptions(self,actions):    
        """take a name:value pair as actions"""
        print("\nSelect a command :")
        i=0
        for key in actions.keys():
            i+=1
            print (str(i)+". "+key)
        cmd=input(" select :")
        while not (cmd in actions):
            print ("wrong command try again")
            cmd=input(" select :")
        print(" ")
        actions[cmd]()
        
