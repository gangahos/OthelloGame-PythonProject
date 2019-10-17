from board import Board
import time
import re
import os


class GameController:
    """Maintains the state of the game."""

    def __init__(self, WIDTH, HEIGHT, NUM_SQUARES, board):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NUM_SQUARES = NUM_SQUARES
        self.CELL_WIDTH = self.WIDTH//self.NUM_SQUARES
        self.ADD1_FACTOR = 1
        self.NUM_ROWS = self.NUM_SQUARES - 1
        self.NUM_COL = self.NUM_SQUARES - 1
        self.player_move = False
        self.computer_move = False
        self.board = board
        self.WHITE = 1
        self.BLACK = 0
        self.valid_move_dict = {}
        self.list_tiles_flip = []
        self.is_player_turn = True
        self.game_stop = False
        self.player_done = False
        self.print_player_turn = True
        self.score_string = ""
        self.computer_move_done = True

    def update(self):
        """Checks if board is full, if not creates valid moves and sets
        player_move and computer_move accordingly. Calls calculate_winner
        to declare who has won the game."""
        SLEEP_TIME = 0.5
        if(self.board.check_board()):
            self.find_winner()
        else:
            if(self.is_player_turn):
                self.create_valid_move(self.BLACK, self.WHITE)
                if(bool(self.valid_move_dict)):
                    if(self.print_player_turn):
                        print("PLAYER'S TURN")
                    self.player_move = True
                else:
                    if(self.print_player_turn):
                        print("PLAYER'S TURN")
                        print("NO MORE VALID MOVES :(")
                    time.sleep(SLEEP_TIME)
                    self.player_move = False
                    self.is_player_turn = False
                self.print_player_turn = False
            else:
                self.create_valid_move(self.WHITE, self.BLACK)
                if(bool(self.valid_move_dict)):
                    time.sleep(SLEEP_TIME)
                    print("COMPUTER'S TURN")
                    self.computer_move = True
                    time.sleep(SLEEP_TIME)
                    self.computer_move_done = False
                else:
                    print("COMPUTER'S TURN")
                    print("NO MORE VALID MOVES :(")
                    self.computer_move = False
                    self.is_player_turn = True
                time.sleep(SLEEP_TIME)
                self.print_player_turn = True

        if(not(self.player_move) and not(self.computer_move)):
            self.find_winner()

    def find_winner(self):
        """Counts the number of black tiles and white tiles on the board
        and declares the winner accordingly. Also calls input function which
        asks for the user to enter their name and calls update_score_file
        function to maintain scores.txt file."""
        TEXTSIZE = 40
        RED = 255
        GREEN = 0
        BLUE = 0
        self.game_stop = True
        black_tiles = 0
        white_tiles = 0
        empty_cell = 0
        HEIGHT_4 = self.HEIGHT//4
        HEIGHT_2 = self.HEIGHT//2
        WIDTH = self.WIDTH//10
        for j in range(self.NUM_SQUARES):
            for i in range(self.NUM_SQUARES):
                if(self.board.list_tiles[j][i] is None):
                    empty_cell += 1
                elif(self.board.list_tiles[j][i].color == 1):
                    white_tiles += 1
                else:
                    black_tiles += 1
        print("Game Ended, Please enter your name")
        player_name = self.input()
        player_string = player_name.capitalize() + " Wins!"
        self.score_string = str(player_name)+" "+str(black_tiles)+"\n"
        self.update_score_file()

        textSize(TEXTSIZE)
        fill(RED, GREEN, BLUE)
        text("GAME ENDED!!!", WIDTH, HEIGHT_2)

        if(white_tiles > black_tiles):
            final_string = "Computer Wins!, has " + str(white_tiles) + "Tiles"
            text(final_string, WIDTH,
                 HEIGHT_2+self.CELL_WIDTH)
        elif(white_tiles < black_tiles):
            final_string = player_string + ",has  " + str(black_tiles) + "Tiles"
            text(final_string, WIDTH, HEIGHT_2+self.CELL_WIDTH)
        else:
            text("IT's A TIE!!!", WIDTH, HEIGHT_2+self.CELL_WIDTH)

    def update_score_file(self):
        """If a file scores.txt exists, updates the same file with player's score.
        If scores.txt does not exist creates one and updates it with player's
        score. The scores are sorted in descending order"""
        read = False
        prev_score = ""
        is_new_score_written = False
        try:
            rd_file = open("scores.txt", "r")
            read = True
        except:
            print("Creating scores.txt to maintain score")
            wr_file = open("scores.txt", "w")
        if read:
            temp_file = open("temp.txt", "w")
            list_player_score = self.score_string.split(" ")
            file_list = rd_file.readlines()
            for line in file_list:
                list_file_score = line.split(" ")
                prev_score = re.sub('\n', "", list_file_score[-1])
                if(int(list_player_score[-1]) > int(prev_score) and
                        not is_new_score_written):
                    is_new_score_written = True
                    temp_file.write(self.score_string)
                    temp_file.write(line)
                else:
                    temp_file.write(line)
            if not is_new_score_written:
                temp_file.write(self.score_string)
            rd_file.close()
            temp_file.close()
            temp_file = open("temp.txt", "r")
            in_file = open("scores.txt", "w")
            temp_list = temp_file.readlines()
            for line in temp_list:
                in_file.write(line)
            in_file.close()
            temp_file.close()
            os.remove("temp.txt")
        else:
            wr_file.write(self.score_string)
            wr_file.close()

    def input(self, message=''):
        """To enter the player's name"""
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)

    def create_valid_move(self, inp_color, inp_opp_color):
        """Iterates through each row and column of the board. Places the tile
        in each cell of list_tiles, checks in 8 direction around it to find one
        or more opposite color tile ending in same color tile.
        If valid, creates dictionary with key as the cordinate of this cell
        and list of tiles to flip as its value.Then remove this tile from
        list_tiles"""
        self.valid_move_dict = {}
        for row in range(self.NUM_SQUARES):
            for col in range(self.NUM_SQUARES):
                list_tiles_flip = []
                if(self.board.is_board_cord_valid(row, col)):
                    self.board.place_temp_tile(row, col, inp_color)
                    for x_d, y_d in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1],
                                     [1, -1], [-1, -1], [-1, 1]]:
                        row_st = row
                        col_st = col
                        row_st += x_d
                        col_st += y_d
                        if(self.is_valid_index(row_st, col_st) and
                                self.board.check_color_tile(row_st, col_st,
                                                            inp_opp_color)):
                            row_st += x_d
                            col_st += y_d
                            if(not(self.is_valid_index(row_st, col_st))):
                                continue
                            while(self.board.check_color_tile(row_st, col_st,
                                                              inp_opp_color)):
                                row_st += x_d
                                col_st += y_d
                                if(not(self.is_valid_index(row_st, col_st))):
                                    break
                            if(not(self.is_valid_index(row_st, col_st))):
                                continue
                            if(self.board.check_color_tile(row_st, col_st,
                                                           inp_color)):
                                while True:
                                    row_st -= x_d
                                    col_st -= y_d
                                    if(row_st == row and col_st == col):
                                        break
                                    list_tiles_flip.append((row_st, col_st))
                                y_cord = (row+self.ADD1_FACTOR)*self.CELL_WIDTH
                                x_cord = (col+self.ADD1_FACTOR)*self.CELL_WIDTH
                                self.valid_move_dict[(
                                    y_cord, x_cord)] = list_tiles_flip

                    self.board.remove_temp_tile(row, col)

    def is_valid_index(self, row_st, col_st):
        """Checks if the index is within the list_tiles size"""
        if(row_st >= 0 and row_st <= self.NUM_ROWS and col_st >= 0 and
                col_st <= self.NUM_COL):
            return True
        else:
            return False

    def check_player_move(self, mousex, mousey):
        """Takes the mousepressed input and checks if it is valid index
        and places the tile on the board and flips the tiles accordingly.
        and set self.player_done = TRUE"""
        list_tiles_flip = []
        vaild_cord_board = False
        valid_player_xy = False

        for j in range(1, (self.NUM_SQUARES+1)):
            y_tile = (self.HEIGHT/self.NUM_SQUARES)*j
            if(mousey < y_tile):
                for i in range(1, (self.NUM_SQUARES+1)):
                    x_tile = (self.WIDTH/self.NUM_SQUARES)*i
                    if(mousex <= x_tile):
                        yx_tuple = (y_tile, x_tile)
                        vaild_cord_board = True
                        break
                break
        if vaild_cord_board:
            for key in self.valid_move_dict.keys():
                if(key == yx_tuple):
                    self.board.place_player_tile(x_tile, y_tile, self.BLACK)
                    list_tiles_flip = self.valid_move_dict[key]
                    self.board.flip_tiles(list_tiles_flip, self.BLACK)
                    valid_player_xy = True
        if valid_player_xy:
            self.player_done = True
        else:
            self.player_done = False

    def make_computer_move(self):
        """When computer_move is set TRUE, this function puts white tile
        on the board. It checks self.valid_move_dict, the key(cordinate)
        whose value which is list of tiles to flip, whichever is
        maximum length is used"""
        INITIAL_VALUE = 0
        list_tiles_flip = []
        max_len = INITIAL_VALUE
        for key in self.valid_move_dict.keys():
            if(len(self.valid_move_dict[key]) > max_len):
                yx_tuple = key
                list_tiles_flip = self.valid_move_dict[key]
                max_len = len(self.valid_move_dict[key])
        y_tile, x_tile = yx_tuple
        self.board.place_player_tile(x_tile, y_tile, self.WHITE)
        self.board.flip_tiles(list_tiles_flip, self.WHITE)
        self.computer_move_done = True
