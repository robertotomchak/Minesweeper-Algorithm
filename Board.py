'''
    Defines the board of the minesweeper game, including all its characteristics and methods to play the game (create game, click on tiles, etc)
'''

import random

'''
Tile: each tile has two informations
    status: what the value of the tile is. -1 means there is a bomb, otherwise is equal to the number of adjacent bombs (0-8)
    symbol: what the player see. "X" means the tile is unknown, "B" shows a bomb (when game is lost), "!" tile is marked with a flag, "?" tile is marked
        with a ?, "0"-"8" the tile has already been freed and shows how many bombs are adjacent to it

    default values are related to the board before the game begins (all tiles are unknown and no bombs are placed, so all tiles have a status of 0)
'''


'''
Board: defines the board in which the game is played
@attributtes:
    n_rows, n_columns: dimensions of the board
    n_bombs: number of bombs in board
    n_marked_bombs: number of marked bombs (marked with "!")
    n_free_tiles: how many tiles have been freed (useful for game_won())
    time_spent: how much time since game started (in seconds)
    tiles: matrix of tiles (see class Tile)
    previous_game: if there was a game saved before opening
'''
class Board:
    # init takes dimensions of board and number of bombs
    def __init__(self, n_rows=0, n_columns=0, n_bombs=0, previous_game=False):
        if previous_game:
            self.load_game("previous_game/status", "previous_game/symbols", "previous_game/time")
            return None
        
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.n_bombs = n_bombs

        self.n_marked_bombs = 0
        self.n_free_tiles = 0
        self.time_spent = 0

        self.tiles_status = []
        self.tiles_symbol = []
        for i in range(n_rows):
            temp_status = []
            temp_symbol = []
            for j in range(n_columns):
                temp_status.append(0)
                temp_symbol.append("X")
            self.tiles_status.append(temp_status)
            self.tiles_symbol.append(temp_symbol)


        return None

    '''
    place_bombs: places <self.n_bombs> in the board and makes the first free click
    @parameters:
        self
        x, y: coordinates of clicked tile
    @return: none
    '''
    def place_bombs(self, x, y):
        # bombs are not allowed in the chosen tile and adjacent tiles
        no_bombs = [(x, y)]
        no_bombs.extend(self.adjacent_tiles(x, y))

        # creating a list with all possible bomb tiles
        possible_bombs = []
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if (i, j) not in no_bombs:
                    possible_bombs.append((i, j))
        random.shuffle(possible_bombs)  # shuffling to get random positions
        # putting bombs in the first <n_bombs> tiles of the list
        for a, b in possible_bombs[:self.n_bombs]:
            self.tiles_status[a][b] = -1
            # update adjacent tiles
            adj_tiles = self.adjacent_tiles(a, b)
            for coords in adj_tiles:
                if self.tiles_status[coords[0]][coords[1]] != -1:
                    self.tiles_status[coords[0]][coords[1]] += 1

        # free selected tile
        self.click(x, y, "left")

        
        return None

    
    '''
    click: all actions that happen when player clicks on a tile
    @parameters:
        self
        x, y: coordinates of tile
        action: what type of mouse click (left/right)
    @return: if player has lost or no (True = not lost, False = lost)
    '''
    def click(self, x, y, action):
        # left click = free tile
        # right click = mark tile
        if action == "left":
            return self.free_tile(x, y)
        elif action == "right":
            self.mark_tile(x, y)
            return True
        # should not happen
        else:
            print("ERROR: INVALID TYPE OF CLICK")
            return False


    '''
    adjacent_tiles: gets tiles adjacent to desired tile
    @parameters:
        self
        x, y: coordinates of tile
    @return: list of coordinates (x,y) of adjacent tiles
    '''
    def adjacent_tiles(self, x, y):
        tiles = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < self.n_rows and 0 <= j < self.n_columns and (i != x or j != y):
                    tiles.append((i, j))
        return tiles
    

    '''
    free_tile: frees given tile
    @parameters:
        self
        x, y: coordinates of given tile
    @return: if player has lost or no (True = not lost, False = lost)
    '''
    def free_tile(self, x, y):
        # can't free tile that has already been freed or marked with flag (flag = "!")
        if self.tiles_symbol[x][y] not in "X?":
            return True

        # if tile is a bomb, game is lost
        if self.tiles_status[x][y] == -1:
            self.tiles_symbol[x][y] = "B"
            return False
        
        # if tile is not a bomb, free it and possibly its adjacent tiles
        self.tiles_symbol[x][y] = str(self.tiles_status[x][y])
        self.n_free_tiles += 1

        # if tile is a number greater than zero, don't free adjacent tiles
        if self.tiles_symbol[x][y] in "12345678":
            return True

        # frees all adjacent tiles. Stops when reach a tile with positive status
        for coords in self.adjacent_tiles(x, y):
            self.free_tile(coords[0], coords[1])

        return True


    '''
    mark_tile: marks given tile (flag or ?)
    @parameters:
        self
        x, y: coordinates of given tile
    @return: None
    '''
    def mark_tile(self, x, y):
        # "X" -> "!" -> "?" -> "X"
        # TO-DO: maybe add those wierd variables of the algorithm
        tile_symbol = self.tiles_symbol[x][y]
        if tile_symbol == "!":
            self.tiles_symbol[x][y] = "?"
            self.n_marked_bombs -= 1
        elif tile_symbol == "?":
            self.tiles_symbol[x][y] = "X"
        elif tile_symbol == "X":
            self.tiles_symbol[x][y] = "!"
            self.n_marked_bombs += 1
        else:
            pass
        return None
    

    '''
    game_won: calculates if game has been won
    @parameters:
        self
    @return: True if game is won; False otherwise (game still not finished)
    '''
    def game_won(self):
        # game is won when all tiles that don't have a bomb have been freed
        return self.n_free_tiles + self.n_bombs == self.n_rows * self.n_columns
    

    '''
    load_game: loads previous game (only called if there is one)
    @parameters:
        self
        status_file: path to file that contains the status of the tiles
        symbols_file: path to file that contains the symbols of the tiles
        time_file: path to file that contains the time spent
    @return: None
    '''
    def load_game(self, status_file, symbols_file, time_file):
        self.tiles_status = []  # matrix of status of tiles
        self.tiles_symbol = []  # matrix of symbols of tiles

        with open(status_file, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                status_line = [int(status) for status in line.split(" ")]
                self.tiles_status.append(status_line)
        with open(symbols_file, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                symbols_line = [symbol for symbol in line.split(" ")]
                self.tiles_symbol.append(symbols_line)
        with open(time_file, "r") as file:
            self.time_spent = float(file.read().splitlines()[0])


        self.n_rows = len(self.tiles_status)
        self.n_columns = len(self.tiles_status[0])
        self.n_bombs = 0
        self.n_marked_bombs = 0
        self.n_free_tiles = 0
        for line_status, line_symbol in zip(self.tiles_status, self.tiles_symbol):
            for status, symbol in zip(line_status, line_symbol):
                if status == -1:
                    self.n_bombs += 1
                if symbol == "!":
                    self.n_marked_bombs += 1
                elif symbol in "012345678":
                    self.n_free_tiles += 1
        return None


    '''
    save_game: saves game when closed (only called if game wasn't finished)
    @parameters:
        self
        status_file: path to file that contains the status of the tiles
        symbols_file: path to file that contains the symbols of the tiles
        time_file: path to file that contains the time spent
    @return: None
    '''
    def save_game(self, status_file, symbols_file, time_file):
        content_status = ""  # string with content of the status of the tiles
        content_symbols = ""  # string with content of the symbols of the tiles
        for line_status, line_symbol in zip(self.tiles_status, self.tiles_symbol):
            for status, symbol in zip(line_status, line_symbol):
                content_status = content_status + str(status) + " "
                content_symbols = content_symbols + symbol + " "
            # adding new line and removing last blank space
            content_status = content_status[:-1] + "\n"
            content_symbols = content_symbols[:-1] + "\n"
        # removing extra new line
        content_status = content_status[:-1]
        content_symbols = content_symbols[:-1]

        # wrinting into files
        with open(status_file, "w") as file:
            file.write(content_status)
        with open(symbols_file, "w") as file:
            file.write(content_symbols)
        with open(time_file, "w") as file:
            file.write(str(self.time_spent))
        return None
