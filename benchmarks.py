# THIS FILE IS NOT A PART OF THE MINESWEEPER GAME AND DOES NOT AFFECT THE OTHER FILES
# The objective of this file is only to test the algorithm, to see how well it is doing
# Prints out how many games (in %) the algorithm won, as well as its average speed (divided between wins and losses)
import functions
import time


# Changes these values to test the algorithm
N = 10000  # number of games to be played
mode = "hard"  # mode selected (can be "easy", "normal" or "hard")

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


results = []
total_wins = 0
time_wins = []
time_loses = []

for i in range(N):
    print(i) if i % 100 == 0 else None
    board = functions.empty_board(rows, columns, bombs)
    functions.start_game(board, auto=True)
    start = time.time()
    while True:
        x, y, action = functions.algorithm(board)
        if board[x][y].action(action, board) == -1:
            value = -1
            break
        if functions.Tile.freed_tiles == functions.Tile.win_condition:
            value = 0
            break
    end = time.time()
    if value == 0:
        results.append({"won?": True, "time": (end - start)})
        total_wins += 1
        time_wins.append((end - start))
    else:
        results.append({"won?": False, "time": (end - start)})
        time_loses.append((end - start))

print(f"% of Wins: {round((total_wins / N)*100, 2)}")
print(f"Average Time of Wins: {sum(time_wins) / len(time_wins)}")
print(f"Average Time of Loses: {sum(time_loses) / len(time_loses)}")
