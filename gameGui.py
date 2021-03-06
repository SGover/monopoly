from gui import guiButton
import time, sys, os
from constants import *
from random import randrange
import pygame
from pygame.locals import QUIT
from threading import Thread

X = 550
POPUP_TOP=100
POPUP_LEFT=200
POPUP_SIZE=(700,500)


class PopupWindow():
    def __init__(self,massage,buttons,image=None,texts=None,measures=((POPUP_TOP,POPUP_LEFT),POPUP_SIZE)):
        #self.gameWindow=gameWindow
        self.top=measures[0][0]
        self.left=measures[0][1]
        self.width=measures[1][0]
        self.height=measures[1][1]
        self.image=image
        self.texts=texts
        self.massage=massage
        self.buttons=buttons
        for button in self.buttons:
            button.position = (self.left+button.position[0],self.top+button.position[1])
        self.background=pygame.Surface((self.width,self.height))
        pygame.font.init()
        self.fnt = pygame.font.Font("fonts//Kabel.ttf", 20)

    def draw(self,surf):
        self.background.fill((25,25,25))
        frame = pygame.Surface((self.width-10,self.height-10))
        frame.fill((220,220,220))
        self.background.blit(frame, (5,5))
        if self.texts!=None:
            for text in self.texts:
                t=self.fnt.render(text[0],True,BLACK)
                self.background.blit(t, text[1])
        surf.blit(self.background,(self.left,self.top))
        m=self.fnt.render(self.massage,True,BLACK)
        if self.image!=None:
            surf.blit(self.image,(330,140))
        surf.blit(m,(self.left+30,self.top+15))
        for button in self.buttons:
            if button._enable:
                surf.blit(button,button.position)
        
    def handle_event(self,event):
        for button in self.buttons:
            button.handle_event(event)
    def close(self):
        del[self]
        
class TradeWindow(PopupWindow):
    def __init__(self,buttons,trader,players):
        self.buttons=buttons
        self.trader=trader
        self.players=players
        self.money_interval=[50,50]
        self.money1=0
        self.money2=0
        margin=5
        curr_x=20
        curr_y=50        
        block_size=(50,75)
        headers=[(players[0].name+ ' assets',(800//4-1,20)),(players[1].name+ ' assets',(3*800//4,20)),
                 ('money :$'+str(players[0].money),(800//4-170,20)),('money :$'+str(players[1].money),(-170+3*800//4,20)),
                 ('Trade assets',(POPUP_SIZE[0]//4-100,260)),('Trade assets',(3*POPUP_SIZE[0]//4-100,260))]
        for asset in players[0].assets_list():
            self.buttons.append(guiButton('',(curr_x,curr_y),action=self.add1_asset,parameter=asset,image=get_asset_image(asset),name='add'+asset.name,sizing=0.5,y_sizing=0.5))
            self.buttons.append(guiButton('',(curr_x,curr_y+260),action=self.rem1_asset,parameter=asset,image=get_asset_image(asset),name='rem'+asset.name,enabled=False,sizing=0.5,y_sizing=0.5))
            if curr_x+block_size[0]<POPUP_SIZE[0]//2-margin:
                    curr_x=curr_x+block_size[0]
            else:
                    curr_x=50
                    curr_y+=block_size[1]
        curr_x=20
        curr_y=50        
        for asset in players[1].assets_list():            
            self.buttons.append(guiButton('',(POPUP_SIZE[0]//2+curr_x,curr_y),action=self.add2_asset,parameter=asset,image=get_asset_image(asset),name='add'+asset.name,sizing=0.5,y_sizing=0.5))
            self.buttons.append(guiButton('',(POPUP_SIZE[0]//2+curr_x,curr_y+260),action=self.rem2_asset,parameter=asset,image=get_asset_image(asset),name='rem'+asset.name,enabled=False,sizing=0.5,y_sizing=0.5))
            if curr_x+block_size[0]<POPUP_SIZE[0]//2-margin:
                    curr_x=curr_x+block_size[0]
            else:
                    curr_x=100
                    curr_y+=block_size[1]

        self.buttons.append(guiButton('+',(50,500),action=self.add1_money))
        self.buttons.append(guiButton('-',(120,500),action=self.rem1_money))
        self.buttons.append(guiButton('+',(450,500),action=self.add2_money))
        self.buttons.append(guiButton('-',(520,500),action=self.rem2_money))
        PopupWindow.__init__(self,'',buttons,texts=headers,measures=((100,50),(800,600)))
        self.top_dx=[40,40]
        self.top_dy=[100,100]
        self.down_dx=[40,40]
        self.down_dy=[400,400]    
    def add1_money(self):
        new_v=self.trader.player1_money+self.money_interval[0]
        if new_v<self.players[0].money:
            self.trader.set_money1(new_v)
            self.money1=new_v                
    def add2_money(self):
        new_v=self.trader.player2_money+self.money_interval[1]
        if new_v<self.players[1].money:
            self.trader.set_money2(new_v)
            self.money2=new_v        
    def rem1_money(self):
        new_v=self.trader.player1_money-self.money_interval[0]
        if new_v>=0:
            self.trader.set_money1(new_v)
            self.money1=new_v        
    def rem2_money(self):
        new_v=self.trader.player2_money-self.money_interval[1]
        if new_v>=0:
            self.trader.set_money2(new_v)
            self.money2=new_v        
    def enable_asset(self,name,enabled):
        for button in self.buttons:
            if button.name==name:
                button.set_enabled(enabled)
    def add1_asset(self,asset):
        self.trader.add_asset_1(asset)        
        self.enable_asset('add'+asset.name,False)
        self.enable_asset('rem'+asset.name,True)                        
    def rem1_asset(self,asset):
        self.trader.remove_asset_1(asset)
        self.enable_asset('add'+asset.name,True)
        self.enable_asset('rem'+asset.name,False)
    def add2_asset(self,asset):
        self.trader.add_asset_2(asset)        
        self.enable_asset('add'+asset.name,False)
        self.enable_asset('rem'+asset.name,True)                        
    def rem2_asset(self,asset):
        self.trader.remove_asset_2(asset)
        self.enable_asset('add'+asset.name,True)
        self.enable_asset('rem'+asset.name,False)
    def draw(self,surf):
        PopupWindow.draw(self,surf)
        t=self.fnt.render('Trade money $'+str(self.money2),True,BLACK)
        surf.blit(t, (self.left-50+3*700//4,self.top+550))
        t=self.fnt.render('Trade money $'+str(self.money1),True,BLACK)
        surf.blit(t, (self.left+700//4-100,self.top+550))
                
    def update(self):
        pass 

        
        
class StatusWindow():
    players = []
    def __init__(self):
        pass

    def start(self, players):
        self.players = players
        # setting fonts
        pygame.font.init()
        self.fnt_name = pygame.font.Font("fonts//Kabel.ttf", 28)
        self.fnt_money = pygame.font.Font("fonts//Kabel.ttf", 24)
        self.fnt_asset = pygame.font.Font("fonts//Kabel.ttf", 13)
        self.img = pygame.image.load("images//gui//status.png")
        
            
    def draw(self, background):
        self.img = self.img.convert_alpha()
        l = 0
        for p in self.players:
            height = l * 270
            
            background.blit(self.img, (X,height+5))
            
            txt_name = self.fnt_name.render(p.name, True, P_COLORS[l])
            textpos = txt_name.get_rect().move(X+15,15+height)
            background.blit(txt_name, textpos)
            
            background.blit(pygame.image.load(TOKENS[p.token_index]).convert_alpha(), (X+250,15+height))
            
            txt_money = self.fnt_money.render("$"+str(p.money), True, (10, 10, 10))
            textpos = txt_money.get_rect().move(X+320,25+height)
            background.blit(txt_money, textpos)
            
            i = 0
            for c in p.assets:
                color = COLORS[c]
                text = ""
                for asset in p.assets[c]:
                    text = text + asset.name + " | " 
                txt_money = self.fnt_asset.render(text, True, color)    
                textpos = txt_money.get_rect().move(X+10,68+height+(i*20))
                background.blit(txt_money, textpos)
                i += 1
            l += 1    
        return background

def get_asset_image(asset):    
    
    #init fonts
    fnt_title = pygame.font.Font("fonts//Kabel.ttf", 10)
    fnt_des = pygame.font.Font("fonts//Kabel.ttf", 9)    
    #creating the image
    surf=pygame.Surface((90,135))
    surf.fill((255,255,255))
    #filling the top
    surf.fill(COLORS[asset.color],pygame.Rect(0,0,90,30))
    #draw title
    text=asset.name.split(' ')
    title = fnt_title.render(text[0], True, BLACK)    
    pos = title.get_rect().move(1,2)
    surf.blit(title,pos)
    title = fnt_title.render(text[1], True, BLACK)    
    pos = title.get_rect().move(1,15)
    surf.blit(title,pos)
  
    #draw rent
    if asset.color!=UTILITY and asset.color!=RW_STATION:
        rent=fnt_des.render("Rent      $"+str(asset.rent_list[0]), True, BLACK)
        pos = rent.get_rect().move(5,30)
        surf.blit(rent,pos)
        for num in range (1,5):
            rent=fnt_des.render(str(num)+" houses   $"+str(asset.rent_list[num]), True, BLACK)
            pos = rent.get_rect().move(5,30+num*11)
            surf.blit(rent,pos)
        rent=fnt_des.render("hotel     $"+str(asset.rent_list[5]), True, BLACK)
        pos = rent.get_rect().move(5,30+62)
        surf.blit(rent,pos)
        mortage=fnt_des.render("mortage $"+str(asset.price//2), True, BLACK)
        pos = mortage.get_rect().move(5,30+72)
        surf.blit(mortage,pos)
        price=fnt_des.render("house price $"+str(asset.house_price), True, BLACK)
        pos = price.get_rect().move(5,30+82)
    else:
        if asset.color==UTILITY:
            descripton=['   Rent',
                        'own 1',
                        'dice roll X 4',
                        '',
                        'own 2',
                        'dice roll X 10']
        else:
            descripton=['   Rent',
                        'own 1   $25',
                        'own 2   $50',
                        'own 3   $100',
                        'own 4   $200']
        for line in descripton:
            tline=fnt_des.render(line, True, BLACK)
            pos = tline.get_rect().move(5,40+descripton.index(line)*11)
            surf.blit(tline,pos)
    return surf

class GameWindow():
    #get the board and the players
    def __init__(self,board,players,console):        
        self.console=console
        self.board=board
        self.players=players
        self.quit=False
        self.statusWin=StatusWindow()
        self.statusWin.start(self.players)
        self.buttonPad = buttonPad()
        self.popup=False
        self.popupWindow=None

    #creating a thread and run its draw function on it
    def run(self):        
        self.thread = Thread(target=self.draw)
        self.thread.daemon = True        
        self.thread.start()
    
    def open_popup(self,popup):
        self.popup=True
        self.popupWindow=popup
    
    def draw(self):        
        # Initialise screen
        pygame.init()  
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(50,20)  # x,y position of the screen
        screen = pygame.display.set_mode((1025, 700))       #witdth and height
        pygame.display.set_caption('Monopoly')
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        clock = pygame.time.Clock()
        
        #initate the tokens for players
        token_list = []
        for p in self.players:
            token_list.append(pygame.image.load(TOKENS[p.token_index]).convert_alpha())
        
        # Event loop
        while 1:
            clock.tick(60)  #FPS
            if not self.popup:
                brd_img = pygame.image.load("images//monopoly.png")            
                brd_img = brd_img.convert()
                for event in pygame.event.get():
                    self.buttonPad.handle_event(event)
                    if event.type == QUIT or self.quit:
                        pygame.quit()
                        os.kill(os.getpid(),0)            
                background.fill((50, 50, 50))
                background = self.console.draw(background)   # console
                self.buttonPad.draw(background)
                background = self.statusWin.draw(background)    #status window            
                for block in self.board.blocks:
                    if not (block.color == RW_STATION or block.color == UTILITY or block.color == -1):
                        if block.hotel:
                            #draw hotel
                            h = pygame.image.load(BUILDINGS[0])
                            brd_img.blit(h, (block.position[0]-8,block.position[1]-5))
                        elif block.houses>=1:
                            #draw houses
                            h = pygame.image.load(BUILDINGS[block.houses])
                            brd_img.blit(h, (block.position[0]-8,block.position[1]-5))
                #get players location on board

                player_pos = []
                for p in self.players:
                    player_pos.append(self.board.blocks[p.location].position)
                #draw players
                i = 0
                check = []
                for pos in player_pos:
                    for c in check:
                        if pos==c:
                            pos = (pos[0],pos[1]+25) 
                    brd_img.blit(token_list[i], (pos[0]-15,pos[1]-10))
                    check.append(pos)
                    i += 1
                
                background.blit(brd_img, (5,5))

                screen.blit(background, (0, 0))            
                pygame.display.flip()
            #popup
            else:
                for event in pygame.event.get():
                    if self.popupWindow!=None:
                        self.popupWindow.handle_event(event)
                    if event.type == QUIT or self.quit:
                        pygame.quit()
                        os.kill(os.getpid(),0)
                if self.popupWindow!=None:
                    self.popupWindow.draw(screen)
                pygame.display.flip()
        
            
    def stop(self):
        self.quit = True
    def move_pawn(self,player,target_move):
        while player.location!=target_move:
            player.location=(player.location+1)%len(self.board.blocks)
            time.sleep(0.25)
    def prompt_commands(self, list_cmds):
        return self.buttonPad.create_selection_menu(list_cmds)
    
    def choose_from_options(self,actions,image=None):
        i=0
        self.buttons=[]
        for name in actions.keys():            
            self.buttons.append(guiButton(name,(250+i//3*100, 65+(i%3)*50),actions[name],sizing=1.5))
            i+=1        
        def check_click():
            for control in self.buttons:
                if control.clicked:
                    return True
            return False
        popup=PopupWindow('Choose',self.buttons,image,measures=((POPUP_TOP,POPUP_LEFT),(400,200)))
        self.open_popup(popup)
        
        while not check_click():
            time.sleep(0.2)
        self.popup=False
        self.popupWindow=None
        popup.close()
        
    def create_trade_menu(self,players,image=None):
        from gameClasses import Trader

        trader=Trader(players[0],players[1])
        self.buttons=[]    
        passb=guiButton('pass',(700//2+40,600-50),action=passf)
        finishb=guiButton('finish',(700//2-40,600-50),action=trader.make_trade)
        self.buttons.append(passb)
        self.buttons.append(finishb)            

        def check_click():            
                if passb.clicked or finishb.clicked:
                    return True
                return False            
        popup=TradeWindow(self.buttons,trader,players)
        self.open_popup(popup)
        while not check_click():
            time.sleep(0.2)            
        self.popup=False
        self.popupWindow=None
        popup.close() 
        
    def choose_from_actions(self,actionsList,image=None,text='Choose',atexts=None):
        try:
            i=0
            self.buttons=[]
            margin=5
            curr_x=20
            curr_y=50
            block_size=(95,150)
            for action in actionsList:                
                if action.pic==None:                    
                    self.buttons.append(guiButton(action.name,(curr_x,curr_y),action=action.do_action))                    
                else:                    
                    self.buttons.append(guiButton('',(curr_x,curr_y),action=action.do_action,image=action.pic))
                if curr_x+block_size[0]<POPUP_SIZE[0]-margin:
                        curr_x=curr_x+block_size[0]
                else:
                    curr_x=20
                    curr_y+=block_size[1]
            self.buttons.append(guiButton('pass',(POPUP_SIZE[0]//2-40,POPUP_SIZE[1]-50),action=passf))            
            def check_click():
                for control in self.buttons:
                    if control.clicked:
                        return True
                return False            
            popup=PopupWindow(text,self.buttons,image,texts=atexts)
            self.open_popup(popup)
            while not check_click():
                time.sleep(0.2)
            self.popup=False
            self.popupWindow=None
            popup.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    
class buttonPad():
    
    def __init__(self):
        self.value=0
        self.controls=[]
    
    #replace prompt commands and prompt commands index
    def create_selection_menu(self,options):
        def set_value(value):
            self.value=value
        i=0
        self.controls=[]
        for option in options:
            x=620+(i//3)*135
            y=560+(i%3)*45
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
    
    def draw(self,surface):
        if len(self.controls)>0:
            for control in self.controls:
                surface.blit(control,control.position)
                
        return surface
    
    def set_enabled(self, enable):
        for control in self.controls:
            control.set_enabled(enable)
        
            
    #passing events from the main pygame thread(currently in gameWindow) 
    def handle_event(self,event):
        for control in self.controls:
            control.handle_event(event)
            
def passf():
    pass
