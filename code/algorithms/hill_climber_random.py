"""
Short description of the algorithm
"""
from classes.structure import House
import random

def hill_climber_random(area):
    worth_global = area.calc_worth_area()
    worth = 0

    # Iteration until no improvement
    for i in range(100):
        if worth < worth_global:
            worth = worth_global
            for house in area.structures["House"]:
                # Stops in hillcliber
                greedyhill_climber(area, house)
            worth_global = area.calc_worth_area()


def greedyhill_climber(area, house):
    best_worth = area.calc_worth_area()
    best_orientation = house.horizontal
    best_x = house.bottom_left_cor[0]
    best_y = house.bottom_left_cor[1]

    # Iterates 1000 times for each house
    for i in range(1000):

        # Sets location for house
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))

        # Checks score for house horizotally
        house.set_orientation(True)
        if area.check_valid(house, x, y):
            move(area, house, x, y)
            worth = area.calc_worth_area()

            # Selects best place for house
            if worth > best_worth:
                best_worth = worth
                best_x = x
                best_y = y
                best_orientation = True

        #Checks score for house vertically
        house.set_orientation(False)
        if area.check_valid(house, x, y):
            move(area, house, x, y)
            worth = area.calc_worth_area()

            # Selects best place for house
            if worth > best_worth:
                best_worth = worth
                best_x = x
                best_y = y
                best_orientation = False

    # Places house in best place
    house.set_orientation(best_orientation)
    move(area, house, best_x, best_y)

def move(area, house, x, y):
    """
    Moves a house.
    """

    house.bottom_left_cor = [x, y]
    house.top_right_cor = [x + house.width, y + house.height]
    house.set_corners()

    area.update_distances(house)
