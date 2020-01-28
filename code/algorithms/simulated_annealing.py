"""
Tries to place a random house on a random location for an x amount of times.
If better it places the house. If not it places the house by chance.
The chance decreases over the amount of iterations.
"""

from classes.structure import House
import random

from settings import simulated_annealing_settings as settings

def simulated_annealing(area):

    for j in range(settings["iterations"]):
        T = settings["iterations"] - j

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

                    chance = random.random() * settings["iterations"]

                    if T < chance:
                        move(area, house, old_x, old_y)
                break

def move(area, house, x, y):
    """
    Moves a house.
    """

    house.set_coordinates([x, y], house.horizontal)
    area.update_distances(house)
