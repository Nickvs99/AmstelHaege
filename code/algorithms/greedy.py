"""
Tries to place the houses one by one on every place and picks the best spot
"""

import random
from classes.structure import House

def greedy(area, house):
    """
    iterates over every place for a house and gets best value. 
    """
    best_worth = 0

    # Checks place for house
    for y in range(area.height - house.height + 1):
        for x in range(area.width - house.width + 1):

            # Check if valid the move is valid for both orientations
            for orientation in [True, False]:
                house.set_coordinates([x,y], orientation)
                if area.check_valid(house, x, y):
                    area.update_distances(house)
                    worth = area.calc_worth_area()

                    # Selects best place for house
                    if worth > best_worth:
                        best_worth = worth
                        best_x = x
                        best_y = y
                        best_orientation = orientation

    # Places house in best place
    house.set_coordinates([best_x, best_y], best_orientation)
    area.update_distances(house)

def place_houses_greedy(area):
    """ Places each house-object randomly on the given area. """

    # Makes house-objects
    area.create_houses(False)
    for house in area.houses:

        area.structures["House"].append(house)
        greedy(area, house)
