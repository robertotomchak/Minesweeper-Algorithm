# THIS FILE IS NOT A PART OF THE MINESWEEPER GAME AND DOES NOT AFFECT THE OTHER FILES
# The objective of this file is only to test the algorithm, to see how well it is doing
# this file creates a csv that contains data about the games played, which are analysed
# in the "Algorithm_Analysis.ipynb" file
import algorithm
import functions
import time
import pandas as pd


# Changes these values to test the algorithm
N = 10000  # number of games to be played
mode = "normal"  # mode selected (can be "easy", "normal" or "hard")

if mode == "easy":
    rows = 9
    columns = 9
    bombs = 10
elif mode == "normal":
    rows = 16
    columns = 16
    bombs = 40
elif mode == "hard":
    rows = 30
    columns = 16
    bombs = 99
else:
    rows = 0
    columns = 0
    bombs = 0


data = []

for i in range(N):
    game_data = {}  # saves data about the game
    strategies = []  # saves used strategies
    print(i) if i % 100 == 0 else None
    board = functions.empty_board(rows, columns, bombs)
    functions.start_game(board, auto=True)
    start = time.time()
    while True:
        x, y, action, strategy = algorithm.algorithm(board)
        if str(strategy) not in strategies:
            strategies.append(str(strategy))
        # game lost
        if board[x][y].action(action, board) == -1:
            value = 0
            break
        # game won
        if functions.Tile.freed_tiles == functions.Tile.win_condition:
            value = 1
            break
    end = time.time()
    game_data["id"] = i + 1
    game_data["won"] = value
    game_data["time"] = end - start
    game_data["main_strategy"] = strategy
    strategies.sort()
    game_data["strategies"] = "".join(strategies)
    data.append(game_data)

# export data to a csv file
df = pd.DataFrame(data)
df.to_csv("minesweeper_data", index=False)

print(100 * df["won"].mean())
print(df[df["won"] == 1]["time"].mean())
print(df[df["won"] == 0]["time"].mean())
