import pygame
from pygame.locals import *  
import threading
import logging

MOUSEDOWN = False
KEYDOWN = False
ENABLED_TEXT_COLOR = (235,235,235)
DISABLED_TEXT_COLOR = (200,200,200)

class guiButton(pygame.Surface):
    def __init__(self, caption, position, action=0):
        #initializing
        self.caption = caption      
        self.position = position
        self.action = action
        self.font_size = 14
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
        #starting event listener
        thread = threading.Thread(target=self.mouse_event)
        thread.start()
    
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
        
    def mouse_event(self):
        clock = pygame.time.Clock()
        hover = False
        # Event loop
        while True:
            clock.tick(100)
            if self._enable:
                for event in pygame.event.get([MOUSEBUTTONDOWN,4,MOUSEBUTTONUP]):
                    if event.type == 4:
                        if self.get_rect().collidepoint((event.pos[0]-self.position[0],event.pos[1]-self.position[1])):
                            if not hover:
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
        thread = threading.Thread(target=self.mouse_event)
        thread.start()
        
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
        
    def mouse_event(self):
        clock = pygame.time.Clock()
        # Event loop
        while True:
            clock.tick(100)
            for event in pygame.event.get(MOUSEBUTTONUP):
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
                        
                
class guiTextBox(pygame.Surface):
    def __init__(self, position, focus=False, label="Your Text Here ..."):
        self.position = position
        self.label = label
        self.focus = focus
        self.mask = pygame.image.load("images\\gui\\textbox.png")
        self.font = pygame.font.Font("fonts\\Kabel.ttf", 16)
        self.text = ""
        self._width = self.mask.get_width()
        self._height = self.mask.get_height()
        #calling parent constructor
        pygame.Surface.__init__(self, size=(self._width,self._height),flags=pygame.SRCALPHA)
        #filling surface with transparent color and than pasting button on it
        self.update_surface()
        thread = threading.Thread(target=self.mouse_event)
        thread.start()        
        
    def update_surface(self):
        self.fill((155,200,255))
        self.blit(self.mask, (0, 0))
        text_surf = self.font.render(self.text, True, (50,50,50))
        textpos = text_surf.get_rect().move(5,self.get_rect().center[1] - text_surf.get_rect().centery/4)
        if not self.focus and self.text=="":
            text_surf = self.font.render(self.label, True, (200,200,200,150))
            textpos = text_surf.get_rect().move(5,self.get_rect().center[1] - text_surf.get_rect().centery)
        self.blit(text_surf, textpos)
        
    def mouse_event(self):
        clock = pygame.time.Clock()
        # Event loop
        while True:
            clock.tick(100)
            for event in pygame.event.get(MOUSEBUTTONDOWN):
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
        clock = pygame.time.Clock()
        # Event loop
        while True:
            clock.tick(100)
            k_list = pygame.key.get_pressed()
            if k_list[K_BACKSPACE]:
                print("backspace")
            k_list = k_list[K_a:K_DELETE]
            print(chr(k_list.index(True)))
            m = pygame.key.get_mods()
            if m & KMOD_SHIFT:
                print('shift pressed')
            
            

    