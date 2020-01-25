"""
main.py
"""

import sys
import random
from time import time

from classes.area import Area
from algorithms.random import random_placement
from algorithms.greedy import place_housesgreedy
from algorithms.greedy_random import place_housesgreedyrandom
from algorithms.hill_climber_steps import hill_climber_steps
from algorithms.hill_climber_random import hill_climber_random
from algorithms.hill_climber_random_random import hill_climber_random_random
from algorithms.evolution import evolution
from algorithms.simulated_annealing import simulated_annealing


def main():

    start = time()

    neighbourhood, houses, algorithm, hill_climber = check_argv()

    seed = set_random_seed()

    area = get_area(neighbourhood, houses, algorithm, hill_climber)
    
    end = time()

    print(f"Seed: {seed} \nRuntime: {end - start}")
    
    area.make_csv_output()

    area.plot_area(neighbourhood, houses, algorithm)


def get_area(neighbourhood, houses, algorithm_name, hill_climber_name):

    area = Area(neighbourhood, houses)

    algorithm(area, algorithm_name)

    if hill_climber_name:

        hill_climber(area, hill_climber_name)

        hill_climber_steps(area)

    return area


def algorithm(area, algorithm_name):
    """ Runs the specific algorithm """

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


def hill_climber(area, hill_climber_name):
    """ Runs the specific hill climber """

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


def check_argv():

    if len(sys.argv) == 4:

        neighbourhood, houses, algorithm = check_neighbourhood_houses_algorithm()

        return neighbourhood, houses, algorithm, None

    elif len(sys.argv) == 5:
        
        if sys.argv[4].lower() not in ["hill_climber_steps", "hill_climber_random", "hill_climber_random_random", "simulated_annealing"]:
            print("Fifth argument must be: 'hill_climber_steps', 'hill_climber_random', 'hill_climber_random_random' or\n \
                            'simulated_annealing'")
            sys.exit (1)
        else:
            neighbourhood, houses, algorithm = check_neighbourhood_houses_algorithm()

            return neighbourhood, houses, algorithm, sys.argv[4].lower()

    else:
        print("Usage: python main.py neighbourhood houses algorithm \n or \
        \nUsage: python main.py neighbourhood houses algorithm hill_climber")
        sys.exit (1)


def check_neighbourhood_houses_algorithm():

    if sys.argv[1].lower() not in ["wijk1", "wijk2", "wijk3"]:
        print("Second argument must be: 'wijk1', 'wijk2' or 'wijk3'")
        sys.exit (1)

    elif not sys.argv[2].isdigit():
        print("Third argument must be a digit")
        sys.exit (1)

    ## (Optional - functions raise exception if invalid)
    elif sys.argv[3].lower() not in ["random", "greedy", "random_greedy", "evolution"]:
        print("Fourth argument must be: 'random', 'greedy', 'random_greedy' or 'evolution'")
        sys.exit (1)

    else:        
        return sys.argv[1].lower(), int(sys.argv[2]), sys.argv[3].lower()
        

def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    return r


if __name__ == "__main__":
    main()
