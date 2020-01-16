import random
from classes.area import Area
from algorithms.random import random_placement
from algorithms.greedy import place_housesgreedy
from algorithms.greedy_random import place_housesgreedyrandom
from algorithms.hill_climber import hill_climber
from time import time

ALGORITHM = "random"
NEIGHBOURHOOD = "wijk2"
HOUSES = 10

def main():

    set_random_seed(0.6113775665997402)

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    area.plot_area()
    
    # area.make_csv_output()

    hill_climber(area)

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
    print(f"Worth: {area.calc_worth_area()}")
    for h in area.structures["House"]:
        print(h)
    
def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    print(f"Seed: {r}")


if __name__ == "__main__":
    main()
