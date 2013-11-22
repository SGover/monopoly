import gameClasses
import pygame
from gui import guiButton
from gameGui import *
import time
P_COLORS = [(255,25,255),
            (25,255,255),(255,25,25),
            (25,25,255),(25,255,25)]
    
class console():
    init=False
    
    def __init__(self):
        self.massage='New Game of Monopoly!'
        self.massege_list=['New Game of Monopoly!']        
        self.controls=[]
        self.value=0
        self.clicked=False
    def setGameWindow(self,gameWindow):
        self.gameWindow=gameWindow
    def display(self, string):
        print(string)
        self.massege_list.append(string)
    def start(self):
        
        print("******************************\n    New Game of Monopoly!\n******************************")
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
        if len(self.controls)>0:
            for control in self.controls:
                surface.blit(control,control.position)
                
        return surface
    #####GUI TODO TASKS#####
    
    #replace choose from options
    def create_buttons_from_action_dict(self,actions):
        self.controls=[]
        i=0
        for name in actions.keys():            
            self.controls.append(guiButton(name,(600+i//3*100,550+(i%3)*50),actions[name],sizing=1.5))
            i+=1
        def check_click():
            for control in self.controls:
                if control.clicked:
                    return True
            return False
        while not check_click():
            time.sleep(0.2)
    #replace prompt commands and prompt commands index
    def create_selection_menu(self,options):
        def set_value(value):
            self.value=value
        i=0
        self.controls=[]
        for option in options:
            x=600+(i//3)*150
            y=550+(i%3)*50
            if len(str(option))>10:
                self.controls.append(guiButton(str(option),(x,y),set_value,option,1.75,7))
            else:
                self.controls.append(guiButton(str(option),(x,y),set_value,option,1.75))
            i+=1
        self.value=0
        while (self.value==0):
            time.sleep(0.1)
        print (self.value)
        return self.value
            
    #passing events from the main pygame thread(currently in gameWindow) 
    def handle_event(self,event):
        for control in self.controls:
            control.handle_event(event)
        
            
    ######################
    
    def get_player_name(self):
        name = input("Enter the Player name :_ ");
        while name=="":            
            
            name = input("Empty input string, Please Enter the Player name :_ ");
        print (name)
        return name 
    
    def show_winner(self, winner):
        
        print(winner,"is the winner!")
        
    def prompt_commands(self, list_cmds):
        return self.create_selection_menu(list_cmds)
      
        self.massage="Select a command:"
        print("\nSelect a command:")
        return input(" {} : ".format(list_cmds))
      
    def prompt_commands_index(self,list_cmds):
        return self.create_selection_menu(list_cmds)
    '''
        print ("use the number to select an option from the following options:")
        str1=''
        for cmd in list_cmds:
            str1+=" "+str(list_cmds.index(cmd)+1)+". "+str(cmd)
        index = -1
        while index<0 or index>=len(list_cmds):
            index= int(input(str1+'\n'))-1
        return list_cmds[index]
    '''         
        
    def printBoard(self,board):
        for block in board.blocks:
            bType=type(block)
            if bType==type(gameClasses.block):
                if bType==type(gameClasses.assetBlock):
                    print (block.asset.name+" in : "+block.asset.groupName)
                elif bType==type(gameClasses.cardBlock):
                    print ("Deck : "+block.deck.name)
    def createChooseButtonPopup(self,actions,image=None):        
        i=0
        self.buttons=[]
        for name in actions.keys():            
            self.buttons.append(guiButton(name,(70+i//3*100,110+(i%3)*50),actions[name],sizing=1.5))
            i+=1
        def check_click():
            for control in self.buttons:
                if control.clicked:
                    return True
            return False
        popup=PopupWindow(self.gameWindow,'Choose',self.buttons,image)
        self.gameWindow.open_popup(popup)
        while not check_click():
            time.sleep(0.2)            
        popup.close()        




        









        
    def chooseFromOptions(self,actions):
        
        self.create_buttons_from_action_dict(actions)
       
        """take a name:value pair as actions"""
        
        '''
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
        '''
        
