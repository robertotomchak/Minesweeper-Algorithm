# This is the main file of the game. It calls the functions necessary to play the game, as well as create the interfaces
import algorithm
import functions
import pygame
import time
import webbrowser


# initialize pygame and create screen
pygame.init()
screen = pygame.display.set_mode((1100, 700))

# limits of board
start_coords = (25, 100)
end_coords = (875, 585)

# important constants for game screen
game_values = {
    "button_sizeX": 205,
    "button_sizeY": 64.69,
    "marginY": 10,
    "startX": end_coords[0] + 10,
    "startY": start_coords[1],
    "margin_displaysX": 85,
    "margin_displaysY": 10,
    "display_sizeX": 126.56,
    "display_sizeY": 60
}

# important constants for welcome_screen
initial_values = {
    "title_marginX": 350,
    "title_marginY": 5,
    "title_sizeX": 400,
    "title_sizeY": 91.91,
    "button_initialX": 210,
    "button_sizeX": 220,
    "button_sizeY": 75.69,
    "button_marginX": 10,
    "button_marginY": 10
}


# title and icon
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("images/bomb.png")
pygame.display.set_icon(icon)

# Add images

# tile images
unknown_tile_img = pygame.image.load("images/unknown_tile.png")
free_tile_img = pygame.image.load("images/free_tile.png")
marked_tile_img = pygame.image.load("images/marked_tile.png")
question_tile_img = pygame.image.load("images/question_tile.png")
one_tile_img = pygame.image.load("images/one_tile.png")
two_tile_img = pygame.image.load("images/two_tile.png")
three_tile_img = pygame.image.load("images/three_tile.png")
four_tile_img = pygame.image.load("images/four_tile.png")
five_tile_img = pygame.image.load("images/five_tile.png")
six_tile_img = pygame.image.load("images/six_tile.png")
seven_tile_img = pygame.image.load("images/seven_tile.png")
eight_tile_img = pygame.image.load("images/eight_tile.png")
bomb_tile_img = pygame.image.load("images/bomb_tile.png")

# game screen images
button_algorithm_img = pygame.image.load("images/button_algorithm.png")
button_new_game_img = pygame.image.load("images/new_game.png")
button_settings_img = pygame.image.load("images/button_settings.png")
button_htp_img = pygame.image.load("images/button_htp.png")
marked_bombs_img = pygame.image.load("images/marked_bombs.png")
time_display_img = pygame.image.load("images/time_display.png")
algorithm_speed_controller_img = pygame.image.load("images/algspeed_controller.png")

# initial screen images
initial_title_img = pygame.image.load("images/initial_title.png")
easy_img = pygame.image.load("images/easy.png")
normal_img = pygame.image.load("images/normal.png")
hard_img = pygame.image.load("images/hard.png")
begin_img = pygame.image.load("images/begin.png")


# draws given board, with given tile_size
# returns nothing
def display_tiles(board, tile_size):
    # images based on symbol
    images = {
        "X": pygame.transform.scale(unknown_tile_img, (tile_size, tile_size)),
        "0": pygame.transform.scale(free_tile_img, (tile_size, tile_size)),
        "!": pygame.transform.scale(marked_tile_img, (tile_size, tile_size)),
        "?": pygame.transform.scale(question_tile_img, (tile_size, tile_size)),
        "1": pygame.transform.scale(one_tile_img, (tile_size, tile_size)),
        "2": pygame.transform.scale(two_tile_img, (tile_size, tile_size)),
        "3": pygame.transform.scale(three_tile_img, (tile_size, tile_size)),
        "4": pygame.transform.scale(four_tile_img, (tile_size, tile_size)),
        "5": pygame.transform.scale(five_tile_img, (tile_size, tile_size)),
        "6": pygame.transform.scale(six_tile_img, (tile_size, tile_size)),
        "7": pygame.transform.scale(seven_tile_img, (tile_size, tile_size)),
        "8": pygame.transform.scale(eight_tile_img, (tile_size, tile_size)),
        "B": pygame.transform.scale(bomb_tile_img, (tile_size, tile_size))

    }
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            screen.blit(images[tile.symbol], (start_coords[0] + j * tile_size, start_coords[1] + i * tile_size))
    return None


# based on the present screen (place), draws the necessary buttons
# returns nothing
def display_buttons(place):
    # buttons for game screen
    if place == "game_screen":
        button_new_game_img_rescaled = pygame.transform.scale(
            button_new_game_img, (game_values["button_sizeX"], game_values["button_sizeY"]))
        screen.blit(button_new_game_img_rescaled, (game_values["startX"], game_values["startY"]))

        button_algorithm_rescaled = pygame.transform.scale(button_algorithm_img, (
            game_values["button_sizeX"], game_values["button_sizeY"]))
        screen.blit(button_algorithm_rescaled, (game_values["startX"], game_values["startY"] +
                                                game_values["marginY"] + game_values["button_sizeY"]))

        button_htp_img_rescaled = pygame.transform.scale(button_htp_img, (
            game_values["button_sizeX"], game_values["button_sizeY"]))
        screen.blit(button_htp_img_rescaled, (game_values["startX"], game_values["startY"] +
                                              2 * game_values["marginY"] + 2 * game_values["button_sizeY"]))

        marked_bombs_rescaled = pygame.transform.scale(marked_bombs_img, (
            game_values["display_sizeX"], game_values["display_sizeY"]))
        screen.blit(marked_bombs_rescaled, (start_coords[0] + game_values["margin_displaysX"],
                                            end_coords[1] + game_values["margin_displaysY"]))

        time_display_rescaled = pygame.transform.scale(time_display_img, (
            game_values["display_sizeX"], game_values["display_sizeY"]))
        screen.blit(time_display_rescaled,
                    (end_coords[0] - game_values["margin_displaysX"] - game_values["display_sizeX"],
                     end_coords[1] + game_values["margin_displaysY"]))

        algorithm_speed_controller_rescaled = pygame.transform.scale(
            algorithm_speed_controller_img, (game_values["button_sizeX"], game_values["button_sizeY"] / 2))
        screen.blit(algorithm_speed_controller_rescaled,
                    (game_values["startX"], game_values["startY"] + 5 * game_values["marginY"] +
                     3 * game_values["button_sizeY"]))

    # elements for initial screen
    elif place == "initial_screen":
        initial_tile_rescaled = pygame.transform.scale(initial_title_img,
                                                       (initial_values["title_sizeX"], initial_values["title_sizeY"]))
        screen.blit(initial_tile_rescaled, (initial_values["title_marginX"], initial_values["title_marginY"]))

        easy_rescaled = pygame.transform.scale(easy_img,
                                               (initial_values["button_sizeX"], initial_values["button_sizeY"]))
        screen.blit(easy_rescaled, (initial_values["button_initialX"], initial_values["title_marginY"] +
                                    initial_values["title_sizeY"] + initial_values["button_marginY"]))

        normal_rescaled = pygame.transform.scale(normal_img,
                                                 (initial_values["button_sizeX"], initial_values["button_sizeY"]))
        screen.blit(normal_rescaled, (initial_values["button_initialX"] + initial_values["button_marginX"]
                                      + initial_values["button_sizeX"], initial_values["title_marginY"] +
                                      initial_values["title_sizeY"] + initial_values["button_marginY"]))

        hard_rescaled = pygame.transform.scale(hard_img,
                                               (initial_values["button_sizeX"], initial_values["button_sizeY"]))
        screen.blit(hard_rescaled, (initial_values["button_initialX"] + 2 * initial_values["button_marginX"] +
                                    2 * initial_values["button_sizeX"], initial_values["title_marginY"] +
                                    initial_values["title_sizeY"] + initial_values["button_marginY"]))

        begin_rescaled = pygame.transform.scale(begin_img,
                                                (initial_values["button_sizeX"], initial_values["button_sizeY"]))
        screen.blit(begin_rescaled, (initial_values["button_initialX"] + initial_values["button_marginX"] +
                                     initial_values["button_sizeX"], initial_values["title_marginY"] +
                                     initial_values["title_sizeY"] + 3 * initial_values["button_marginY"] +
                                     initial_values["button_sizeY"]))

        button_htp_img_rescaled = pygame.transform.scale(button_htp_img, (
            game_values["button_sizeX"], game_values["button_sizeY"]))
        screen.blit(button_htp_img_rescaled, (initial_values["button_marginX"], 700 - initial_values["button_marginY"]
                                              - game_values["button_sizeY"]))


# function for initial screen
# returns -1 if player closes the game. Else, returns the chosen game
def initial_screen():
    # text style for selected mode
    font = pygame.font.Font("freesansbold.ttf", 20)

    # by default, mode is hard
    mode = (16, 30, 99)
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            # close the game
            if event.type == pygame.QUIT:
                return -1
            # left click on something
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                # check for selected mode, if clicked
                if initial_values["title_marginY"] + initial_values["title_sizeY"] + initial_values["button_marginY"]\
                        <= y <= initial_values["title_marginY"] + initial_values["title_sizeY"] +\
                        initial_values["button_marginY"] + initial_values["button_sizeY"]:
                    # easy mode
                    if initial_values["button_initialX"] <= x <= initial_values["button_initialX"] +\
                            initial_values["button_sizeX"]:
                        mode = (9, 9, 10)
                    # normal mode
                    elif initial_values["button_initialX"] + initial_values["button_marginX"] +\
                            initial_values["button_sizeX"] <= x <= initial_values["button_initialX"] +\
                            initial_values["button_marginX"] + 2 * initial_values["button_sizeX"]:
                        mode = (16, 16, 40)
                    # hard mode
                    elif initial_values["button_initialX"] + 2 * initial_values["button_marginX"] +\
                            2 * initial_values["button_sizeX"] <= x <= initial_values["button_initialX"] +\
                            2 * initial_values["button_marginX"] + 3 * initial_values["button_sizeX"]:
                        mode = (16, 30, 99)
                    # did not click on mode selector
                    else:
                        pass
                # checks if begin button was clicked
                elif initial_values["title_marginY"] + initial_values["title_sizeY"] + \
                        4 * initial_values["button_marginY"] + initial_values["button_sizeY"] <= y <=\
                        initial_values["title_marginY"] + initial_values["title_sizeY"] +\
                        4 * initial_values["button_marginY"] + 2 * initial_values["button_sizeY"] and\
                        initial_values["button_initialX"] + initial_values["button_marginX"] +\
                        initial_values["button_sizeX"] <= x <= initial_values["button_initialX"] +\
                        initial_values["button_marginX"] + 2 * initial_values["button_sizeX"]:
                    return mode
                # checks if how to play button was clicked
                elif 700 - game_values["button_sizeY"] - initial_values["button_marginY"] <= y <= 700 -\
                        initial_values["button_marginY"] and initial_values["button_marginX"] <= x <=\
                        initial_values["button_marginX"] + game_values["button_sizeX"]:
                    webbrowser.open("https://freeminesweeper.org/how-to-play-minesweeper.php", new=0, autoraise=True)
                else:
                    pass

        # draw elements
        screen.blit(font.render("MODE SELECTED", True, (255, 255, 255)), (463, 300))
        if mode == (16, 30, 99):
            screen.blit(font.render("HARD", True, (255, 0, 0)), (523, 325))
        elif mode == (16, 16, 40):
            screen.blit(font.render("NORMAL", True, (255, 204, 41)), (504, 325))
        elif mode == (9, 9, 10):
            screen.blit(font.render("EASY", True, (0, 255, 0)), (520, 325))
        else:
            pass
        display_buttons("initial_screen")
        pygame.display.update()


# function for game screen
# if there's a previous game, uses previous board. Else, creates a new board
# if players exits, returns -1. If players wants to play a new game, returns 1
def game_screen(n_rows=0, n_columns=0, n_bombs=0, board=[], start_time=0):
    if not board:
        board = functions.empty_board(n_rows, n_columns, n_bombs)
        started = False
    else:
        started = True
        start = time.time() - start_time

    # text style for marked_bombs and time spent
    normal_font = pygame.font.Font("freesansbold.ttf", 35)
    # text style for won/lost screen
    end_font = pygame.font.Font("freesansbold.ttf", 65)
    # text style for algorithm speed
    smaller_font = pygame.font.Font("freesansbold.ttf", 15)

    # select tile size based on available space
    tile_size = min((end_coords[0] - start_coords[0]) // functions.Tile.N_COLUMNS,
                    (end_coords[1] - start_coords[1]) // functions.Tile.N_ROWS)

    algorithm_active = False  # turns True when players want the algorithm to play
    game_status = 0  # -1 for lost, 1 for won and 0 if not ended
    algorithm_speed = 0  # by default, the algorithm will run by its normal speed
    time_spent = start_time  # default time

    # runs game until players clicks the X button
    while True:
        screen.fill((0, 0, 0))
        # if the algorithm is activated, let it play the game
        if algorithm_active and game_status == 0:
            algorithm_start = time.time()
            x, y, action, _ = algorithm.algorithm(board)
            algorithm_end = time.time()
            algorithm_sleep = algorithm_speed - (algorithm_end - algorithm_start) if\
                algorithm_speed > (algorithm_end - algorithm_start) else 0
            time.sleep(algorithm_sleep)
            if board[x][y].action(action, board) == -1:
                game_status = -1
                algorithm_active = False

        for event in pygame.event.get():
            # stop game. Saves the board if game is not finished and is started
            if event.type == pygame.QUIT:
                if game_status == 0 and started:
                    functions.save_game(board, time_spent)
                else:
                    functions.save_game([], 0)
                return -1
            # click on screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # checks if coordinates are inside board
                if (start_coords[0] <= x <= start_coords[0] + tile_size * functions.Tile.N_COLUMNS) and \
                        (start_coords[1] <= y <= start_coords[1] + tile_size * functions.Tile.N_ROWS):
                    # get index of tile based on board coordinates
                    a, b = (y - start_coords[1]) // tile_size, (x - start_coords[0]) // tile_size

                    # left click
                    if event.button == 1:
                        # if game has not started, it's the first click
                        if not started:
                            functions.start_game(board, a, b)
                            started = True
                            start = time.time() - start_time
                        else:
                            print(board[a][b].adjacent_unknowns, board[a][b].adjacent_bombs, board[a][b].symbol)
                            if board[a][b].action("F", board) == -1:
                                game_status = -1
                    # mark bomb
                    elif event.button == 3:
                        board[a][b].action("M", board)

                # checks if coordinates are inside button
                elif game_values["startX"] <= x <= game_values["startX"] + game_values["button_sizeX"] \
                        and y >= game_values["startY"]:
                    # new game button
                    if y <= game_values["startY"] + game_values["button_sizeY"]:
                        return 1
                    # algorithm button
                    elif y <= game_values["startY"] + 2 * game_values["button_sizeY"] + game_values["marginY"]:
                        algorithm_active = True if not algorithm_active else False  # turns on and off
                        # if game hasn't started, begins the game
                        if not started:
                            functions.start_game(board, auto=True)
                            started = True
                            start = time.time()
                    # how to play button
                    elif y <= game_values["startY"] + 3 * game_values["button_sizeY"] + 2 * game_values["marginY"]:
                        webbrowser.open("https://freeminesweeper.org/how-to-play-minesweeper.php", new=0,
                                        autoraise=True)
                    # decrease algorithm speed button
                    elif x <= game_values["startX"] + game_values["button_sizeY"] and game_values["startY"] +\
                            3 * game_values["button_sizeY"] + 5 * game_values["marginY"] <= y <= game_values["startY"]\
                            + (3 + 1/2) * game_values["button_sizeY"] + 5 * game_values["marginY"]:
                        algorithm_speed -= 0.1 if algorithm_speed > 0.1 else 0
                    # increase algorithm speed button
                    elif 1100 - 10 - game_values["button_sizeY"] <= x <= 1100 - 10 and game_values["startY"] +\
                            3 * game_values["button_sizeY"] + 5 * game_values["marginY"] <= y <= game_values["startY"]\
                            + (3 + 1/2) * game_values["button_sizeY"] + 5 * game_values["marginY"]:
                        algorithm_speed += 0.1 if algorithm_speed < 2 else 0
                    # no button clicked
                    else:
                        pass

        # verify if game is won
        if functions.Tile.freed_tiles == functions.Tile.win_condition:
            game_status = 1
            algorithm_active = False

        # calculates time spent
        end = time.time()
        if started and game_status == 0:
            time_spent = round(end - start)

        # draw elements
        display_buttons("game_screen")
        screen.blit(smaller_font.render(f"Algorithm Speed: {round(algorithm_speed,1)}s", True, (255, 255, 255)),
                    (game_values["startX"] + 28, game_values["startY"] +
                     3 * game_values["button_sizeY"] + 3 * game_values["marginY"]))
        screen.blit(normal_font.render(str(functions.Tile.marked_bombs), True, (0, 0, 0)),
                    (start_coords[0] + game_values["margin_displaysX"] + game_values["display_sizeX"] * 3 / 5,
                     end_coords[1] + game_values["margin_displaysY"] + game_values["display_sizeY"] / 4))
        screen.blit(normal_font.render(str(time_spent), True, (0, 0, 0)),
                    (end_coords[0] - game_values["margin_displaysX"] - game_values["display_sizeX"] * 1 / 2,
                     end_coords[1] + game_values["margin_displaysY"] + game_values["display_sizeY"] / 4))
        display_tiles(board, tile_size)
        if game_status == 1:
            screen.blit(end_font.render("YOU WIN", True, (0, 255, 0)), (405, 20))
        elif game_status == -1:
            screen.blit(end_font.render("GAME OVER", True, (255, 0, 0)), (350, 20))
        else:
            pass
        pygame.display.update()


# main function
def main():
    # loads previous game (if any)
    board, time_spent = functions.load_game()
    # goes to initial screen if there's no previous game. Else, goes directly to the game
    if not board:
        mode = initial_screen()
        # exits game
        if mode == -1:
            return None
        value = game_screen(*mode)
    else:
        value = game_screen(board=board, start_time=time_spent)
    # runs the game while players doesn't exit
    while True:
        # exit game
        if value == -1:
            return None
        # create new game
        if value == 1:
            mode = initial_screen()
            value = game_screen(*mode)


# runs code
main()
