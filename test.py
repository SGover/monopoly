from mainGame import *
from gameClasses import *
from board import *
statusW = statusWindow()
board =  board(statusW)
game = monoGame(board,2)
game.start()
