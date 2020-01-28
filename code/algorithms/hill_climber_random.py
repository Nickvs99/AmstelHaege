"""
Tries every house an x amount of times and places it in the best position.
It does that until a cycle of placing every house gives no improvement.
"""
from classes.structure import House
import random

from settings import hill_climber_random_settings as settings

def hill_climber_random(area):

    worth_global = area.calc_worth_area()

    for i in range(settings["iterations"]):

        if worth < worth_global:
            worth = worth_global
            for house in area.structures["House"]:
                # Starts hillcimbing for a house
                greedy_hill_climber(area, house)
            worth_global = area.calc_worth_area()

def greedy_hill_climber(area, house):
    
    best_worth = area.calc_worth_area()
    best_orientation = house.horizontal
    best_x = house.bottom_left_cor[0]
    best_y = house.bottom_left_cor[1]

    # Checks place for house
    for i in range(settings["iterations_house"]):
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))

        # Checks score for house
        for orientation in [True, False]:
            house.set_coordinates([x, y], orientation)
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
