'''
This is the main file of the game, which calls other modules and creates the game's interface
'''

from Algorithm import Algorithm
from Board import Board
from Element import Element, Button
import pygame
import time
import webbrowser
import random
import os

# colors used in this project
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "ORANGE": (255, 204, 41)
}

# screen size
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

# limits of board
BOARD_START = (25, 100)
BOARD_END = (875, 585)

# elements info
TITLE = {
    "X": 350,
    "Y": 5,
    "SIZE_X": 400,
    "SIZE_Y": 91.91,
}

INITIAL_BUTTONS = {
    "X": 210,
    "Y": 100, 
    "SIZE_X": 220,
    "SIZE_Y": 75.69,
    "MARGIN_X": 10, 
    "MARGIN_Y": 20
}

INITIAL_TEXT = {
    "MODE_SELECTED_Y": 300,
    "MODE_Y": 325
}

GAME_BUTTONS = {
    "SIZE_X": 205,
    "SIZE_Y": 65,
    "MARGIN_Y": 10,
    "START_X": BOARD_END[0] + 10,
    "START_Y": BOARD_START[1],
}

# margin related to boards corners
GAME_DISPLAYS = {
    "MARGIN_X": 85,
    "MARGIN_Y": 10,
    "SIZE_X": 127,
    "SIZE_Y": 60
}

# margin related to starting x,y of displays
DISPLAYS_TEXT = {
    "X":65,
    "Y": 15
}

ALG_SPEED_TEXT = {
    "X":GAME_BUTTONS["START_X"] + 30,
    "Y": GAME_BUTTONS["START_Y"] + 3 * (GAME_BUTTONS["SIZE_Y"] + GAME_BUTTONS["MARGIN_Y"]) + 40
}

# title whe game ends ("you won" or "game over")
END_TITLE = {
    "Y": 20
}

# characteristics of each difficulty, format: (n_rows, n_columns, n_bombs) and color
DIFFICULTY = {
    "EASY": (9, 9, 10),
    "NORMAL": (16, 16, 40),
    "HARD": (16, 30, 99)
}

DIFFICULTY_COLORS = {
    "EASY": COLORS["GREEN"],
    "NORMAL": COLORS["ORANGE"],
    "HARD": COLORS["RED"]
}


# initialize pygame and create screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# title and icon
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("images/bomb.png")
pygame.display.set_icon(icon)

# Add images

marked_bombs_img = pygame.image.load("images/marked_bombs.png")
time_display_img = pygame.image.load("images/time_display.png")
algorithm_speed_controller_img = pygame.image.load("images/algspeed_controller.png")

# initial screen images
initial_title_img = pygame.image.load("images/initial_title.png")
easy_img = pygame.image.load("images/easy.png")
normal_img = pygame.image.load("images/normal.png")
hard_img = pygame.image.load("images/hard.png")
begin_img = pygame.image.load("images/begin.png")


'''
resize_tiles: resizes all tile's images to the desired tile size
@parameters:
    tile_images: dict whose keys are tile's possible symbols and values are the loaded images
    tile_size: size of each tile (both x and y sizes)
@return: None
'''
def resize_tiles(tile_images, tile_size):
    for symbol, image in tile_images.items():
        tile_images[symbol] = pygame.transform.scale(image, (tile_size, tile_size))
    return None

'''
load_tiles: loads tile's images
@parameters: none
@return: dict whose keys are tile's possible symbols and values are the loaded images
obs: also used to reset shape of tiles
'''
def load_tiles():
    return {
    "X": pygame.image.load("images/unknown_tile.png"),
    "!": pygame.image.load("images/marked_tile.png"),
    "?": pygame.image.load("images/question_tile.png"),
    "0": pygame.image.load("images/free_tile.png"),
    "1": pygame.image.load("images/one_tile.png"),
    "2": pygame.image.load("images/two_tile.png"),
    "3": pygame.image.load("images/three_tile.png"),
    "4": pygame.image.load("images/four_tile.png"),
    "5": pygame.image.load("images/five_tile.png"),
    "6": pygame.image.load("images/six_tile.png"),
    "7": pygame.image.load("images/seven_tile.png"),
    "8": pygame.image.load("images/eight_tile.png"),
    "B": pygame.image.load("images/bomb_tile.png")
}



'''
load_buttons: loads elements and buttons for both screens
@parameters: none
@return: dict whose keys are "initial" and "game" (name of screens) and values are the elements and buttons objects to be drawn
'''
def load_buttons():
    # initial screen buttons
    initial_buttons = {
        "title": Element("images/initial_title.png", TITLE["X"], TITLE["Y"], TITLE["SIZE_X"], TITLE["SIZE_Y"]),
        "easy": Button("images/easy.png", INITIAL_BUTTONS["X"], INITIAL_BUTTONS["Y"], INITIAL_BUTTONS["SIZE_X"], INITIAL_BUTTONS["SIZE_Y"]),
        "normal": Button("images/normal.png", (SCREEN_WIDTH - INITIAL_BUTTONS["SIZE_X"]) / 2, INITIAL_BUTTONS["Y"], INITIAL_BUTTONS["SIZE_X"], INITIAL_BUTTONS["SIZE_Y"]),
        "hard": Button("images/hard.png", SCREEN_WIDTH - INITIAL_BUTTONS["X"] - INITIAL_BUTTONS["SIZE_X"], INITIAL_BUTTONS["Y"], INITIAL_BUTTONS["SIZE_X"], INITIAL_BUTTONS["SIZE_Y"]),
        "begin": Button("images/begin.png", (SCREEN_WIDTH - INITIAL_BUTTONS["SIZE_X"]) / 2, INITIAL_BUTTONS["Y"] + INITIAL_BUTTONS["MARGIN_Y"] + INITIAL_BUTTONS["SIZE_Y"], INITIAL_BUTTONS["SIZE_X"], INITIAL_BUTTONS["SIZE_Y"]),
        "how_to_play": Button("images/button_htp.png", (SCREEN_WIDTH - INITIAL_BUTTONS["SIZE_X"]) / 2, SCREEN_HEIGHT - INITIAL_BUTTONS["MARGIN_Y"] - INITIAL_BUTTONS["SIZE_Y"], INITIAL_BUTTONS["SIZE_X"], INITIAL_BUTTONS["SIZE_Y"])
    }

    # game screen buttons
    game_buttons = {
        "new_game": Button("images/new_game.png", GAME_BUTTONS["START_X"], GAME_BUTTONS["START_Y"], GAME_BUTTONS["SIZE_X"], GAME_BUTTONS["SIZE_Y"]),
        "algorithm": Button("images/button_algorithm.png", GAME_BUTTONS["START_X"], GAME_BUTTONS["START_Y"] + GAME_BUTTONS["SIZE_Y"] + GAME_BUTTONS["MARGIN_Y"], GAME_BUTTONS["SIZE_X"], GAME_BUTTONS["SIZE_Y"]),
        "how_to_play": Button("images/button_htp.png", GAME_BUTTONS["START_X"], GAME_BUTTONS["START_Y"] + 2 * (GAME_BUTTONS["SIZE_Y"] + GAME_BUTTONS["MARGIN_Y"]), GAME_BUTTONS["SIZE_X"], GAME_BUTTONS["SIZE_Y"]),
        "algorithm_speed": Button("images/algspeed_controller.png", GAME_BUTTONS["START_X"], GAME_BUTTONS["START_Y"] + 3 * (GAME_BUTTONS["SIZE_Y"] + GAME_BUTTONS["MARGIN_Y"]), GAME_BUTTONS["SIZE_X"], GAME_BUTTONS["SIZE_Y"] / 2),
        "marked_bombs": Element("images/marked_bombs.png", BOARD_START[0] + GAME_DISPLAYS["MARGIN_X"], BOARD_END[1] + GAME_DISPLAYS["MARGIN_Y"], GAME_DISPLAYS["SIZE_X"], GAME_DISPLAYS["SIZE_Y"]),
        "time_spent": Element("images/time_display.png", BOARD_END[0] - (GAME_DISPLAYS["MARGIN_X"] + GAME_DISPLAYS["SIZE_X"]), BOARD_END[1] + GAME_DISPLAYS["MARGIN_Y"], GAME_DISPLAYS["SIZE_X"], GAME_DISPLAYS["SIZE_Y"])
    }

    
    return {"initial": initial_buttons, "game": game_buttons}


'''
draw_board: draws all tiles into the screen
@parameters:
    board: the Board object with all info from the game
    tile_images: dict whose keys are tile's possible symbols and values are the loaded images
    tile_size: the size of each individual tile
@return: None
'''
def draw_board(board, tile_images, tile_size):
    for i, row in enumerate(board.tiles_symbol):
        for j, tile in enumerate(row):
            screen.blit(tile_images[tile], (BOARD_START[0] + j * tile_size, BOARD_START[1] + i * tile_size))
    return None


'''
draw_buttons: draws all buttons
@parameters:
    place: the screen ("game_screen" or "initial_screen")
@return: None
'''
def draw_buttons(buttons):
    for _, button in buttons.items():
        button.draw(screen)
    return None


'''
initial_screen: creates the initial screen (when you enter the game and can select the difficulty)
@parameters:
    buttons: list with the elements/buttons objects to be drawn
@return: empty string if player quits game; otherwise, string containing the selected difficulty
'''
def initial_screen(buttons):
    # text style for selected mode
    font = pygame.font.Font("freesansbold.ttf", 20)

    # by default, mode is hard
    mode = "HARD"
    while True:
        screen.fill(COLORS["BLACK"])

        for event in pygame.event.get():
            # close the game
            if event.type == pygame.QUIT:
                return ""
            # left click on something
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                # easy mode
                if buttons["easy"].clicked(x, y):
                    mode = "EASY"
                # normal mode
                elif buttons["normal"].clicked(x, y):
                    mode = "NORMAL"
                # hard mode
                elif buttons["hard"].clicked(x, y):
                    mode = "HARD"
                # checks if begin button was clicked
                elif buttons["begin"].clicked(x, y):
                    return mode
                # checks if how to play button was clicked
                elif buttons["how_to_play"].clicked(x, y):
                    webbrowser.open("https://freeminesweeper.org/how-to-play-minesweeper.php", new=0, autoraise=True)
                else:
                    pass

        # draw elements
        text1 = font.render("MODE SELECTED", True, COLORS["WHITE"])
        screen.blit(text1, ((SCREEN_WIDTH - text1.get_width()) // 2, INITIAL_TEXT["MODE_SELECTED_Y"]))

        text2 = font.render(mode, True, DIFFICULTY_COLORS[mode])
        screen.blit(text2, ((SCREEN_WIDTH - text2.get_width()) // 2, INITIAL_TEXT["MODE_Y"]))

        draw_buttons(buttons)

        pygame.display.update()

    # should never be reacher
    return None


# function for game screen
# if there's a previous game, uses previous board. Else, creates a new board
# if players exits, returns -1. If players wants to play a new game, returns 1
'''
game_screen: creates the screen for the game (when you're playing a game of minesweeper)
@parameters:
    board: the board object of the game
    game_started: True if there was an existing game; False if it's a new game
    buttons: list with the buttons/elements objects to be drawn
@return: True if player clicks on "new game", False if player quits
'''
def game_screen(board, game_started, buttons):
    # text style for marked_bombs and time spent
    normal_font = pygame.font.Font("freesansbold.ttf", 35)
    # text style for won/lost screen
    end_font = pygame.font.Font("freesansbold.ttf", 65)
    # text style for algorithm speed
    small_font = pygame.font.Font("freesansbold.ttf", 15)

    # select tile size based on available space
    tile_images = load_tiles()
    tile_size = min((BOARD_END[0] - BOARD_START[0]) // board.n_columns,
                    (BOARD_END[1] - BOARD_START[1]) // board.n_rows)
    resize_tiles(tile_images, tile_size)

    algorithm_active = False  # turns True when players want the algorithm to play
    game_status = 0  # -1 for lost, 1 for won and 0 if not ended
    algorithm_speed = 0.0  # by default, the algorithm will run by its normal speed

    # create the algorithm player
    algorithm_player = Algorithm(board.tiles_symbol, board.n_rows, board.n_columns)

    # runs game until players clicks the X button
    while True:
        start_time = time.time()
        screen.fill((0, 0, 0))

        # if the algorithm is activated, let it play the game
        if algorithm_active and game_status == 0:
            algorithm_start = time.time()
            x, y, action = algorithm_player.play()
            algorithm_end = time.time()
            algorithm_time = algorithm_end - algorithm_start
            algorithm_sleep = max(algorithm_speed - algorithm_time, 0)
            time.sleep(algorithm_sleep)
            if not board.click(x, y, action):
                game_status = -1
                algorithm_active = False

        for event in pygame.event.get():
            # stops game. Saves the board if game is not finished and is started, else deletes files from previous game
            if event.type == pygame.QUIT:
                if game_status == 0 and game_started:
                    board.save_game("previous_game/status", "previous_game/symbols", "previous_game/time")
                else:
                    for file in os.listdir("previous_game"):
                        os.remove("previous_game/" + file)
                return False
            
            # click on screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # checks if coordinates are inside board
                if (BOARD_START[0] <= x <= BOARD_START[0] + tile_size * board.n_columns) and \
                        (BOARD_START[1] <= y <= BOARD_START[1] + tile_size * board.n_rows):
                    # get index of tile based on board coordinates
                    a, b = (y - BOARD_START[1]) // tile_size, (x - BOARD_START[0]) // tile_size

                    # left click
                    if event.button == 1 and game_status == 0:
                        # if game has not started, it's the first click
                        if not game_started:
                            board.place_bombs(a, b)
                            game_started = True
                        else:
                            if not board.click(a, b, "left"):
                                game_status = -1
                    # right click
                    elif event.button == 3 and game_status == 0:
                        board.click(a, b, "right")

                # new game button
                if buttons["new_game"].clicked(x, y):
                    # deletes previous game (if any)
                    for file in os.listdir("previous_game"):
                        os.remove("previous_game/" + file)
                    return True
                # algorithm button
                elif buttons["algorithm"].clicked(x, y):
                    algorithm_active = not(algorithm_active) # turns on and off
                    # if game hasn't started, begins the game by clicking close to the middle
                    if not game_started:
                        board.place_bombs(*algorithm_player.first_play())
                        game_started = True
                        start = time.time()
                # how to play button
                elif buttons["how_to_play"].clicked(x, y):
                    webbrowser.open("https://freeminesweeper.org/how-to-play-minesweeper.php", new=0,
                                    autoraise=True)
                # algorithm_speed (works differently than other buttons)
                elif buttons["algorithm_speed"].clicked(x, y):
                    dx, _ = buttons["algorithm_speed"].place_click(x, y)
                    # minus clicked
                    if 0 <= dx <= 0.33:
                        algorithm_speed = max(0.0, algorithm_speed - 0.1)
                    # plus clicked
                    elif 0.66 <= dx <= 1:
                        algorithm_speed = min(2.0, algorithm_speed + 0.1)
                # no button clicked
                else:
                    pass

        # verify if game is won
        if board.game_won():
            game_status = 1
            algorithm_active = False


        # draw elements
        draw_buttons(buttons)

        # drawing text (marked bombs, time spent and algorithm speed)
        text1 = normal_font.render(str(board.n_marked_bombs), True, COLORS["BLACK"])
        screen.blit(text1, (BOARD_START[0] + GAME_DISPLAYS["MARGIN_X"] + DISPLAYS_TEXT["X"], BOARD_END[1] + GAME_DISPLAYS["MARGIN_Y"] + DISPLAYS_TEXT["Y"]))

        text2 = normal_font.render(str(int(board.time_spent)), True, COLORS["BLACK"])
        screen.blit(text2, (BOARD_END[0] - GAME_DISPLAYS["MARGIN_X"] - GAME_DISPLAYS["SIZE_X"] + DISPLAYS_TEXT["X"], BOARD_END[1] + GAME_DISPLAYS["MARGIN_Y"] + DISPLAYS_TEXT["Y"]))

        text3 = small_font.render("algorithm speed: " + str(round(algorithm_speed, 1)), True, COLORS["WHITE"])
        screen.blit(text3, (ALG_SPEED_TEXT["X"], ALG_SPEED_TEXT["Y"]))

        draw_board(board, tile_images, tile_size)
        if game_status == 0:
            pass
        else:
            if game_status == 1:
                end_text = end_font.render("YOU WIN", True, COLORS["GREEN"])
            else:
                end_text = end_font.render("GAME OVER", True, COLORS["RED"])
            screen.blit(end_text, ((SCREEN_WIDTH - end_text.get_width()) // 2, END_TITLE["Y"]))
        pygame.display.update()

        # calculates time spent
        end_time = time.time()
        if game_started and game_status == 0:
            board.time_spent += (end_time - start_time)


# main function
def main():
    # loads previous game (if any)
    files = ["status", "symbols",   "time"]
    previous_game_dir = os.listdir("previous_game")
    if all(file in previous_game_dir for file in files):
        board = Board(previous_game=True)
    else:
        board = None

    buttons = load_buttons()

    # goes to initial screen if there's no previous game. Else, goes directly to the game
    if not board:
        mode = initial_screen(buttons["initial"])
        # exits game
        if not(mode):
            return None
        board = Board(*DIFFICULTY[mode])
        value = game_screen(board, False, buttons["game"])
    else:
        value = game_screen(board, True, buttons["game"])
    # runs the game while player doesn't exit (exit -> value is False)
    while value:
        mode = initial_screen(buttons["initial"])
        if not(mode):
            break
        board = Board(*DIFFICULTY[mode])
        value = game_screen(board, False, buttons["game"])
    return None


# runs code
main()
