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
from classes.area import Area
from algorithms.random import random_placement
from algorithms.greedy import place_housesgreedy
from algorithms.greedy_random import place_housesgreedyrandom
from best_result import best_result
from time import time

ALGORITHM = "random"
NEIGHBOURHOOD = "wijk2"
HOUSES = 10

def main():

    set_random_seed()

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    area.plot_area()

    hill_climber(area)

def hill_climber(area):

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
        for move_steps in range(1,10):

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
                    place_house_hillclimbing(area, house, move, move_steps)
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

    print(f"Best worth: {best_worth}")
    for h in area.structures["House"]:
        print(h)

    area.plot_area()

def place_house_hillclimbing(area, house, move, move_steps):

    house.bottom_left_cor = move
    house.top_right_cor = [move[0] + house.width, move[1] + house.height]
    update_coordinates(area, house)

def place_house_restore(area, house, bottom_left_cor, top_right_cor):
    
    house.bottom_left_cor = bottom_left_cor
    house.top_right_cor = top_right_cor
    update_coordinates(area, house)

def update_coordinates(area, house):
    
    house.set_corners()
    area.update_distances(house)

def algorithm(area, algorithm_name):

    start = time()

    # TODO switch case statement
    if algorithm_name == "random":
        random_placement(area)

    elif algorithm_name == "greedy":
        place_housesgreedy(area)

    elif algorithm_name == "greedy_random":
        place_housesgreedyrandom(area)

    else:
        raise Exception("Invalid algorithm name")

    end = time()

    # print(f"Runtime: {end - start}")
    print(f"Worth: {area.calc_worth_area()}")
    for h in area.structures["House"]:
        print(h)
    
def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    print(f"Seed: {r}")


if __name__ == "__main__":
    main()