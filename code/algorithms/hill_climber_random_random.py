"""
Tries to place a random house on a random location and places it when it scores better.
It does this an x amount of times.
"""

from classes.structure import House
import random

from settings import iterations

def hill_climber_random_random(area):
    """
    Iterates over random houses and makes changes.
    """
    
    for i in range(iterations["hill_climber_random_random"]):
        worth = area.calc_worth_area()

        # Picks random house and new coordinates
        selected_house_number = int(random.random() * area.houses_count - 1)
        house = area.structures["House"][selected_house_number]

        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))

        old_x = house.bottom_left_cor[0]
        old_y = house.bottom_left_cor[1]
        old_orientation = house.horizontal

        # Checks if the move is valid and moves house
        for orientation in[True, False]:
            house.set_orientation(orientation)
            if area.check_valid(house, x, y):
                move(area, house, x, y)
                new_worth = area.calc_worth_area()

                # Places house back if the move gets a lower score
                if worth > new_worth:
                    house.set_orientation(old_orientation)
                    move(area, house, old_x, old_y)

def move(area, house, x, y):
    """
    Moves a house to a new position [x, y].
    """

    house.set_coordinates([x, y], house.horizontal)
    area.update_distances(house)
