# This file contains the algorithm that plays the game, as well as some functions that help the algorithm play the game
import functions
import random


# calculates all possible scenarios for that tile
# returns a list with the coordinates of the possible bombs
def possibilities(board, tile):
    possible_scenarios = []  # saves the possible scenarios
    # loops for each scenario
    for x, y in tile.adjacent():
        possible = True  # by default, a scenario is possible
        # supposes there's a bomb in the board[x][y] tile (can only put bombs in unknown tiles)
        if board[x][y].symbol != "X":
            continue
        # checks if scenario is possible
        for a, b in board[x][y].adjacent():
            if board[a][b].symbol in "12345678":
                # tile has more bombs marked than possible
                if int(board[a][b].symbol) < board[a][b].adjacent_bombs + 1:
                    possible = False
        if possible:
            possible_scenarios.append((x, y))
    return possible_scenarios


# simulates what would happen in each scenario, based on tiles that have possible_bombs and known tiles
# returns the actions that are common in all scenarios
def simulate(possible_bombs, tiles, board):
    actions = []
    for tile in tiles:
        tile_actions = []
        # suppose that a certain possible_bomb is a bomb
        for bomb in possible_bombs:
            scenario_actions = []
            a, b = tile  # coordinates of tile
            x, y = bomb  # coordinates of supposed bomb
            board[x][y].suppose_status = -1
            scenario_actions.append((x, y, "M"))
            # all other possible_bombs must be "freed"
            for not_bomb in possible_bombs:
                if not_bomb != bomb:
                    x_, y_ = not_bomb
                    board[x_][y_].suppose_status = 1
                    scenario_actions.append((x_, y_, "F"))
            # check if tile is "solved" (the two previous steps are enough)
            if board[a][b].adjacent_unknowns - len(possible_bombs) == 0:
                continue
            # check if adjacent tiles can be "freed"
            elif board[a][b].adjacent_bombs + 1 == int(board[a][b].symbol):
                for x2, y2 in board[a][b].adjacent():
                    if board[x2][y2].symbol == "X" and board[x2][y2].suppose_status == 0:
                        scenario_actions.append((x2, y2, "F"))
            # check if adjacent tiles can be "marked"
            elif board[a][b].adjacent_unknowns - len(possible_bombs) == int(board[a][b].symbol) - \
                    board[a][b].adjacent_bombs - 1:
                for x2, y2 in board[a][b].adjacent():
                    if board[x2][y2].symbol == "X" and board[x2][y2].suppose_status == 0:
                        scenario_actions.append((x2, y2, "M"))
            else:
                pass
            # saves actions to tile_actions
            tile_actions.append(scenario_actions)

        # after all the simulations for that tile, we only want the actions that happened in all simulations
        if tile_actions == []:
            continue
        actual_tile_actions = set(tile_actions[0])
        for possible_actions in tile_actions[1:]:
            actual_tile_actions = actual_tile_actions & set(possible_actions)
        for action in actual_tile_actions:
            actions.append(action)
    return actions


# the algorithm that plays the game by itself. It supposes that the board has already been initialized
# returns the coordinates of the changed tile and the action (free or mark)
def algorithm(board):
    for row in board:
        for tile in row:
            # if all bombs are marked, start freeing all other tiles
            if functions.Tile.marked_bombs == functions.Tile.N_BOMBS:
                if tile.symbol == "X":
                    return tile.coords[0], tile.coords[1], "F", 1
                else:
                    pass

            # if tile is known and it's a number
            elif tile.symbol in "12345678":
                # if no unknown tiles are adjacent, tile is solved
                if tile.adjacent_unknowns == 0:
                    continue
                # if we know all bombs adjacent to tile, free the other adjacent tiles
                if tile.adjacent_bombs == int(tile.symbol):
                    for x, y in tile.adjacent():
                        if board[x][y].symbol == "X":
                            return x, y, "F", 1
                # if the number of unknowns is the same as remaining bombs, they must be bombs
                elif tile.adjacent_unknowns + tile.adjacent_bombs == int(tile.symbol):
                    for x, y in tile.adjacent():
                        if board[x][y].symbol == "X":
                            return x, y, "M", 1

                else:
                    pass
            else:
                pass

    # if none of the previous strategies worked, try to find the bomb via possible scenarios
    for row in board:
        for tile in row:
            # if tile is known, it's a number and only one bomb left
            if tile.symbol in "12345678" and int(tile.symbol) - tile.adjacent_bombs == 1:
                possible_bombs = possibilities(board, tile)
                # get adjacent tiles that are common to all possible_bombs and are not solved numbers
                if len(possible_bombs) == 0:
                    continue
                x, y = possible_bombs[0]
                adjacents = set([(a, b) for a, b in board[x][y].adjacent() if board[a][b].symbol
                                 in "12345678" and board[a][b].adjacent_unknowns != 0])
                for bomb in possible_bombs[1:]:
                    x, y = bomb
                    adjacents = adjacents & set(board[x][y].adjacent())
                # simulate scenarios to get common actions
                actions = simulate(possible_bombs, adjacents, board)
                for x, y, action in actions:
                    return x, y, action, 2

    # if ends loop without marking bombs or freeing tiles, try to guess a free tile
    while True:
        x = random.randint(0, functions.Tile.N_ROWS-1)
        y = random.randint(0, functions.Tile.N_COLUMNS-1)
        # it's only going to guess if tile is unknown
        if board[x][y].symbol in "X?":
            return x, y, "F", 3
