import pygame
from pygame.locals import *
import threading

class statusWindow():
    quit = False
    players = []
    def __init__(self):
        pass

    def start(self, players):
        self.players = players
        thread = threading.Thread(target=self.run)
        thread.start()
    
    def run(self):
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((500, 650))
        pygame.display.set_caption('Status Window')
        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        
        # setting fonts
        fnt_name = pygame.font.Font(None, 28)
        fnt_money = pygame.font.Font(None, 24)
        
        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or self.quit:
                    return
            background.fill((250, 250, 250))
            #text values
            p = self.players[0]
            txt_name = fnt_name.render(p.name, 3, (10, 10, 10))
            textpos = txt_name.get_rect().move(15,10)
            background.blit(txt_name, textpos)
            
            txt_money = fnt_money.render("$"+str(p.money), 3, (10, 10, 10))
            textpos = txt_money.get_rect().move(400,20)
            background.blit(txt_money, textpos)
        
            screen.blit(background, (0, 0))
            pygame.display.flip()
    
    
    def stop(self):
            self.quit = True
