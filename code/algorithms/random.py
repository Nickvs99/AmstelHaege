"""
Random algorithm

Places all houses at a random spot. Constrains for this spot are:
- a house doesn't overlap with another house
- a house doesn't overlap with water
- a house fits on the grid
"""

import random
from classes.structure import House

def random_placement(area):
    """ Places a new set of house-objects on a given area. """

    area.create_houses(True)

    for house in area.houses:
        place_house(area, house)

def place_house(area, house):
    """
    Places a house
    It picks a random x and y coordinate and then checks if there is room for the new house.
    If it does not succeed, try new coordinates.
    """

    while_count = 0
    valid = False
    while not valid:

        # Get random bottom_left coordinates
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))

        house.set_coordinates([x,y], house.horizontal)

        if area.check_valid(house, x, y):
            valid = True

        if while_count == 1000:

            raise Exception("Something went wrong when placing a house. There was probably too little room to fit an extra house.") 
        
        while_count += 1


    area.structures["House"].append(house)
    area.update_distances(house)
