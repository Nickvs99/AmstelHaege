"""
This interpretation of hill climbing works on a generated solution.
Each house object will be moved in specific steps horizontally and vertically.
All the moves will be checked for validation and the best results stored.
This process will be iterated and stopped if the best area is found.
"""

from time import time
from classes.structure import House


def hill_climber_steps(area, neighbourhood, houses, algorithm):
    """ 
    Iterates over single hill climbers and returns the area with the highest worth.
    """

    start = time()

    counter = 1

    compare_area_worth = area.calc_worth_area()

    for i in range(1000):

        hill_climber_once(area)

        worth = area.calc_worth_area()

        if compare_area_worth < worth:
            compare_area_worth = worth
        else:
            print(f"{counter} iterations needed")
            break

        counter += 1

    end = time()

    print(f"Runtime hill climber (steps): {end - start}")
    
    # print(f"Best worth: {worth}")
    # for h in area.structures["House"]:
    #     print(h)
    
    area.plot_area(neighbourhood, houses, algorithm)

def hill_climber_once(area):
    """ 
    Moves each house object seperatly and stores the coordinates with the best area worth.
    """

    best_worth = 0

    move_directions = ["up", "right", "down", "left"]

    for house in area.structures["House"]:

        # store house coordinates
        saved_bottom_left = house.bottom_left_cor
        saved_orientation = house.horizontal

        best_bottom_left = house.bottom_left_cor
        best_orientation = house.horizontal
        
        # move object by the range in steps
        for move_steps in range(1,11):

            for direction in move_directions:

                if direction == "up":
                    move = [house.bottom_left_cor[0], house.bottom_left_cor[1] + move_steps]
                elif direction == "right":
                    move = [house.bottom_left_cor[0] + move_steps, house.bottom_left_cor[1]]
                elif direction == "down":
                    move = [house.bottom_left_cor[0], house.bottom_left_cor[1] - move_steps]
                elif direction == "left":
                    move = [house.bottom_left_cor[0] - move_steps, house.bottom_left_cor[1]]
                
                # Check if valid the move is valid for both orientations
                for orientation in [True, False]:
                    
                    house.set_coordinates(move, orientation)

                    if area.check_valid(house, move[0], move[1]):

                        # Place the house in the new coordinates and checks highest worth
                        area.update_distances(house)
                        worth = area.calc_worth_area()
                        if worth > best_worth:
                            best_worth = worth
                            best_bottom_left = house.bottom_left_cor
                            best_orientation = orientation

            # Restore the coordinate of the house object
            place_house_hillclimbing(area, house, saved_bottom_left, saved_orientation)  

        # Place house with the best configuration
        place_house_hillclimbing(area, house, best_bottom_left, best_orientation)


def place_house_hillclimbing(area, house, bottom_left_cor, horizontal):
    """ 
    Updates coordinates and orientation of the house object and area. 
    """

    house.set_coordinates(bottom_left_cor, horizontal)
    area.update_distances(house)