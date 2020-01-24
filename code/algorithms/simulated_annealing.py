# TODO
"""
Short description of algorithm
"""

from classes.structure import House
import random

def simulated_annealing(area):

    # Iteration
    # TODO 1000 should be a variable
    # Nick: Why does it start at 1 and not 0?
    for j in range(1,1000):

        # Set temperature
        T = 1000 - j
        worth = area.calc_worth_area()

        # Tries to place house
        while True:
            
            # Pick random house and new coordinates
            k = int(random.random() * area.houses - 1)
            house = area.structures["House"][k]

            x = int(random.random() * (area.width - house.width + 1))
            y = int(random.random() * (area.height - house.height + 1))

            old_x = house.bottom_left_cor[0]
            old_y = house.bottom_left_cor[1]

            # Places house when valid
            if area.check_valid(house, x, y):
                move(area, house, x, y)
                new_worth = area.calc_worth_area()

                # Places house if worth more
                if worth > new_worth:
                    chance = random.random() * 1000

                    # Places house if worth less by chance
                    if T < chance:
                        move(area, house, old_x, old_y)
                break

def move(area, house, x, y):
    """
    Moves a house.
    """

    house.set_coordinates([x, y], house.horizontal)
    area.update_distances(house)
