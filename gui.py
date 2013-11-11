import pygame
from pygame.locals import *  
import threading

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
                    if pos[0] >= self.position[0] and pos[1] >= self.position[1]:
                        if pos[0] <= self.position[0]+self.width and pos[1] <= self.position[1]+self.height:
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