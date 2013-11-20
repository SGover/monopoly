from gameClasses import *
from random import randrange
import pygame
from pygame.locals import QUIT
from threading import Thread
import os

X = 545
COLORS = {"UTILTIES": (150,150,150),
          "RAILWAY STATIONS":(50,50,50),
          "INDIGO COLOR":(75,60,130),
          "LIGHTBLUE COLOR":(128,225,255),
          "PURPLE COLOR":(170,40,150),
          "ORANGE COLOR":(250,140,10),
          "RED COLOR":(250,10,10),
          "YELLOW COLOR":(240,240,0),
          "GREEN COLOR":(10,250,10),
          "BLUE COLOR":(10,10,250),
          }
TOKENS = ["images\\dog.png","images\\military.png",
          "images\\piece.png","images\\eye.png",
          "images\\scanner.png","images\\skull.png",
          "images\\tank.png","images\\tron.png",
          "images\\and.png","images\\worm.png"]

BUILDINGS = ["images\\hotel.png","images\\h1.png",
             "images\\h2.png","images\\h3.png",
             "images\\h4.png"]

P_COLORS = [(255,25,255),
            (25,255,255),(255,25,25),
            (25,25,255),(25,255,25)]
class PopupWindow:
    def __init__(self,gameWindow,massage,buttons,image=None):
        self.gameWindow=gameWindow
        self.image=image
        self.massage=massage
        self.buttons=buttons
        self.background=pygame.Surface((400,600))
        self.background.fill((220,220,220))
        pygame.font.init()
        self.fnt = pygame.font.Font("fonts\Kabel.ttf", 20)
    def draw(self,surf):
        m=self.fnt.render(self.massage,True,BLACK)
        if self.image!=None:
            self.background.blit(self.image,(40,400))
        self.background.blit(m,(100,20))
        for button in self.buttons:
            self.background.blit(button,button.position)
        surf.blit(self.background,(0,0))
    def handle_event(self,event):
        for button in self.buttons:
            button.handle_event(event)
    def close(self):
        self.gameWindow.popup=False
        self.gameWindow.popupWindow=None
        del[self]
class StatusWindow():
    players = []
    def __init__(self):
        pass

    def start(self, players):
        self.players = players
        # setting fonts
        pygame.font.init()
        self.fnt_name = pygame.font.Font("fonts\Kabel.ttf", 28)
        self.fnt_money = pygame.font.Font("fonts\Kabel.ttf", 24)
        self.fnt_asset = pygame.font.Font("fonts\Kabel.ttf", 16)
        self.img = pygame.image.load("images\\gui\\status.png")
        
            
    def draw(self, background):
        self.img = self.img.convert_alpha()
        l = 0
        for p in self.players:
            height = l * 270
            
            background.blit(self.img, (X,height+5))
            
            txt_name = self.fnt_name.render(p.name, True, P_COLORS[l])
            textpos = txt_name.get_rect().move(X+15,20+height)
            background.blit(txt_name, textpos)
            
            background.blit(pygame.image.load(TOKENS[p.token_index]).convert_alpha(), (X+250,15+height))
            
            txt_money = self.fnt_money.render("$"+str(p.money), True, (10, 10, 10))
            textpos = txt_money.get_rect().move(X+320,30+height)
            background.blit(txt_money, textpos)
            
            i = 0
            for c in p.assets:
                color = COLORS[c]
                text = ""
                for asset in p.assets[c]:
                    text = text + asset.name + " | " 
                txt_money = self.fnt_asset.render(text, True, color)    
                textpos = txt_money.get_rect().move(X+10,73+height+(i*20))
                background.blit(txt_money, textpos)
                i += 1
            l += 1    
        return background
    


def get_asset_image(asset):    
    
    #init fonts
    fnt_title = pygame.font.Font("fonts\Kabel.ttf", 10)
    fnt_des = pygame.font.Font("fonts\Kabel.ttf", 9)    
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
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(50,50)  # x,y position of the screen
        
        screen = pygame.display.set_mode((1020, 700))       #witdth and height
        
        pygame.display.set_caption('Monopoly')
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        clock = pygame.time.Clock()
        bg_img = pygame.image.load("images\\gui\\bigbg.png")
        
        #initate the tokens for players
        token_list = []
        for p in self.players:
            token_list.append(pygame.image.load(TOKENS[p.token_index]).convert_alpha())

        
        # Event loop
        while 1:
            clock.tick(30)  #FPS
            if not self.popup:
                brd_img = pygame.image.load("images\\monopoly.png")            
                brd_img = brd_img.convert()
                for event in pygame.event.get():
                    self.console.handle_event(event)
                    if event.type == QUIT or self.quit:
                        pygame.quit()
                        os.kill(os.getpid(),0)            
                background.fill((180, 190, 180))
                background = self.console.draw(background)   # console
                background.blit(bg_img, (0,0))
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
                    self.popupWindow.handle_event(event)
                    if event.type == QUIT or self.quit:
                        pygame.quit()
                        os.kill(os.getpid(),0) 
                self.popupWindow.draw(screen)
                pygame.display.flip()
        
            
    def stop(self):
        self.quit = True
