"""
main.py
"""


import random
from time import time

from classes.area import Area
from algorithms.random import random_placement
from algorithms.greedy import place_housesgreedy
from algorithms.greedy_random import place_housesgreedyrandom
from algorithms.hill_climber_random import hill_climber_random
from algorithms.hill_climber_steps import hill_climber_steps


HOUSES = 10
NEIGHBOURHOOD = "wijk2"
ALGORITHM = "random"
# HILL_CLIMBER = "hill_climber_steps"
HILL_CLIMBER = None


def main():

    set_random_seed()

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    area.plot_area(NEIGHBOURHOOD, HOUSES, ALGORITHM)
    
    area.make_csv_output(HILL_CLIMBER)

    hill_climber(area, HILL_CLIMBER)

    area.plot_area(NEIGHBOURHOOD, HOUSES, HILL_CLIMBER)
    
    area.make_csv_output(HILL_CLIMBER)

def algorithm(area, algorithm_name):

    start = time()

    # TODO switch case statement
    if algorithm_name == "random":
        random_placement(area)

    elif algorithm_name == "greedy":
        place_housesgreedy(area)

    elif algorithm_name == "greedy_random":
        place_housesgreedyrandom(area)

    else:
        raise Exception("Invalid algorithm name")

    end = time()

    print(f"Runtime: {end - start}")
    
    # for h in area.structures["House"]:
    #     print(h)

def hill_climber(area, hill_climber_name):

    if hill_climber_name == "hill_climber_steps":
        hill_climber_steps(area)

    elif hill_climber_name == "hill_climber_random":
        hill_climber_random(area)

def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    print(f"Seed: {r}")

    return r


if __name__ == "__main__":
    main()
