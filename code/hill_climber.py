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

        saved_bottom_left = house.bottom_left_cor
        saved_top_right = house.top_right_cor
        
        best_bottom_left = house.bottom_left_cor
        best_top_right = house.top_right_cor
        
        for move_steps in range(1,10):

            # for direction in move_directions:

            # Move up
            if area.check_valid(house, house.bottom_left_cor[0],house.bottom_left_cor[1] + move_steps):
                place_house_hillclimbing(area, house, "up", move_steps)
                worth = area.calc_worth_area()
                if worth > best_worth:
                    best_worth = worth
                    best_bottom_left = house.bottom_left_cor
                    best_top_right = house.top_right_cor

            place_house_restore(area, house, saved_bottom_left, saved_top_right)            
                
            # Move right
            if area.check_valid(house, house.bottom_left_cor[0] + move_steps,house.bottom_left_cor[1]):
                place_house_hillclimbing(area, house, "right", move_steps)
                worth = area.calc_worth_area()
                if worth > best_worth:
                    best_worth = worth
                    best_bottom_left = [house.bottom_left_cor[0] + move_steps,house.bottom_left_cor[1]]
                    best_top_right = [house.top_right_cor[0] + move_steps,house.top_right_cor[1]]

            place_house_restore(area, house, saved_bottom_left, saved_top_right)

            # Move down
            if area.check_valid(house, house.bottom_left_cor[0],house.bottom_left_cor[1] - move_steps):
                place_house_hillclimbing(area, house, "down", move_steps)
                worth = area.calc_worth_area()
                if worth > best_worth:
                    best_worth = worth
                    best_bottom_left = [house.bottom_left_cor[0],house.bottom_left_cor[1] - move_steps]
                    best_top_right = [house.top_right_cor[0],house.top_right_cor[1] - move_steps]

            place_house_restore(area, house, saved_bottom_left, saved_top_right)

            # Move left
            if area.check_valid(house, house.bottom_left_cor[0] - move_steps,house.bottom_left_cor[1]):
                place_house_hillclimbing(area, house, "left", move_steps)
                worth = area.calc_worth_area()
                if worth > best_worth:
                    best_worth = worth
                    best_bottom_left = [house.bottom_left_cor[0] - move_steps,house.bottom_left_cor[1]]
                    best_top_right = [house.top_right_cor[0] - move_steps,house.top_right_cor[1]]
            
            place_house_restore(area, house, saved_bottom_left, saved_top_right)

        house.bottom_left_cor = best_bottom_left
        house.top_right_cor = best_top_right
        house.set_corners()
        area.update_distances(house)

    print(f"Best worth: {best_worth}")
    for h in area.structures["House"]:
        print(h)

    area.plot_area()

def place_house_hillclimbing(area, house, move_direction, move_steps):

    if move_direction == "up":
        house.bottom_left_cor[1] = house.bottom_left_cor[1] + move_steps
        house.top_right_cor[1] = house.top_right_cor[1] + move_steps
    
    elif move_direction == "right":
        house.bottom_left_cor[0] = house.bottom_left_cor[0] + move_steps
        house.top_right_cor[0] = house.top_right_cor[0] + move_steps
    
    elif move_direction == "down":
        house.bottom_left_cor[1] = house.bottom_left_cor[1] - move_steps
        house.top_right_cor[1] = house.top_right_cor[1] - move_steps

    elif move_direction == "left":
        house.bottom_left_cor[0] = house.bottom_left_cor[0] - move_steps
        house.top_right_cor[0] = house.top_right_cor[0] - move_steps

    house.set_corners()
    area.update_distances(house)

def place_house_restore(area, house, bottom_left_cor, top_right_cor):
    
    house.bottom_left_cor = bottom_left_cor
    house.top_right_cor = top_right_cor
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