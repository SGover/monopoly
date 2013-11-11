import pygame
from pygame.locals import *  
import threading
import logging

MOUSEDOWN = False

class guiButton(pygame.Surface):
    def __init__(self, caption, position, action):
        #initializing
        pygame.init()
        self.caption = caption      
        self.position = position
        self.action = action
        self.font_size = 14
        #loading from files
        self.img = pygame.image.load("images\\blue.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img = self.img.convert_alpha()
        self.font = pygame.font.Font("fonts\\Kabel.ttf", self.font_size)
        #calling parent constructor
        pygame.Surface.__init__(self, size=(self.width,self.height),flags=pygame.SRCALPHA)
        #writing caption on button in the center
        self.caption = self.font.render(self.caption, True, (225,225,225))
        textpos = self.caption.get_rect()
        textpos.center = (self.img.get_rect().center[0],
                          self.img.get_rect().center[1] - textpos.centery/4)
        self.img.blit(self.caption, textpos)
        #filling surface with transparent color and than pasting button on it
        self.fill((0,0,0,0))
        self.blit(self.img,(0,0))
        #starting event listener
        thread = threading.Thread(target=self.mouse_event)
        thread.start()
        
    def mouse_event(self):
        global MOUSEDOWN
        clock = pygame.time.Clock()
        # Event loop
        while True:
            clock.tick(500)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            left = pygame.mouse.get_pressed()[0]
            if left:
                if not MOUSEDOWN:
                    MOUSEDOWN = True
            elif not left:
                if MOUSEDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.get_rect().collidepoint((pos[0]-self.position[0],pos[1]-self.position[1])):
                        self.action()
                MOUSEDOWN = False

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
class guiImageList(pygame.Surface):
    def __init__(self, position, image_paths):
        self.position = position
        self.images = []
        self.scrollx = 0
        self.selected = 2
        #loading from files
        for img in image_paths:
            self.images.append(pygame.image.load(img).convert_alpha())
        self.left = pygame.image.load("images\\left.png").convert_alpha()
        self.right = pygame.image.load("images\\right.png").convert_alpha()
        self.slct_img =  pygame.image.load("images\\sel.png")
        self.width = 224
        self.height = 64
        #calling parent constructor
        pygame.Surface.__init__(self, size=(self.width,self.height),flags=pygame.SRCALPHA)
        #filling surface with transparent color and than pasting button on it
        self.update_surface()
        thread = threading.Thread(target=self.mouse_event)
        thread.start()
        
    def update_surface(self):
        self.fill((155,200,255))
        i = 0
        for img in self.images:
            if self.selected == i:
                self.slct_img.blit(img, (2, 2))
                img = self.slct_img
            self.blit(img,((64*i)+(-self.scrollx)+32, 8))
            i += 1
        self.blit(self.left, (8,0))
        self.blit(self.right, (self.width-(self.right.get_width()+8),0))        
        
    def mouse_event(self):
        global MOUSEDOWN
        clock = pygame.time.Clock()
        # Event loop
        while True:
            clock.tick(500)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            left = pygame.mouse.get_pressed()[2]
            if left:
                if not MOUSEDOWN:
                    MOUSEDOWN = True
            elif not left:
                if MOUSEDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.left.get_rect().collidepoint((pos[0]-self.position[0],pos[1]-self.position[1])):
                        self.scrollx += 48
                        self.update_surface()
                        logging.warn("{}".format(self.scrollx))
                    if self.right.get_rect().collidepoint((pos[0]-self.position[0],pos[1]-self.position[1])):
                        if self.scrollx > 48:
                            self.scrollx -= 48
                            self.update_surface()
                    
                MOUSEDOWN = False   