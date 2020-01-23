"""
Short description of the algorithm
"""
from algorithms.greedy_random import place_housegreedyrandom
from classes.structure import House
import random

def hill_climber_random(area):
    worth_global = area.calc_worth_area()

    worth = 0

    for i in range(100):
        if worth < worth_global:
            worth = worth_global
            place_houseshill_climber(area)
            worth_global = area.calc_worth_area()

def place_houseshill_climber(area):
    """ iterates through houses. """

    # Makes houses
    for house in area.structures["House"]:
        greedyhill_climber(area, house)

def greedyhill_climber(area, house):
    best_worth = area.calc_worth_area()
    best_orientation = house.horizontal
    best_x = house.bottom_left_cor[0]
    best_y = house.bottom_left_cor[1]

    # Checks place for house
    for i in range(1000):
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))
        house.set_orientation(True)
        if area.check_valid(house, x, y):
            place_housegreedyrandom(area, house, x, y)
            worth = area.calc_worth_area()

            # Selects best place for house
            if worth > best_worth:
                best_worth = worth
                best_x = x
                best_y = y
                best_orientation = True

        house.set_orientation(False)
        if area.check_valid(house, x, y):
            place_housegreedyrandom(area, house, x, y)
            worth = area.calc_worth_area()
            # Selects best place for house
            if worth > best_worth:
                best_worth = worth
                best_x = x
                best_y = y
                best_orientation = False

    # Places house in best place
    house.set_orientation(best_orientation)
    place_housegreedyrandom(area, house, best_x, best_y)

def place_housegreedyrandom(area, house, x, y):
    """
    Place a house.
    """

    house.bottom_left_cor = [x, y]
    house.top_right_cor = [x + house.width, y + house.height]
    house.set_corners()

    area.update_distances(house)
