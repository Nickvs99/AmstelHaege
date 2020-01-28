"""
Tries to place the houses one by one an x amount of random.
It then chooses the best spot.
"""

import random
from classes.structure import House
from settings import greedy_random_settings as settings

def greedy(area, house):
    """
    Tries x amount of random places and places it on the best position for
    that house.
    """

    best_worth = area.calc_worth_area()
    min_dist = min(house.width, house.height)
    for i in range(settings["iterations"]):

        x = int(random.random() * (area.width - min_dist + 1))
        y = int(random.random() * (area.height - min_dist + 1))

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
    house.set_coordinates([best_x,best_y], best_orientation)
    area.update_distances(house)

def create_houses_greedy(area, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with houses. """

        houses = []
        for i in range(maison_count):
            house = House("maison_" + str(i), True)
            houses.append(house)

        for i in range(bungalow_count):
            house = House("bungalow_" + str(i), True)
            houses.append(house)

        for i in range(one_person_house_count):
            house = House("one_person_home_" + str(i), True)
            houses.append(house)

        for h in houses:
            h.init_distances(houses)

        return houses

def place_houses_greedy_random(area):
    """ Creates houses and runs greed on them. """

    houses = create_houses_greedy(area, area.one_person_house_count, area.bungalow_count, area.maison_count)

    for house in houses:

        area.structures["House"].append(house)
        greedy(area, house)
