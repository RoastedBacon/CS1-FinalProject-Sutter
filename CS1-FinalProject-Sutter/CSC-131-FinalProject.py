'''
Cell Canvas
CSC-131 Computer Science I
Final Project

Acknowledgements:
    https://beltoforion.de/en/recreational_mathematics/game_of_life.php

time spent: 600 minutes (present and participation) for Ben (Ben also worked on the presentation)
            800 minutes (present and participation) for Isaiah
            540 minutes present and 120 minutes approx participation for Cory
'''

import time
import math
import sys
import random as rnd
import numpy  as np
import pygame as pg
from   enum     import Enum, auto
from   datetime import datetime, timedelta




# ==============================================================================#=
# ANIMATION
# The code below is is where the client controls and manages
# what is displayed on the cell canvas.
# ==============================================================================#=
player_col = 0
player_row = 16
player_color = pg.Color('red')
player_trail = pg.Color(20, 20, 20)
final_col_color = pg.Color('white')
final_col = 41
final_row = 0
mine_row = 0
mine_col = 0
mine_color = 0
move_count = 0
level = 1
background_color = pg.Color(64, 64, 64)




# --------------------------------------------------------------+-
# Periodic Canvas Content Update
# --------------------------------------------------------------+-
def get_next_matrix():
    '''
    The main loop in the Cell Canvas calls this function periodically,
    each time it's ready for a new 2D-Array of cells to be displayed.
    This function returns a new or updated matrix of cells based on
    the design of the client animation/simulation/game.
    '''
    global cell_matrix
    global player_row
    global player_col
    global player_color
    global mine_row
    global mine_col
    global mine_color
    global player_trail
    global final_col_color
    global final_col
    global final_row
   

    # Add your code here to update the cell matrix.
    cell_matrix[player_row][player_col] = player_color
    cell_matrix[mine_row][mine_col] = mine_color
    cell_matrix[final_row][final_col] = final_col_color
   


    if final_row != 31:
        for count in range(1):
            final_row += 1

    return cell_matrix


# ==============================================================================#=
# Event Dispatcher
# ==============================================================================#=
def dispatch_next_event(given_pg_event):

    global player_row
    global player_col
    global player_color
    global mine_row
    global mine_col
    global mine_color
    global player_trail
    global cell_matrix
    global move_count
    global final_row
    global level
    global caption
    global background_color
    global final_col_color


    '''
    Returns true if the program should quit;
    false otherwise
    '''

    evt = given_pg_event

    if evt.type == pg.QUIT:
        return True   # time to exit the program
   
    elif evt.type == pg.KEYDOWN:
        # Which keys determine the movement of the player.
        if (evt.key == pg.K_d) and (player_col != 41):
            # The movement count and player position need to be updated with each key press    
            move_count +=1
            player_col += 1
            # The player trail is subtracted by one from the players position
            cell_matrix[player_row][player_col -1] = player_trail
            print(move_count)
        elif (evt.key == pg.K_w) and (player_row != 0):
            move_count +=1
            player_row -= 1
            cell_matrix[player_row +1][player_col] = player_trail
            print(move_count)
        elif (evt.key == pg.K_a) and (player_col != 0):
            move_count +=1
            player_col -= 1
            cell_matrix[player_row][player_col +1] = player_trail
            print(move_count)
        elif (evt.key == pg.K_s) and (player_row != 31):
            move_count +=1
            player_row += 1
            cell_matrix[player_row -1][player_col] = player_trail
            print(move_count)
        # This is the cheat code, if you take the "l" you will instantly win
        elif (evt.key == pg.K_l) and (player_row != 31):
            player_row = 16
            player_col = 41

    # When the player reaches the highlited area, the player position
    # and count along with the entire canvas need to reset
    if player_col == 41:
        print("You moved a total of", move_count, "spaces")
        final_row = -1
        # This if statement and for loop will reset the highlited area
        # It will also change the color of the highlited area for each level
        if final_row != 31 and level == 1:
            final_col_color = pg.Color('blue')
            for count in range(1):
                final_row += 1
        elif final_row != 31 and level == 2:
            final_col_color = pg.Color('teal')
            for count in range(1):
                final_row += 1
        elif final_row != 31 and level == 3:
            final_col_color = pg.Color('red')
            for count in range(1):
                final_row += 1
        elif final_row != 31 and level == 4:
            for count in range(1):
                final_row += 1
        player_row = 16
        player_col = 0
        move_count = 0
        mine_col = 0
        mine_row = 0
        mine_color = 0
        # This code will reset the canvas
        for row, col in np.ndindex(cell_matrix.shape):
            cell_matrix[row, col] = 0
        level += 1

   

    # ------------------------------------------------------------------------------+-
    # Mine Locations
    # ------------------------------------------------------------------------------+-
    list_of_mines = [(1,2), (2, 3), (3, 4), (4, 5), (5, 6),
                     (6, 7), (9, 4), (8, 5), (10, 6), (13, 7),
                     (14, 8), (29, 20), (28, 22), (27, 21),
                     (26, 23), (25, 29), (24, 28), (23, 30),
                     (20, 8), (21, 9), (31, 12), (17, 5), (22, 22),
                     (18, 25), (14, 27), (24, 31), (30, 10), (18, 8),
                     (16, 3), (16, 7), (16, 10), (16, 20), (16, 30), (15, 4),
                     (15, 10), (15, 17), (15, 7), (15, 27), (15, 30), (17, 5),
                     (17, 15), (17, 28), (18, 5), (18, 15), (18, 20), (18, 27),
                     (19, 8), (19, 18), (19, 27), (19, 11), (19, 24), (1, 5),
                     (1, 7), (1, 13), (1, 19), (1, 25), (1, 30)]

    list_of_mines_2 = [(1,2), (2, 3), (3, 4), (4, 5), (5, 6),
                     (6, 7), (9, 4), (8, 5), (10, 6), (13, 7),
                     (14, 8), (29, 20), (28, 22), (27, 21),
                     (26, 23), (25, 29), (24, 28), (23, 30),
                     (20, 8), (21, 9), (31, 12), (17, 5), (22, 22),
                     (18, 25), (14, 27), (24, 31), (30, 10), (18, 8),
                     (19, 32), (19, 15), (19, 18), (19, 6), (19, 26), (19, 21), (19, 10), (19, 25), (19, 14),
                     (0, 20), (0, 12), (0, 9), (0, 3), (0, 6), (0, 40), (0, 27), (0, 23), (0, 17), (0, 21), (0, 32),
                     (17, 36), (17, 11), (17, 18), (17, 30), (17, 7), (17, 13), (17, 25),
                     (4, 9), (4, 3), (4, 21), (4, 15), (4, 19), (4, 28), (4, 10), (4, 18),
                     (7, 23), (7, 15), (7, 18), (7, 6), (7, 26), (7, 21), (7, 10), (7, 25), (7, 14),
                     (12, 7), (12, 17), (12, 13), (12, 30), (12, 25), (12, 20), (12, 4), (12, 7), (12, 16),
                     (15, 20), (15, 14), (15, 9), (15, 24), (15, 26), (15, 3), (15, 5), (15, 22), (15, 8),
                     (20, 5), (20, 3), (20, 23), (20, 7), (20, 29), (20, 24), (20, 25), (20, 26), (20, 10),
                     (31, 9), (31, 11), (31, 6), (31, 4), (31, 28), (31, 17), (31, 2), (31, 22), (31, 16),
                     (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 16),
                     (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 30), (16, 31), (16, 32),
                     (16, 33), (16, 34), (16, 35), (16, 36), (16, 37), (16, 38), (16, 39), (16, 40)]

    list_of_mines_3 = [(1,2), (2, 3), (3, 4), (4, 5), (5, 6),
                     (6, 7), (9, 4), (8, 5), (10, 6), (13, 7),
                     (14, 8), (29, 20), (28, 22), (27, 21),
                     (26, 23), (25, 29), (24, 28), (23, 30),
                     (20, 8), (21, 9), (31, 12), (17, 5), (22, 22),
                     (18, 25), (14, 27), (24, 31), (30, 10), (18, 8),
                     (4, 9), (4, 3), (4, 21), (4, 15), (4, 19), (4, 28), (4, 10), (4, 18),
                     (7, 23), (7, 15), (7, 18), (7, 6), (7, 26), (7, 21), (7, 10), (7, 25), (7, 14),
                     (12, 7), (12, 17), (12, 13), (12, 30), (12, 25), (12, 20), (12, 4), (12, 7), (12, 16),
                     (15, 20), (15, 14), (15, 9), (15, 24), (15, 26), (15, 3), (15, 5), (15, 22), (15, 8),
                     (20, 5), (20, 3), (20, 23), (20, 7), (20, 29), (20, 24), (20, 25), (20, 26), (20, 10),
                     (31, 9), (31, 11), (31, 6), (31, 4), (31, 28), (31, 17), (31, 2), (31, 22), (31, 16),
                     (1,2), (2, 3), (3, 4), (4, 5), (5, 6),
                     (6, 7), (9, 4), (8, 5), (10, 6), (13, 7),
                     (14, 8), (29, 20), (28, 22), (27, 21),
                     (26, 23), (25, 29), (24, 28), (23, 30),
                     (20, 8), (21, 9), (31, 12), (17, 5), (22, 22),
                     (18, 25), (14, 27), (24, 31), (30, 10), (18, 8),
                     (16, 3), (16, 7), (16, 10), (16, 20), (16, 30), (15, 4),
                     (15, 10), (15, 17), (15, 7), (15, 27), (15, 30), (17, 5),
                     (17, 15), (17, 28), (18, 5), (18, 15), (18, 20), (18, 27),
                     (19, 8), (19, 18), (19, 27), (19, 11), (19, 24), (1, 5),
                     (19, 32), (19, 15), (19, 18), (19, 6), (19, 26), (19, 21), (19, 10), (19, 25), (19, 14),
                     (1, 7), (1, 13), (1, 19), (1, 25), (1, 30), (24, 4), (24, 10), (24, 15), (24, 22), (24, 30), (24, 38),
                     (11, 29), (11, 18), (11, 9), (11, 25), (11, 6), (11, 40), (11, 27), (11, 8), (11, 17), (11, 1), (11, 41),
                     (0, 20), (0, 12), (0, 9), (0, 3), (0, 6), (0, 40), (0, 27), (0, 23), (0, 17), (0, 21), (0, 32),
                     (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 30), (16, 31), (16, 32),
                     (16, 33), (16, 34), (16, 35), (16, 36), (16, 37), (16, 38), (16, 39), (16, 40),
                     (23, 14), (23, 3), (23, 6), (23, 18), (23, 20), (23, 37), (23, 25), (23, 31), (23, 41), (23, 35), (23, 39)]

    list_of_mines_4 = [(18, 0), (18, 1), (18, 2), (14, 0), (14, 1), (14, 2), (15, 3), (16, 3), (17, 3)]

    # The following code will change the positiion of the land mines for each level
    if level == 1:
        for mine in list_of_mines:
            if (player_row == mine[0]) and (player_col == mine[1]):
                mine_col = player_col
                mine_row = player_row
                # preents bug where some landmines appear out of nowhere
                mine_color = pg.Color('yellow')
                player_row = 16
                player_col = 0  
    elif level == 2:
        for mine in list_of_mines_2:
            if (player_row == mine[0]) and (player_col == mine[1]):
                mine_col = player_col
                mine_row = player_row
                mine_color = pg.Color('yellow')
                player_row = 16
                player_col = 0  
    elif level == 3:
        for mine in list_of_mines_3:
            if (player_row == mine[0]) and (player_col == mine[1]):
                mine_col = player_col
                mine_row = player_row
                mine_color = pg.Color('yellow')
                player_row = 16
                player_col = 0 
    elif level == 4:
        for mine in list_of_mines_4:
            if (player_row == mine[0]) and (player_col == mine[1]):
                mine_col = player_col
                mine_row = player_row
                mine_color = pg.Color('yellow')
                player_row = 16
                player_col = 0 

    # After the 4th level the game will just close
    else:
        return True
    # ------------------------------------------------------------------------------+-
    # End of Mine Locations
    # ------------------------------------------------------------------------------+-
   
    return False   # Don't quit the game.  


# ------------------------------------------------------------------------------+-
# Startup Init
# ------------------------------------------------------------------------------+-
def startup_initialization():
   
    '''
    Add to this function,
    anything that needs to be done once at program startup.
    '''
    rnd.seed()
    print("")
    print("Wlcome to Mine Evader!")
    print("")
    print("Get to the highlited area using W-A-S-D in the least amount of movements.")
    print("CAREFUL!! There are hiddens mines in the way! These mines will reset your position.")
    print("Your movements will be shown below.")
    return


# ======================================================================#=
# Build-Time Configuration
#
# The Cell-Canvas expects the following values to be defined.
# ======================================================================#=
# The number of cells in each row and column,
# And the width and height of a cell in pixels.
num_cols = 42
num_rows = 32
pixels_per_cell = 24

# The background color is used to fill the entire display surface before
# the cells are re-drawn upon it.  Each cell is drawn as a colored rectangle
# that is one pixel smaller (in both dimensions) than the actual cell size.
# This allows the background color to show in between each cell and appear
# as a grid that highlights each individual cell with a square frame.
background_color = pg.Color(64, 64, 64)

# Text to display at the top of the window.
caption = "MineEvader - Level 1 = White,    Level 2 = Blue,    Level 3 = Teal,    Level 4 = Red - lol"

# Number of seconds to delay per iteration of the main loop.
main_loop_delay = 0.1
# ======================================================================#=

'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|@
Avoid changing any code below this marker!
If you think you want to make a change,
discuss this with your instructor before doing so.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|@
'''

# ==============================================================================#=
# CELL MATRIX
#
# The Cell Matrix defines the color for each cell on the canvas.
#
# It is a 2D numpy array that represents all the cells on the canvas.
# Each element in the array represents a single cell.
# Any element in the array can be set to any color thus
# changing the color corresponding cell on the canvas.
# ==============================================================================#=
cell_matrix_shape = (num_rows, num_cols)
cell_matrix = np.zeros(cell_matrix_shape, dtype=pg.Color)

# ==============================================================================#=
# CELL CANVAS
#
# The Cell Canvas is an interactive 2D animation.
# ==============================================================================#=
def run_cell_canvas():

    global num_cols
    global num_rows
    global pixels_per_cell
    global caption

    '''
    Some Background...
    A pygame SURFACE is an object that represents a rectangular, two-dimensional image.
    A surface has fixed dimensions: width and height (in pixels).

    A pygame DISPLAY is a module that is used to manage the pygame application window.
    This is the window in which the pygame surfaces are displayed.
    The set_mode method returns a surface that represents the entire screen image within the window.

    A pygame COLOR is an RGB triplet. Each of the three values defines
    how much Red, Green, or Blue to mix into the color.
    Each R, G, and B value can be 0-255.
    '''

    # ----------------------------------------------------------------------------------------------+-
    # Setup the pygame display
    # ----------------------------------------------------------------------------------------------+-
    pg.init()
    display_size = (num_cols * pixels_per_cell, num_rows * pixels_per_cell)
    display_surface = pg.display.set_mode(display_size)
    pg.display.set_caption(caption)

    # ----------------------------------------------------------------------+-
    # MAIN LOOP
    # ----------------------------------------------------------------------+-
    quit = False
    while(not quit):

        # ----------------------------------------------------------------------+-
        # DISPATCH EVENTS
        #
        # Give each input event to the client so they can
        # take the appropriate action.
        # The client has the option to return false.
        # We use false to indicate the main loop should exit.
        # ----------------------------------------------------------------------+-
        for event in pg.event.get():
            quit = dispatch_next_event(event)

        # ----------------------------------------------------------------------+-
        # NEXT MATRIX
        #
        # Get the next array of cells from the client.
        # ----------------------------------------------------------------------+-
        nxt_matrix = get_next_matrix()

        # ----------------------------------------------------------------------+-
        # REDRAW THE DISPLAY
        #
        # Clear the display and redraw all of the cells.
        # ----------------------------------------------------------------------+-

        # Fill the entire surface with the solid background color.
        display_surface.fill(background_color)

        # For each cell on the canvas...
        for row, col in np.ndindex(nxt_matrix.shape):

            cell_color = nxt_matrix[row, col]

            # Draw a rectagle on the given surface.
            # The rectangle is defined by its (left,top) coordinates
            # and its width and height.
            # The rectangle's color is given by the value of cell.
            pg.draw.rect(
                display_surface, cell_color,
                # Consider making the following a pg.Rect
                (col*pixels_per_cell, row*pixels_per_cell, pixels_per_cell-1, pixels_per_cell-1)
            )

        # Now render it to the actual display window.
        pg.display.update()

        # ----------------------------------------------------------------------+-
        # LOOP DELAY
        #
        # Delay as per build-time configuration.
        # ----------------------------------------------------------------------+-
        if main_loop_delay >= 0:
            time.sleep(main_loop_delay)

    pg.quit()
    return

# ----------------------------------------------------------------------+-
# ----------------------------------------------------------------------+-
def main():


    # Perform the client's startup initialization tasks.
    startup_initialization()

    # Operate the cell canvas until it decides that it is finished.
    run_cell_canvas()

    sys.exit()
    return

# ----------------------------------------------------------------------+-
# This is the pythonic name-main idiom.
# Google it to learn what this does.
# ----------------------------------------------------------------------+-
if __name__ == "__main__":
    main()