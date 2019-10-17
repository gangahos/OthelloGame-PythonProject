class Tile:
    def __init__(self, x, y, char_width, color):
        """Draws ellipse at given x,y cordinate"""
        self.x = x
        self.y = y
        self.char_width = char_width
        self.color = color

    def draw_tile(self, x_add_disc, y_add_disc, add_dist):
        """Draws either black tile or white tile at x, y cordinate"""
        STROKEWEIGHT = 5
        STROKE_COLOR = 0
        WHITE = 1
        stroke(STROKE_COLOR, STROKE_COLOR, STROKE_COLOR)
        strokeWeight(STROKEWEIGHT)
        if(self.color == WHITE):  # Drawing white tile
            RED = 255
            BLUE = 255
            GREEN = 255
            fill(RED, BLUE, GREEN)
            if(add_dist):
                ellipse((self.x+x_add_disc), (self.y+y_add_disc),
                        self.char_width, self.char_width)
            else:
                ellipse((self.x-x_add_disc), (self.y-y_add_disc),
                        self.char_width, self.char_width)

        else:  # Drawing black tile
            RED = 0
            BLUE = 0
            GREEN = 0
            fill(RED, BLUE, GREEN)
            if(add_dist):
                ellipse((self.x+x_add_disc), (self.y+y_add_disc),
                        self.char_width, self.char_width)
            else:
                ellipse((self.x-x_add_disc), (self.y-y_add_disc),
                        self.char_width, self.char_width)
