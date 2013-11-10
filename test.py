from mainGame import monoGame
from statusWindow import statusWindow 
from board import board
statusW = statusWindow()
board =  board(statusW)
game = monoGame(board,2)
game.start()
