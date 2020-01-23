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
from algorithms.hill_climber_random_random import hill_climber_random_random
from algorithms.hill_climber_steps import hill_climber_steps
from algorithms.evolution import evolution
from algorithms.simulated_annealing import simulated_annealing


HOUSES = 20
NEIGHBOURHOOD = "wijk1"
ALGORITHM = "greedy_random"
HILL_CLIMBER = "hill_climber_random_random"
# HILL_CLIMBER = None

def main():

    set_random_seed(0.4906269926668486)

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    area.plot_area(NEIGHBOURHOOD, HOUSES, ALGORITHM)

    area.make_csv_output()

    if HILL_CLIMBER:
    
        start = time()

        hill_climber(area, HILL_CLIMBER)

        hill_climber_steps(area)

        area.plot_area(NEIGHBOURHOOD, HOUSES, HILL_CLIMBER)

        end = time()

        print(f"Runtime {HILL_CLIMBER}: {end - start}")
        
        # area.make_csv_output()

def algorithm(area, algorithm_name):

    start = time()

    if algorithm_name == "random":
        random_placement(area)

    elif algorithm_name == "greedy":
        place_housesgreedy(area)

    elif algorithm_name == "greedy_random":
        place_housesgreedyrandom(area)

    elif algorithm_name == "evolution":
        evolution(area)

    else:
        raise Exception("Invalid algorithm name")

    end = time()

    # print(f"Runtime {algorithm_name}: {end - start}")

    # for h in area.structures["House"]:
    #     print(h)

def hill_climber(area, hill_climber_name):

    if hill_climber_name == "hill_climber_steps":
        hill_climber_steps(area)

    elif hill_climber_name == "hill_climber_random":
        hill_climber_random(area)

    elif hill_climber_name == "hill_climber_random_random":
        hill_climber_random_random(area)

    elif hill_climber_name == "simulated_annealing":
        simulated_annealing(area)
    else:
        raise Exception("Invalid hill climber name")

    # for h in area.structures["House"]:
    #     print(h)


def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    # print(f"Seed: {r}")

    return r


if __name__ == "__main__":
    main()
