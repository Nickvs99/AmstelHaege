"""
Short description of the algorithm
"""

import random
from classes.structure import House


def random_placement(area):
    
    place_houses(area)


def create_houses(area, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with houses. """

        houses = []
        for i in range(maison_count):
            r = random.choice([True, False])
            houses.append(House("maison", r))

        for i in range(bungalow_count):
            r = random.choice([True, False])
            houses.append(House("bungalow", r))

        for i in range(one_person_house_count):
            r = random.choice([True, False])
            houses.append(House("one_person_home", r))

        return houses

def place_houses(area):
    """ Places the houses randomly. """

    houses = create_houses(area, area.one_person_house_count, area.bungalow_count, area.maison_count)

    for house in houses:
        place_house(area, house)

def place_house(area, house):
    """
    Place a house.
    It picks a random x and y coordinate and then checks if there is room for the new house.
    If it does not succeed, try new coordinates.
    """

    house_placed = False
    while_count = 0
    while not house_placed and while_count < 1000:

        # Get random bottom_left x and y coordinate
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))

        if area.check_valid(house, x, y):
            
            house.bottom_left_cor = [x, y]
            house.top_right_cor = [x + house.width, y + house.height]
            house.set_corners()

            area.structures["House"].append(house)

            house_placed = True

        while_count += 1

    if while_count == 1000:

        raise Exception("Something went wrong when placing a house. There was probably to little room to fit an extra house.") 
