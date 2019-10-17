# Name : Ganga Hosmani
# Othello game 8x8 board. 

from board import Board
from game_controller import GameController
import time


WIDTH = 640
HEIGHT = 640
NUM_SQUARES = 8

board = Board(WIDTH, HEIGHT, NUM_SQUARES)
game_controller = GameController(WIDTH, HEIGHT, NUM_SQUARES, board)


def setup():
# Sets the background as green and calls setup_board to setup the initial
# stage of othello game
    size(WIDTH, HEIGHT)
    background(0, 100, 0)
    board.setup_board()

def draw():
# If the game_stop is not true and it is not player's turn make_computer_move 
# method is invoked and ai part places it's tile and at end set is_player_turn True
    if not game_controller.game_stop:
        game_controller.update()
        if not game_controller.is_player_turn:
            if(game_controller.computer_move and not game_controller.computer_move_done):
                time.sleep(1)
                game_controller.make_computer_move()
                game_controller.is_player_turn = True
        

def mousePressed():
# If is_player_turn is True, player can place the tile by clicking mouse.
# It waits till the player clicks in the correct place
# When player_done is True sets is_player_turn is set False   
    if(game_controller.player_move):
        game_controller.check_player_move(mouseX, mouseY)
        if(game_controller.player_done):
            game_controller.is_player_turn = False
        
        
    
    
