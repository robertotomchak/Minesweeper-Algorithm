# This file contains the functions that affect the game, as well as the class of the Tiles
import random


# class that defines each tile of the board
class Tile:
    # values that define the board (set to zero by default)
    N_ROWS = 0
    N_COLUMNS = 0
    N_BOMBS = 0

    win_condition = N_ROWS * N_COLUMNS - N_BOMBS  # how many free tiles we need to win

    # counts how many tiles have been freed
    freed_tiles = 0

    # counts how many "!" in the board
    marked_bombs = 0

    def __init__(self, status=0, symbol="X", coords=(0, 0)):
        self.status = status
        self.symbol = symbol
        self.coords = coords

    # returns the coordinates of adjacent tiles
    def adjacent(self):
        adjacent_tiles = []
        x, y = self.coords
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < Tile.N_ROWS and 0 <= j < Tile.N_COLUMNS and (i != x or j != y):
                    adjacent_tiles.append((i, j))
        return adjacent_tiles

    # frees the clicked tile
    # returns nothing
    def free(self, board):
        # if tile is already freed, no need to free again
        if self.symbol not in "X?":
            return None

        # if title is not a bomb, change its symbol
        self.symbol = str(self.status)
        Tile.freed_tiles += 1

        # frees all adjacent tiles. Stops when reach a tile with positive status
        for tile in self.adjacent():
            if board[tile[0]][tile[1]].status == 0:
                board[tile[0]][tile[1]].free(board)
            elif board[tile[0]][tile[1]].status != -1 and board[tile[0]][tile[1]].symbol == "X":
                board[tile[0]][tile[1]].symbol = str(board[tile[0]][tile[1]].status)
                Tile.freed_tiles += 1
        return None

    # gives a number to tiles that touch one or more bombs
    # returns nothing
    def new_status(self, board):
        # if it's a bomb or already has a number, continues to be a bomb
        if self.status != 0:
            return None

        # for each bomb, the status grows by 1
        n_bombs = 0
        for tile in self.adjacent():
            if board[tile[0]][tile[1]].status == -1:
                n_bombs += 1

        self.status = n_bombs
        return None

    # changes the symbol of a tile based on player's argument and updates number of marked bombs
    # if players tries to free a tile with a bomb, returns -1. Else, returns 0
    def action(self, player_action, board):
        if player_action == "F":
            # can't free tile with "!"
            if self.symbol == "!":
                return 0
            # game lost
            elif self.status == -1:
                self.symbol = "B"
                return -1
            # if it's a valid tile, calls the free method
            else:
                self.free(board)
                return 0
        # update number of marked bombs
        if player_action == "M":
            if self.symbol == "X":
                Tile.marked_bombs += 1
                self.symbol = "!"
            elif self.symbol == "?":
                self.symbol = "X"
            elif self.symbol == "!":
                Tile.marked_bombs -= 1
                self.symbol = "?"
        return 0


# creates an empty board (no bombs yet). By default, it's a hard mode board
# returns the empty board
def empty_board(rows=16, columns=30, bombs=99):
    Tile.N_ROWS = rows
    Tile.N_COLUMNS = columns
    Tile.N_BOMBS = bombs
    Tile.win_condition = rows * columns - bombs

    Tile.marked_bombs = 0
    Tile.freed_tiles = 0
    # create empty board
    board = [[Tile(coords=(i, j)) for j in range(Tile.N_COLUMNS)] for i in range(Tile.N_ROWS)]
    return board


# loads previous game, if exists
# returns the game board if previous game exists. Else, returns an empty list
def load_game():
    # Set values to default
    Tile.N_ROWS = 0
    Tile.N_COLUMNS = 0
    Tile.N_BOMBS = 0
    Tile.marked_bombs = 0
    Tile.freed_tiles = 0
    # status of each tile of the board
    with open("previous_game/status.txt", "r") as file:
        rows = file.read().splitlines()
        # if file is empty, there's no previous game
        if not rows:
            return [], 0
        board = []
        for i, row in enumerate(rows):
            board_row = []
            # stops when finds an empty row
            if not rows:
                break
            row = row.split(" ")
            for j, status in enumerate(row):
                if status != "":
                    board_row.append(Tile(status=int(status), coords=(i, j)))
                if status == "-1":
                    # if status is -1, it's a bomb
                    Tile.N_BOMBS += 1
            board.append(board_row)

    # symbol of each tile of the board
    with open("previous_game/symbols.txt") as file:
        rows = file.read().splitlines()
        # if file is empty, there's no previous game
        if not rows:
            return -1
        for i, row in enumerate(rows):
            # stops when finds an empty row
            if not row:
                break
            row = row.split(" ")
            for j, symbol in enumerate(row):
                if symbol:
                    board[i][j].symbol = symbol
                # if tile is known, it's a free tile
                if symbol in "012345678" and symbol != "":
                    Tile.freed_tiles += 1
                # if tile is "!", is a marked bomb
                elif symbol == "!":
                    Tile.marked_bombs += 1
            time_spent = int(rows[-1])
    # Correcting the dimensions of the game
    Tile.N_ROWS = len(board)
    Tile.N_COLUMNS = len(board[0])
    Tile.win_condition = Tile.N_ROWS * Tile.N_COLUMNS - Tile.N_BOMBS

    return board, time_spent


# saves the game when players exits
# returns nothing
def save_game(board, time_spent):
    # if board is empty, clears both files
    if not board and time_spent == 0:
        with open("previous_game/status.txt", "w") as file:
            file.write("")
        with open("previous_game/symbols.txt", "w") as file:
            file.write("")
        return None

    with open("previous_game/status.txt", "w") as file:
        for row in board:
            for tile in row:
                file.write(f"{tile.status} ")
            file.write("\n")
    with open("previous_game/symbols.txt", "w") as file:
        for row in board:
            for tile in row:
                file.write(f"{tile.symbol} ")
            file.write("\n")
        file.write(f"\n{time_spent}")


# starts the game via the first click
# returns nothing
def start_game(board, a=0, b=0, auto=False):
    # start game (first tile is defined to be with no bomb in or adjacent)
    # if auto is True, a random tile is chosen to start the game
    if auto:
        a = random.randint(0, Tile.N_ROWS-1)
        b = random.randint(0, Tile.N_COLUMNS-1)

    # bombs are not allowed in the chosen tile and adjacent tiles
    no_bombs = [(a, b)]
    no_bombs.extend(board[a][b].adjacent())

    # put bombs until finished
    board_bombs = 0
    while True:
        x, y = random.randint(0, Tile.N_ROWS-1), random.randint(0, Tile.N_COLUMNS-1)
        # if tile is not already a bomb, turns into a bomb
        if board[x][y].status != -1 and (x, y) not in no_bombs:
            board[x][y].status = -1
            board_bombs += 1

        # if contains the correct number of bombs, end
        if board_bombs == Tile.N_BOMBS:
            break

    # updates the status now that we have bombs
    for row in board:
        for tile in row:
            tile.new_status(board)

    # free selected tile
    board[a][b].free(board)

    return None


# the algorithm that plays the game by itself. It supposes that the board has already been initialized
# returns the coordinates of the changed tile and the action (free or mark)
def algorithm(board):
    for row in board:
        for tile in row:
            # if all bombs are marked, start freeing all other tiles
            if Tile.marked_bombs == Tile.N_BOMBS:
                if tile.symbol == "X":
                    return tile.coords[0], tile.coords[1], "F"

            # if tile is known and a number
            if tile.symbol in "12345678":
                # calculates number of bombs and unknown tiles
                n_bombs = 0
                n_unknown = 0
                adjacent_tiles = tile.adjacent()
                for x, y in adjacent_tiles:
                    if board[x][y].symbol == "!":
                        n_bombs += 1
                    elif board[x][y].symbol == "X":
                        n_unknown += 1

                # if we know all bombs adjacent to tile, free the other adjacent tiles
                if n_bombs == int(tile.symbol):
                    for x, y in adjacent_tiles:
                        if board[x][y].symbol == "X":
                            return x, y, "F"
                # if the number of unknowns is the same as remaining bombs, they must be bombs
                elif n_bombs + n_unknown == int(tile.symbol):
                    for x, y in adjacent_tiles:
                        if board[x][y].symbol == "X":
                            return x, y, "M"
                else:
                    pass
    # if ends loop without marking bombs or freeing tiles, try to guess a free tile
    while True:
        x = random.randint(0, Tile.N_ROWS-1)
        y = random.randint(0, Tile.N_COLUMNS-1)
        # it's only going to guess if tile is unknown
        if board[x][y].symbol in "X?":
            return x, y, "F"
