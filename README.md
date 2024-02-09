# MINESWEEPER ALGORITHM
### Video Demo:  https://youtu.be/3HaNfj8fxaQ (obs: the project had some changes compared to when I created it to the CS50 course)
### Description:
This is a minesweeper game. Other than the usual content of a minesweeper, it also contains an algorithm that solves the game.

In the images folder, you will find all images used in this project. Most of them where either created by me or collected via screenshots of the original minesweeper game, but some icons where collected on the internet. Here are the references:
- Bomb image: https://www.flaticon.com/free-icons/bomb"
- Flag image: https://www.flaticon.com/free-icons/destination"


### Terminology
Before explaining the python codes, here's a short explanation of the terms used:
- Adjacent: a tile is adjacent to another if it "touches" it (diagonal included);
- Free: free a tile means to left click on it. If you free a tile that has a bomb, you lose the game. Otherwise, you will see the content of that tile, which can be a number or nothing, depending on how many bombs are adjacent to it;
- Mark: mark a tile means to right click on it. If it's just an unknown tile, it marks with a flag (or "!" inside the code). If it has a flag, it's marked with a question mark (?), and if it has a question mark, it goes back to an unknown tile;
- Status: the status of a tile is the content it has. It can be 0 if it has no bombs adjacent, 1 to 8 depending on how many bombs are adjacent, and -1 if itself has a bomb. The player does not have access to a tile's status until the tile is freed;
- Symbol: the symbol of a tile is what the player sees on the interface. If it's an unknown tile, it can be "X", "!" or "?", depending on the mark. If it's known, it can be a number between 0 and 8, depending on how many bombs are adjacent (the symbol 0 appears as just a empty tile on the interface).

If you want to know more about the rules of minesweeper, check out https://freeminesweeper.org/how-to-play-minesweeper.php (this is also the link of the "how to play" button inside the codes's interface).

There are 5 Python codes (.py) and 1 Jupyter Notebook file (.ipynb) in this project:
- Board.py: defines the board object (where the game is played);
- Element.py: defines the element and button objects (anything that is drawn in the interface);
- Algorithm.py: defines the algorithm that can play the game
- interface.py: this is the main file of the game. It calls all the useful functions and defines the interface for the user to play in;
- test_solver.py: this file does not affect the game itself. It's purpose is to test how good the algorithm is;
- Algorithm Analysis.ipynb: an analysis of the algorithm's performance.

There's also a CSV file called "minesweeper_data.csv" that contains the data generated from the "test_solver.py" file.

### Algorithm

The algorithm uses 3 strategies to play the game:

#### Strategy 1: Simple
This is the main strategy of the algorithm, which most players already know. It is divided in two parts:
1. If a known tile with a number is touching <number of tile - number of marked bombs> unknown tiles, then the adjacent unknown tiles must be bombs.
2. If a known tile with a number is touching <number of tile> marked bombs, then the adjacent unknown tiles must be bombs.

#### Strategy 2: Complex
This is a more complex strategy, that used the concept of Constraint Satisfaction Problem (check https://dash.harvard.edu/bitstream/handle/1/14398552/BECERRA-SENIORTHESIS-2015.pdf for more info). The general idea is:
1. An unknown tile can have a value of 0 or 1 (0 means no bomb, 1 means there's a bomb on it);
2. Create equations using freed tiles, where the variables are the values of the unknown tiles it touches, and the result is how many unknown bombs it touches;
3. For each unkown tile, get the equations that envolve it and create a system of equations;
4. Get all possible solutions of the system of equations above;
5. If a variable has the same value in all possible solutions, then we can conclude if there is a bomb or not in that tile.
  
#### Strategy 3: Random Guesses
If the algorithm loops through the entire board and doesn't use any of the two previous strategies, it frees a random unknown tile from the board.

The algorithm saves the possible plays in a queue, so it doesn't have to loop through the entire board everytime it is called, making it a lot faster.

The first click of the algorithm is in a random tile (I tested some other strategies, like click on the middle or on an edge, and all seem to have about the same results, but random tile was the best, so it's the default strategy). You can change it in the "first_play" method of the Algorithm class.

#### Performance of the Algorithm
  
According to my tests, this is the results of the algorithm (analysing 10,000 games for each mode):

EASY (9x9, 10 bombs)
% of Wins: 94.48
Average Time: 0.00316 seconds

NORMAL (16x16, 40 bombs):
% of Wins: 65.78
Average Time of Wins: 0.005658274473988854 seconds
Average Time of Loses: 0.004797840313490617 seconds

HARD (30x16, 99 bombs):
% of Wins: 30.35
Average Time: 0.05756 seconds

All files contains multiple comments explaining what each function's purpose is, as well as its returning values.
