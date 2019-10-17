from tile import Tile


class Board():
    """Draws Board and tiles"""

    def __init__(self, WIDTH, HEIGHT, NUM_SQUARES):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NUM_SQUARES = NUM_SQUARES
        self.HALF_SQUARES = NUM_SQUARES//2
        self.TOTAL_SQUARES = self.NUM_SQUARES**2
        self.CHAR_WIDTH = self.WIDTH//(self.NUM_SQUARES+1)
        self.MUL_FACTOR_2 = 2
        self.ADD1_FACTOR = 1
        self.BLACK = 0
        self.WHITE = 1
        self.X1 = self.WIDTH/self.NUM_SQUARES
        self.Y1 = self.HEIGHT/self.NUM_SQUARES
        self.CELL_WIDTH = self.WIDTH//self.NUM_SQUARES
        self.INITIAL_SQUARE = (self.NUM_SQUARES)//2 - 1
        self.FIRST_TILE = self.CELL_WIDTH*self.INITIAL_SQUARE
        self.color = self.BLACK
        self.board_full = False
        self.x_add_disc = self.WIDTH/(self.NUM_SQUARES*self.MUL_FACTOR_2)
        self.y_add_disc = self.HEIGHT/(self.NUM_SQUARES*self.MUL_FACTOR_2)
        self.list_tiles = []
        self.board_cord = []

    def setup_board(self):
        """Draw Board with black lines and green background calls method
        to create board_cord list, place initial four tiles
        and create list_tiles"""
        STROKEWEIGHT = 5
        ZERO_CORD = 0
        for i in range(1, self.NUM_SQUARES+1):
            stroke(self.BLACK, self.BLACK, self.BLACK)
            strokeWeight(STROKEWEIGHT)
            x_i = self.X1*i
            line(x_i, ZERO_CORD, x_i, self.HEIGHT)
        for i in range(1, self.NUM_SQUARES+1):
            stroke(self.BLACK, self.BLACK, self.BLACK)
            strokeWeight(STROKEWEIGHT)
            y_i = self.Y1*i
            line(ZERO_CORD, y_i, self.WIDTH, y_i)

        self.board_pattern()
        self.place_initial_tile()

    def board_pattern(self):
        """Creates board_cord list which has coordinates of each square of the
        board. For the initial four tiles the indexes are updated as None"""
        for j in range(1, (self.NUM_SQUARES+1)):
            y_part = (self.HEIGHT/self.NUM_SQUARES)*j
            local_cord = []
            for i in range(1, (self.NUM_SQUARES+1)):
                x_part = (self.WIDTH/self.NUM_SQUARES)*i
                local_cord.append((y_part, x_part))
            self.board_cord.append(local_cord)

        self.board_cord[self.INITIAL_SQUARE][self.INITIAL_SQUARE] = None
        self.board_cord[self.INITIAL_SQUARE][self.HALF_SQUARES] = None
        self.board_cord[self.HALF_SQUARES][self.INITIAL_SQUARE] = None
        self.board_cord[self.HALF_SQUARES][self.HALF_SQUARES] = None

    def check_board(self):
        """Checks if the board is full by iterating list board_cord"""
        INITIAL_VALUE = 0
        check_count = INITIAL_VALUE
        found_cord = False
        for j in range(self.NUM_SQUARES):
            for i in range(self.NUM_SQUARES):
                if(self.board_cord[j][i] is None):
                    check_count += 1
                else:
                    found_cord = True
                    break
            if found_cord:
                break
        if(check_count == self.TOTAL_SQUARES):
            self.board_full = True
        return self.board_full

    def create_list_tiles(self):
        """Creates the list_tiles and initializes all values as None"""
        for j in range(self.NUM_SQUARES):
            local_tiles = []
            for i in range(self.NUM_SQUARES):
                local_tiles.append(None)
            self.list_tiles.append(local_tiles)

    def is_board_cord_valid(self, inp_j, inp_i):
        """Checks if the index on the board_cord[][] is None or holds
        xy coordinate value"""
        if(self.board_cord[inp_j][inp_i] is not None):
            return(True)
        else:
            return(False)

    def check_color_tile(self, inp_row, inp_col, inp_color):
        """This function checks if the color of the tile at given
        row colum in list_tiles matches inp_color"""
        if self.list_tiles[inp_row][inp_col] is not None:
            tile = self.list_tiles[inp_row][inp_col]
            if tile.color == inp_color:
                return True
        return False

    def flip_tiles(self, list_tiles_flip, inp_color):
        """Calculates x and y cordinates for each tile in list_tiles_flip"""
        for elem in list_tiles_flip:
            row, col = elem
            y_tile = (row+self.ADD1_FACTOR)*self.CELL_WIDTH
            x_tile = (col+self.ADD1_FACTOR)*self.CELL_WIDTH
            self.place_player_tile(x_tile, y_tile, inp_color, board_update=False)

    def place_initial_tile(self):
        """Places the first four tiles and update the list_tiles accordingly"""
        self.create_list_tiles()
        add_dist = True
        x_tile = (self.FIRST_TILE)
        y_tile = (self.FIRST_TILE)
        color = self.WHITE
        tile = Tile(x_tile, y_tile, self.CHAR_WIDTH, color)
        self.list_tiles[self.HALF_SQUARES-1][self.HALF_SQUARES-1] = tile
        tile.draw_tile(self.x_add_disc, self.y_add_disc, add_dist)

        x_tile = (self.FIRST_TILE+self.CELL_WIDTH)
        y_tile = (self.FIRST_TILE)
        color = self.BLACK
        tile = Tile(x_tile, y_tile, self.CHAR_WIDTH, color)
        self.list_tiles[self.HALF_SQUARES-1][self.HALF_SQUARES] = tile
        tile.draw_tile(self.x_add_disc, self.y_add_disc, add_dist)

        x_tile = (self.FIRST_TILE)
        y_tile = (self.FIRST_TILE+self.CELL_WIDTH)
        color = self.BLACK
        tile = Tile(x_tile, y_tile, self.CHAR_WIDTH, color)
        self.list_tiles[self.HALF_SQUARES][self.HALF_SQUARES-1] = tile
        tile.draw_tile(self.x_add_disc, self.y_add_disc, add_dist)

        x_tile = (self.FIRST_TILE+self.CELL_WIDTH)
        y_tile = (self.FIRST_TILE+self.CELL_WIDTH)
        color = self.WHITE
        tile = Tile(x_tile, y_tile, self.CHAR_WIDTH, color)
        self.list_tiles[self.HALF_SQUARES][self.HALF_SQUARES] = tile
        tile.draw_tile(self.x_add_disc, self.y_add_disc, add_dist)

    def place_player_tile(self, inp_x_tile, inp_y_tile, inp_color,
                          board_update=True):
        """Places the tile on the board and updates board_cord list"""
        valid_tile = 0
        add_dist = False
        tile = Tile(inp_x_tile, inp_y_tile, self.CHAR_WIDTH, inp_color)
        tile.draw_tile(self.x_add_disc, self.y_add_disc, add_dist)

        if board_update:
            for j in range(self.NUM_SQUARES):
                for i in range(self.NUM_SQUARES):
                    if(self.board_cord[j][i] == (inp_y_tile, inp_x_tile)):
                        valid_tile = 1
                        self.board_cord[j][i] = None
                        row = j
                        col = i
                        break
                    elif(self.board_cord[j][i] is None):
                        valid_tile = 0
                if(valid_tile == 1):
                    break
            self.list_tiles[row][col] = tile
        else:
            row = (inp_y_tile/self.CELL_WIDTH)-self.ADD1_FACTOR
            col = (inp_x_tile/self.CELL_WIDTH)-self.ADD1_FACTOR
            self.list_tiles[row][col] = tile

    def place_temp_tile(self, row, col, inp_color):
        """Instantiates object of classs Tile and adds
        the tile object to self.list_tiles"""
        x_cord, y_cord = self.board_cord[row][col]
        tile = Tile(x_cord, y_cord, self.CHAR_WIDTH, inp_color)
        self.list_tiles[row][col] = tile

    def remove_temp_tile(self, row, col):
        """Updates the value at given row and column in
        self.list_tiles as None"""
        self.list_tiles[row][col] = None
