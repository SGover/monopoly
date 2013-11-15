from mainGame import monoGame
from statusWindow import statusWindow 
from board import board
from gameClasses import player
statusW = statusWindow()
board =  board(statusW)
#game = monoGame(board,players=[player("adeel",900),player("tariq",900)])    
game = monoGame(board,num_players=2)  #NO more than 3 plz
game.start()
