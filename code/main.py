"""
main.py

The main program to retrieve the solutions of the case. The user will be requested 
to insert the neighbourhood, amount of houses, algorithm and (optional) the hill_climber
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

from settings import main_settings as settings 


def main():
    """ Main function """

    start = time()

    neighbourhood, houses, algorithm, hill_climber = check_argv()

    seed = set_random_seed()

    area = get_area(neighbourhood, houses, algorithm, hill_climber)
    
    end = time()

    print(f"Seed: {seed} \nRuntime: {end - start}")
    
    area.make_csv_output()

    area.plot_area(neighbourhood, houses, algorithm)


def get_area(neighbourhood, houses, algorithm_name, hill_climber_name):
    """ 
    Runs the specific algorithm with hill_climber, if requested.
    And returns the generated area. 
    """

    area = Area(neighbourhood, houses)

    algorithm(area, algorithm_name)

    if hill_climber_name:

        hill_climber(area, hill_climber_name)

    return area


def algorithm(area, algorithm_name):
    """ Runs the specific algorithm with the given area. """

    if algorithm_name == "random":
        random_placement(area)

    elif algorithm_name == "greedy":
        place_housesgreedy(area)

    elif algorithm_name == "greedy_random":
        place_housesgreedyrandom(area)

    elif algorithm_name == "evolution":
        get_alpha_and_beta(area)


def hill_climber(area, hill_climber_name):
    """ Runs the specific hill climber with the given area. """

    if hill_climber_name == "hill_climber_steps":
        hill_climber_steps(area)

    elif hill_climber_name == "hill_climber_random":
        hill_climber_random(area)

    elif hill_climber_name == "hill_climber_random_random":
        hill_climber_random_random(area)

    elif hill_climber_name == "simulated_annealing":
        simulated_annealing(area)


def check_argv():
    """ Checks the command-line arguments for validity. """

    hill_climber_list = ["hill_climber_steps", "hill_climber_random", 
                            "hill_climber_random_random", "simulated_annealing"]

    neighbourhood, houses, algorithm = check_neighbourhood_houses_algorithm()
    
    # Command-line without hill climber
    if len(sys.argv) == 4:
        
        return neighbourhood, houses, algorithm, None

    # Command-line with hill climber
    elif len(sys.argv) == 5:
        
        if sys.argv[4].lower() not in hill_climber_list:
            print(f"Hill climber must be: {str(hill_climber_list)[1:-1]}")
            sys.exit (1)
        
        else:
            return neighbourhood, houses, algorithm, sys.argv[4].lower()

    else:
        print("Usage: python main.py neighbourhood amount_houses algorithm \n or \
        \nUsage: python main.py neighbourhood amount_houses algorithm hill_climber")
        sys.exit (1)


def check_neighbourhood_houses_algorithm():
    """ Checks the arguments for the neighbourhood, amount of houses and the algorithm. """

    neighbourhood_list = ["wijk1", "wijk2", "wijk3"]
    algorithm_list = ["random", "greedy", "greedy_random", "evolution"]

    if sys.argv[1].lower() not in neighbourhood_list:
        print(f"Neighbourhood must be: {str(neighbourhood_list)[1:-1]}")
        sys.exit (1)

    elif not sys.argv[2].isdigit():
        print("Amount of houses must be a digit")
        sys.exit (1)

    elif sys.argv[3].lower() not in algorithm_list:
        print(f"Algorithm must be: {str(algorithm_list)[1:-1]}")
        sys.exit (1)

    # If valid, return their values
    else:        
        return sys.argv[1].lower(), int(sys.argv[2]), sys.argv[3].lower()
        

def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    return r


if __name__ == "__main__":
    main()
