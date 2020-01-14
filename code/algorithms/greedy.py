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
            if area.check_valid(house, x, y):
                place_housegreedy(area, house, x, y)
                worth = area.calc_worth_area()

                # Selects best place for house
                if worth > best_worth:
                    best_worth = worth
                    best_x = x
                    best_y = y

    # Places house in best place
    place_housegreedy(area, house, best_x, best_y)
    
def create_houses_greedy(area, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with houses. """

        houses = []
        for i in range(maison_count):
            r = random.choice([True])
            house = House("maison", r)
            house.structure_name = "maison_" + str(i)
            houses.append(house)
        for i in range(bungalow_count):
            r = random.choice([True])
            house = House("bungalow", r)
            house.structure_name = "bungalow_" + str(i)
            houses.append(house)
        for i in range(one_person_house_count):
            r = random.choice([True])
            house = House("one_person_home", r)
            house.structure_name = "one_person_home_" + str(i)
            houses.append(house)

        
        for h in houses:
            h.init_distances(houses)

        return houses

def place_housesgreedy(area):
    """ Places the houses randomly. """

    # Makes houses
    houses = create_houses_greedy(area, area.one_person_house_count, area.bungalow_count, area.maison_count)
    counter = 0
    for house in houses:
        print(counter)

        # Places the rest of the houses
        if counter >= 1:
            house.bottom_left_cor = [0, 0]
            house.top_right_cor = [0 + house.width, 0 + house.height]
            house.set_corners()
            area.structures["House"].append(house)
            greedy(area, house)
            print(area.calc_worth_area())

        # Places house in first position
        else:
            house.bottom_left_cor = [74, 85]
            house.top_right_cor = [74 + house.width, 85 + house.height]

            house.set_corners()

            area.structures["House"].append(house)
        counter += 1

def place_housegreedy(area, house, x, y):
    """
    Place a house.
    """

    house.bottom_left_cor = [x, y]
    house.top_right_cor = [x + house.width, y + house.height]
    house.set_corners()

    area.update_distances(house)
