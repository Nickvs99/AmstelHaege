"""
Tries every house an x amount of times and places it in the best position.
It does that until a cycle of placing every house gives no improvement.
"""
from classes.structure import House
import random

from settings import iterations

def hill_climber_random(area):
    """
    Iterates x amount of times over each house-object and relocate 
    each house-object by coordinates.
    """
    prev_worth = area.calc_worth_area()
    new_worth = prev_worth + 1

    # Keep running until no improvement
    while prev_worth < new_worth:

        for house in area.structures["House"]:
            # Starts hillcimbing for a house
            greedy_hill_climber(area, house)
        prev_worth = new_worth
        new_worth = area.calc_worth_area()

def greedy_hill_climber(area, house):
    
    best_worth = area.calc_worth_area()
    best_orientation = house.horizontal
    best_x = house.bottom_left_cor[0]
    best_y = house.bottom_left_cor[1]

    # Checks place for house
    for i in range(iterations["hill_climber_random"]):
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
