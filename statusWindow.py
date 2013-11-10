import pygame
from board import P_COLORS

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

class statusWindow():
    players = []
    def __init__(self):
        pass

    def start(self, players):
        self.players = players
        # setting fonts
        pygame.font.init()
        self.fnt_name = pygame.font.Font(None, 28)
        self.fnt_money = pygame.font.Font(None, 24)
        self.fnt_asset = pygame.font.Font(None, 16)
            
    def draw(self, background):
        l = 0
        for p in self.players:
            height = l * 200
            txt_name = self.fnt_name.render(p.name, 3, P_COLORS[l])
            textpos = txt_name.get_rect().move(X+15,10+height)
            background.blit(txt_name, textpos)
            
            txt_money = self.fnt_money.render("$"+str(p.money), 3, (10, 10, 10))
            textpos = txt_money.get_rect().move(X+350,20+height)
            background.blit(txt_money, textpos)
            
            i = 0
            for c in p.assets:
                color = COLORS[c]
                text = ""
                for asset in p.assets[c]:
                    text = text + asset.name + " | " 
                txt_money = self.fnt_asset.render(text, 3, color)    
                textpos = txt_money.get_rect().move(X+10,50+height+(i*20))
                background.blit(txt_money, textpos)
                i += 1
            l += 1    
        return background
    
