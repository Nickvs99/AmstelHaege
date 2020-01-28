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
    house.set_coordinates([best_x, best_y], best_orientation)
    area.update_distances(house)


def create_houses_greedy(area, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with all house-objects. """

        houses = []

        for i in range(bungalow_count):
            r = random.choice([True])
            house = House("bungalow_" + str(i), r)
            houses.append(house)

        for i in range(maison_count):
            r = random.choice([True])
            house = House("maison_" + str(i), r)
            houses.append(house)

        for i in range(one_person_house_count):
            r = random.choice([True])
            house = House("one_person_home_" + str(i), r)
            houses.append(house)

        for h in houses:
            h.init_distances(houses)

        return houses

def place_housesgreedy(area):
    """ Places each house-object randomly on the given area. """

    # Makes house-objects
    houses = create_houses_greedy(area, area.one_person_house_count, area.bungalow_count, area.maison_count)
    counter = 0
    for house in houses:
        print(counter)

        house.set_coordinates([0,0], house.horizontal)
        area.structures["House"].append(house)
        greedy(area, house)
        print(area.calc_worth_area())

        counter += 1