'''
This file's objective is to test the minesweeper solver by playing various games in a certain difficulty
It does not affect the interface
To get more accurate results, no interface is used, just the algorithm playing the game using the Board object
Change the constants N and MODE to make different analysis
All data is stored in the "minesweeper_data.csv" file, and some of the results are outputted at the end
'''
from Algorithm import Algorithm
from Board import Board
import time
import pandas as pd
from random import randint


# Changes these isWins to test the algorithm
N = 10000  # number of games to be played
MODE = "hard"  # mode selected (can be "easy", "normal" or "hard")

if MODE == "easy":
    rows = 9
    columns = 9
    bombs = 10
elif MODE == "normal":
    rows = 16
    columns = 16
    bombs = 40
elif MODE == "hard":
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
    print(i) if i % (N // 100) == 0 else None
    board = Board(rows, columns, bombs)
    algorithm_player = Algorithm(board.tiles_symbol, board.n_rows, board.n_columns, return_strategy=True)
    board.place_bombs(*algorithm_player.first_play())
    array_strategies = ""
    start = time.time()
    while True:
        x, y, action, strategy = algorithm_player.play()
        array_strategies += strategy
        # game lost
        if not board.click(x, y, action):
            isWin = False
            break
        # game won
        if board.game_won():
            isWin = True
            break
    end = time.time()
    game_data["id"] = i + 1
    game_data["won"] = isWin
    game_data["time"] = end - start
    game_data["strategies"] = array_strategies
    data.append(game_data)

# export data to a csv file
df = pd.DataFrame(data)
df.to_csv("minesweeper_data.csv", index=False)

# basic analysis
print(f"Total Number of Games: {N}")
print(f"Win Rate: {100 * df['won'].mean()}")
print(f"Average Time (in seconds): {df['time'].mean()}")
print(f"Average Number of Plays: {df['strategies'].apply(len).mean()}")
