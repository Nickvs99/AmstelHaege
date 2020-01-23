"""
Short description of the algorithm
"""

import random
from classes.structure import House

def greedy(area, house):
    best_x = 0
    best_y = 0
    best_worth = 0

    # Checks place for house
    for y in range(area.height - house.height + 1):
        for x in range(area.width - house.width + 1):
            house.set_coordinates([x,y], True)
            if area.check_valid(house, x, y):
                area.update_distances(house)
                worth = area.calc_worth_area()

                # Selects best place for house
                if worth > best_worth:
                    best_worth = worth
                    best_x = x
                    best_y = y
                    best_orientation = True

            house.set_coordinates([x,y], False)
            if area.check_valid(house, x, y):
                area.update_distances(house)
                worth = area.calc_worth_area()

                # Selects best place for house
                if worth > best_worth:
                    best_worth = worth
                    best_x = x
                    best_y = y
                    best_orientation = False


    # Places house in best place
    house.set_coordinates([best_x, best_y], best_orientation)
    area.update_distances(house)


def create_houses_greedy(area, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with houses. """

        houses = []

        for i in range(maison_count):
            r = random.choice([True])
            house = House("maison_" + str(i), r)
            houses.append(house)

        for i in range(bungalow_count):
            r = random.choice([True])
            house = House("bungalow_" + str(i), r)
            houses.append(house)

        for i in range(one_person_house_count):
            r = random.choice([True])
            house = House("one_person_home_" + str(i), r)
            houses.append(house)

        for h in houses:
            h.init_distances(houses)

        return houses

def place_housesgreedy(area):
    """ Places the houses randomly. """

    # Makes houses
    houses = create_houses_greedy(area, area.one_person_house_count, area.bungalow_count, area.maison_count)
    for house in houses:
        house.set_coordinates([0,0], house.horizontal)
        area.structures["House"].append(house)
        greedy(area, house)
