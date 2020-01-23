from algorithms.greedy_random import place_housesgreedyrandom
from algorithms.greedy_random import place_housegreedyrandom
from classes.structure import House
from algorithms.random import random_placement
import random

def hill_climber_random_random(area):
    for i in range(100000):
        worth = area.calc_worth_area()
        j = int(random.random() * area.houses)
        house = area.structures["House"][j]
        old_x = house.bottom_left_cor[0]
        old_y = house.bottom_left_cor[1]
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))
        if area.check_valid(house, x, y):
            place_housegreedyrandom(area, house, x, y)
            new_worth = area.calc_worth_area()
            if worth > new_worth:
                place_housegreedyrandom(area, house, old_x, old_y)
