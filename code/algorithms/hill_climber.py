"""
Short description of the algorithm
"""

# Retrieve area with objects of a random solution

# Repeat n times 

    # Loop over each house_object and move them in the 4 directions

    # Check if valid for each direction

    # Keep coordinates with highest calc_worth_area()

# Show plot before - after, with the worth

import random
from time import time
from classes.structure import House


def hill_climber(area):

    start = time()

    compare_area_worth = area.calc_worth_area()

    # counter = 1

    for i in range(1000):

        # print(counter)

        hill_climber_once(area)

        worth = area.calc_worth_area()

        if compare_area_worth < worth:
            compare_area_worth = worth
        else:
            break
        
        # counter += 1

    end = time()

    print(f"Runtime hill climber: {end - start}")
    
    print(f"Best worth: {worth}")
    
    area.plot_area()

def hill_climber_once(area):

    best_worth = 0

    move_directions = ["up", "right", "down", "left"]

    for house in area.structures["House"]:

        # store house coordinates
        saved_bottom_left = house.bottom_left_cor
        saved_top_right = house.top_right_cor
        
        x = house.bottom_left_cor[0]
        y = house.bottom_left_cor[1]

        best_bottom_left = house.bottom_left_cor
        best_top_right = house.top_right_cor
        
        # move object by the range in steps
        for move_steps in range(1,11):

            for direction in move_directions:

                if direction == "up":
                    move = [x, y + move_steps]
                elif direction == "right":
                    move = [x + move_steps, y]
                elif direction == "down":
                    move = [x, y - move_steps]
                elif direction == "left":
                    move = [x - move_steps, y]

                # Check if valid the move is valid 
                if area.check_valid(house, move[0], move[1]):

                    # Place the house in the new coordinates and check if the worth is the highest
                    place_house_hillclimbing(area, house, move, house.horizontal)
                    worth = area.calc_worth_area()
                    if worth > best_worth:
                        best_worth = worth
                        best_bottom_left = house.bottom_left_cor
                        best_top_right = house.top_right_cor

            # Restore the coordinate of the house object
            place_house_restore(area, house, saved_bottom_left, saved_top_right)  

        house.bottom_left_cor = best_bottom_left
        house.top_right_cor = best_top_right
        update_coordinates(area, house)

    # for h in area.structures["House"]:
    #     print(h)


def place_house_hillclimbing(area, house, bottom_left_cor, horizontal):

    house.set_coordinates(bottom_left_cor, horizontal)
    area.update_distances(house)  

def place_house_restore(area, house, bottom_left_cor, top_right_cor):
    
    house.bottom_left_cor = bottom_left_cor
    house.top_right_cor = top_right_cor
    update_coordinates(area, house)

def update_coordinates(area, house):
    
    house.set_corners()
    area.update_distances(house)