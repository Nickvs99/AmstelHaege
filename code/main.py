import random
from classes.area import Area
from algorithms.random import random_placement
from algorithms.greedy import place_housesgreedy

ALGORITHM = "random"
NEIGHBOURHOOD = "wijk2"
HOUSES = 20

def main():

    start = timeit.default_timer()

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    stop = timeit.default_timer()
    print('Runtime: ', stop - start)

    area.plot_area()
    
    area.make_csv_output()

def algorithm(area, algorithm_name):

    # TODO switch case statement
    if algorithm_name == "random":
        random_placement(area)

    elif algorithm_name == "greedy":
        place_housesgreedy(area)

    elif algorithm_name == "greedy_random":
        greedy_random(area)

    else:
        raise Exception("Invalid algorithm name")


def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    print(f"Seed: {r}")


if __name__ == "__main__":
    main()