# MINESWEEPER ALGORITHM
### Video Demo:  https://youtu.be/3HaNfj8fxaQ (obs: the project had some changes compared to when I created it to the CS50 course)
### Description:
This is a minesweeper game. Other than the usual content of a minesweeper, it also contains an algorithm who solves the game for you.

In the images folder, you will find all images used in this project. Most of them where either created by me or collected via screenshots of the original minesweeper game, but some icons where collected on the internet. Here are the references:
-Bomb image: https://www.flaticon.com/free-icons/bomb"

-Flag image: https://www.flaticon.com/free-icons/destination"

In the previous_game folder, there are two text files that saves the game when the players exists.

Before explaining the python codes, here's a short explanation of the terms used:
-Adjacent: we refer to "adjacent tiles" all the eight tiles around;
-Free: free a tile means to left click on it. If you free a tile that has a bomb, you lose the game. Otherwise, you will see the content of that tile, which can be a number or nothing, depending on how many bombs are adjacent to it;
-Mark: mark a tile means to right click on it. If it's just an unknown tile, it marks with a flag (or "!" inside the code). If it has a flag, it's marked with a question mark (?), and if it has a question mark, it goes back to an unknown tile;
-Status: the status of a tile is the content is has. It can be 0 if it has no bombs adjacent, 1 to 8 depending on how many bombs are adjacent, and -1 if itself has a bomb. The player does not have access to a tile's status;
-Symbol: the symbol of a tile is what the player sees on the interface. If it's an unknown tile, it can be "X", "!" or "?", depending on how many times it was marked. If it's known, it can be a number between 0 and 8, depending on how many bombs are adjacent (the 0 symbol appears as just a free tile on the interface).

If you want to know more about the rules of minesweeper, check out https://freeminesweeper.org/how-to-play-minesweeper.php (this is also the link of the "how to play" buttn inside the codes's interface).

There are 4 Python codes (.py) and 1 Jupyter Notebook file (.ipynb) in this project:
-functions: contains all functions that affect the minesweeper board, as well as a class for the tiles. They allow the player to play the game;
-algorithm: contains the algorithm that can play the game;
-interface: this is the main file of the game. It calls all the useful functions and defines the interface for the user to play in;
-benchmarks: this file does not affect the game itself. It's purpose is to test how good the algorithm is.

There's also a CSV file called "minesweeper_data" that contains the data generated from the "benchmarks.py" file.

### Algorithm

The algorithm uses 3 strategies to play the game:

#### Strategy 1: Default
This is the main strategy of the algorithm, which every player uses a lot during the game. It is divided in three parts:
1. If a known tile with a number is touching <number of tile - number of marked bombs> unknown tiles, the unknown tiles must be bombs.
2. If a known tile with a number is touching <number of tile> marked bombs, then the rest of unknown tiles must be bombs.
3. If all bombs are marked in the board, free all the other unknown tiles.

#### Strategy 2: Simulations

According to my tests, this is the results of the algorithm (after 10,000 games for each mode):

EASY (9x9, 10 bombs)
% of Wins: 88.35
Average Time of Wins: 0.0008571343564960197 seconds
Average Time of Loses: 0.001110771080966671 seconds

NORMAL (16x16, 40 bombs):
% of Wins: 90.78
Average Time of Wins: 0.024174977304862445
Average Time of Loses: 0.016808433543058384

HARD (30x16, 99 bombs):
% of Wins: 6.54
Average Time of Wins: 0.02935 seconds
Average Time of Loses: 0.0154 seconds


All files contains multiple comments explaining what each function's purpose is, as well as its returning values.
