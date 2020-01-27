from algorithms.greedy_random import place_housesgreedyrandom
from algorithms.greedy_random import place_housegreedyrandom
from classes.structure import House
from algorithms.random import random_placement
import random

from settings import simulated_annealing_settings as settings

def simulated_annealing(area):
    # for i in range(100):
    #     print("iteratie")
    #     print(i)
    #     print(area.calc_worth_area())

    for j in range(settings["iterations"]):
        T = settings["iterations"] - j
        print(j)
        worth = area.calc_worth_area()
        x = 0
        y = 0
        house = area.structures["House"][0]
        while not area.check_valid(house, x, y):
            k = int(random.random() * area.houses)
            house = area.structures["House"][k]
            old_x = house.bottom_left_cor[0]
            old_y = house.bottom_left_cor[1]
            x = int(random.random() * (area.width - house.width + 1))
            y = int(random.random() * (area.height - house.height + 1))
            if area.check_valid(house, x, y):
                place_housegreedyrandom(area, house, x, y)
                new_worth = area.calc_worth_area()
                if worth > new_worth:
                    chance = random.random() * settings["iterations"]
                    if T < chance:
                        place_housegreedyrandom(area, house, old_x, old_y)
