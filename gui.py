import pygame
from pygame.locals import *  
import threading
import os
from gameGui import P_COLORS, TOKENS


MOUSEDOWN = False
BACKDOWN = False
KEYDOWN = False
SPACEDOWN = False
GUIQUIT = False
hover = False
ENABLED_TEXT_COLOR = (235,235,235)
DISABLED_TEXT_COLOR = (200,200,200)

class guiButton(pygame.Surface):
    def __init__(self, caption, position, action=0):
        #initializing
        self.caption = caption      
        self.position = position
        self.action = action
        self.font_size = 14
        self.events = [MOUSEBUTTONDOWN,4,MOUSEBUTTONUP]
        #loading from files
        self.img = pygame.image.load("images\\gui\\blue.png")
        self.pressed = pygame.image.load("images\\gui\\pressed.png")
        self.hover = self.img.copy()
        self.hover.fill((255,255,255,0))
        self.btn = self.img.copy()
        self._width = self.img.get_width()
        self._height = self.img.get_height()
        self.img = self.img.convert_alpha()
        self.font = pygame.font.Font("fonts\\Kabel.ttf", self.font_size)
        self.text_color = ENABLED_TEXT_COLOR
        self._enable = True
        #calling parent constructor
        pygame.Surface.__init__(self, size=(self._width,self._height),flags=pygame.SRCALPHA)
        #update surface
        self.update_surface()
    
    def update_surface(self):
        #writing caption on button in the center
        text_surf = self.font.render(self.caption, True, self.text_color)
        textpos = text_surf.get_rect()
        textpos.center = (self.img.get_rect().center[0],
                          self.img.get_rect().center[1] - textpos.centery/4)
        self.img.blit(text_surf, textpos)
        #filling surface with transparent color and than pasting button on it
        self.fill((0,0,0,0))
        self.blit(self.img,(0,0))
        self.blit(self.hover,(0,0))
        
    def handle_event(self, event):
        global hover
        if self._enable:
            if event.type == 4:
                if self.get_rect().collidepoint((event.pos[0]-self.position[0],event.pos[1]-self.position[1])):
                    if not hover:
                        self.img = self.btn.copy()
                        self.hover.fill((255,255,255,20))
                        self.update_surface()
                        hover = True
                else:
                    if hover:
                        self.img = self.btn.copy()
                        self.hover.fill((255,255,255,0))
                        self.update_surface()
                        hover = False
            elif event.type==MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.get_rect().collidepoint((event.pos[0]-self.position[0],event.pos[1]-self.position[1])):
                        self.img = self.pressed.copy()
                        self.update_surface()
            elif event.type==MOUSEBUTTONUP:
                if event.button == 1:
                    if self.get_rect().collidepoint((event.pos[0]-self.position[0],event.pos[1]-self.position[1])):
                        if not self.action==0:
                            self.action()
                self.img = self.btn.copy()
                self.update_surface()
                    
    def set_enabled(self, enable):
        self._enable = enable
        if self._enable:
            self.img = self.btn.copy()
            self.text_color = ENABLED_TEXT_COLOR
        else:
            self.img = self.btn.copy()
            self.text_color = DISABLED_TEXT_COLOR
        self.update_surface()
    
    def set_font_size(self, size):
        self.font_size = size
        
    def set_caption(self, caption):
        self.caption = caption
        
    def set_position(self, position):
        self.position = position
                
    def set_action(self, action):
        self.action = action
        
####################
#guiImageList        
###################

class guiImageList(pygame.Surface):
    def __init__(self, position, image_paths):
        self.position = position
        self.images = []
        self.scrollx = 0
        self.selected = 0
        self.events = [MOUSEBUTTONUP]
        #loading from files
        for img in image_paths:
            self.images.append(pygame.image.load(img).convert_alpha())
        self.left = pygame.image.load("images\\gui\\left.png").convert_alpha()
        self.right = pygame.image.load("images\\gui\\right.png").convert_alpha()
        self.cover = pygame.image.load("images\\gui\\cover.png").convert_alpha()
        self.bg = pygame.image.load("images\\gui\\bg.png").convert_alpha()
        self.slct_img =  pygame.Surface((52,52))
        self.width = 240
        self.height = 70
        #calling parent constructor
        pygame.Surface.__init__(self, size=(self.width,self.height),flags=pygame.SRCALPHA)
        #filling surface with transparent color and than pasting button on it
        self.update_surface()
        
    def update_surface(self):
        self.fill((155,200,255))
        self.slct_img.fill((225, 231, 68))
        self.blit(self.bg, (0, 0))
        i = 0
        for img in self.images:
            if self.selected == i:
                self.slct_img.blit(img, (2, 2))
                img = self.slct_img
            self.blit(img,((64*i)+(-self.scrollx)+32, 10))
            i += 1
        self.blit(self.cover, (0, 0))
        self.blit(self.left, (8,2))
        self.blit(self.right, (self.width-(self.right.get_width()+9),2))        
        
    def handle_event(self, event):
        if event.type==MOUSEBUTTONUP:
            if event.button==1:
                pos = event.pos
                if self.left.get_rect().collidepoint((pos[0]-(self.position[0]+8),pos[1]-self.position[1])):
                    if self.scrollx >= 64:
                        self.scrollx -= 64
                        self.update_surface()
                elif self.right.get_rect().collidepoint((pos[0]-(self.position[0]+self.width-(self.right.get_width()+8)),pos[1]-self.position[1])):
                    if self.scrollx < (len(self.images)-3) * 64:
                        self.scrollx += 64
                        self.update_surface()
                else:
                    i = 0    
                    for img in self.images:
                        if img.get_rect().collidepoint(pos[0]-(self.position[0]+(64*i)+(-self.scrollx)+32),pos[1]-(self.position[1]+8)):
                            self.selected = i
                            self.update_surface()
                        i += 1    
################
# guiTextBox
################                        

class guiTextBox(pygame.Surface):
    def __init__(self, position, focus=False, label="Your Text Here ..."):
        self.position = position
        self.label = label
        self.focus = focus
        self.events = [MOUSEBUTTONDOWN]

        self.mask = pygame.image.load("images\\gui\\textbox.png")
        self.font = pygame.font.Font("fonts\\Kabel.ttf", 16)
        self.text = ""
        self._width = self.mask.get_width()
        self._height = self.mask.get_height()
        #calling parent constructor
        pygame.Surface.__init__(self, size=(self._width,self._height),flags=pygame.SRCALPHA)
        #filling surface with transparent color and than pasting button on it
        self.update_surface()
        thread1 = threading.Thread(target=self.key_event)
        thread1.daemon = True
        thread1.start()
        
    def update_surface(self):
        self.fill((155,200,255))
        self.blit(self.mask, (0, 0))
        if not self.focus:
            text_surf = self.font.render(self.text, True, (50,50,50))
        else:
            text_surf = self.font.render(self.text+"_", True, (50,50,50))
        textpos = text_surf.get_rect().move(5,self.get_rect().center[1] - text_surf.get_rect().centery)
        if not self.focus and self.text=="":
            text_surf = self.font.render(self.label, True, (200,200,200,150))
            textpos = text_surf.get_rect().move(5,self.get_rect().center[1] - text_surf.get_rect().centery)
        self.blit(text_surf, textpos)
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button==1:
                if self.get_rect().collidepoint((event.pos[0]-self.position[0],event.pos[1]-self.position[1])):
                    self.focus = True
                    self.update_surface()
                else:
                    self.focus = False
                    self.update_surface()
                        
    def key_event(self):
        global KEYDOWN
        global BACKDOWN
        global SPACEDOWN
        clock = pygame.time.Clock()
        # Event loop
        while True:
            if GUIQUIT:
                return
            clock.tick(100)
            if self.focus:
                k_list = pygame.key.get_pressed()
                if k_list[K_BACKSPACE]:
                    if not BACKDOWN:
                        self.text = self.text[:len(self.text)-1]
                        self.update_surface()
                        BACKDOWN = True
                else:
                    BACKDOWN = False
                    
                if k_list[K_SPACE]:
                    if not SPACEDOWN:
                        self.text = self.text + ' '
                        self.update_surface()
                        SPACEDOWN = True
                else:
                    SPACEDOWN = False        
                        
                k_list1 = k_list[K_a:K_DELETE]
                if True in k_list1:
                    if not KEYDOWN:
                        if pygame.key.get_mods() & KMOD_SHIFT:
                            self.text = self.text + chr(k_list1.index(True)+65)
                            self.update_surface()
                        else:
                            self.text = self.text + chr(k_list1.index(True)+97)
                            self.update_surface()
                        KEYDOWN = True
                else:
                    KEYDOWN = False
            
            
class playerDialog():
               
    def __init__(self):
        self.result = ""
    
    def show(self):
        self.thread = threading.Thread(target=self.draw)
        self.thread.daemon = True
        self.thread.start()
        self.thread.join()
        pygame.quit()
        global GUIQUIT
        GUIQUIT = False
        return self.result
    
    def draw(self):
        # Initialise screen
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(200,100)  # x,y position of the screen
        screen = pygame.display.set_mode((720, 540))       #witdth and height
        pygame.display.set_caption("Monopoly")
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        clock = pygame.time.Clock()
        #load
        bg_img = pygame.image.load("images\\gui\\bigbg.png")
        font = pygame.font.Font("fonts\\Kabel.ttf", 14)
        font2 = pygame.font.Font("fonts\\Kabel.ttf", 40)
        #controls
        p_num1 = font2.render("Player 1", True, (200,200,200))
        self.text_surf1 = font.render("Name : ", True, (30,30,30))
        self.tok_surf1 = font.render("Token : ", True, (30,30,30))
        p_num2 = font2.render("Player 2", True, (200,200,200))
        self.text_surf2 = font.render("Name : ", True, (30,30,30))
        self.tok_surf2 = font.render("Token : ", True, (30,30,30))
        control_list = []
        control_list.append(guiTextBox((50,200), focus=True, label="player1"))
        control_list.append(guiImageList((50,270), TOKENS))
        control_list.append(guiTextBox((360 + 50,200), focus=False, label="player2"))
        control_list.append(guiImageList((360 + 50,270), TOKENS))
        
        control_list.append(guiButton("Exit",(30,495), lambda: os.kill(os.getpid(),0)))
        control_list.append(guiButton("Play!",(620,495), lambda: get_input()))

        def get_input():
            if not control_list[0].text == "" and not control_list[2].text == "":
                self.result=[[control_list[0].text,control_list[1].selected],[control_list[2].text,control_list[3].selected]]
                global GUIQUIT
                GUIQUIT = True
            else:
                if control_list[0].text == "":
                    self.text_surf1 = font.render("Name : ", True, (255,30,30))
                if control_list[2].text == "":
                    self.text_surf2 = font.render("Name : ", True, (255,30,30))
        
        # Event loop
        while 1:
            clock.tick(100)  #FPS
            if GUIQUIT:
                return
            for event in pygame.event.get():
                for control in control_list:
                    if event.type in control.events:
                        control.handle_event(event)
                if event.type == QUIT:
                    pygame.quit()
                    os.kill(os.getpid(),0)
            background.fill((180, 190, 180))
            background.blit(bg_img, (0,0))
            background.blit(p_num1, (80, 70))
            background.blit(self.tok_surf1,(50,245))
            background.blit(self.text_surf1,(50,175))
            
            background.blit(p_num2, (360 + 80, 70))
            background.blit(self.tok_surf2,(360 + 50,245))
            background.blit(self.text_surf2,(360 + 50,175))
            
            for control in control_list:
                background.blit(control,control.position)
            screen.blit(background, (0, 0))
            pygame.display.flip()
