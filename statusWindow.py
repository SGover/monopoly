import pygame
from pygame.locals import *
import threading

class statusWindow():
    quit = False
    def __init__(self):
        pass

    def start(self, players):
        thread = threading.Thread(target=statusWindow.run, args = (self,players))
        thread.start()
        pass
    
    def run(self, players):
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((500, 650))
        pygame.display.set_caption('Status Window')
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        # setting fonts
        font = pygame.font.Font(None, 28)
        #text values
        p = players[0]
        text = font.render(p.name, 3, (10, 10, 10))
        textpos = text.get_rect().move(15,10)
        background.blit(text, textpos)

        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or self.quit:
                    return
         
            screen.blit(background, (0, 0))
            pygame.display.flip()
    def stop(self):
            self.quit = True
