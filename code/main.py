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
from algorithms.greedy import place_houses_greedy
from algorithms.greedy_random import place_houses_greedy_random
from algorithms.hill_climber_steps import hill_climber_steps
from algorithms.hill_climber_random import hill_climber_random
from algorithms.hill_climber_random_random import hill_climber_random_random
from algorithms.evolution import evolution
from algorithms.simulated_annealing import simulated_annealing

from user_input import user_input

def main():
    """ Main function """

    start = time()

    neighbourhood, houses, algorithm, hill_climber = user_input()

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
        place_houses_greedy(area)

    elif algorithm_name == "greedy_random":
        place_houses_greedy_random(area)

    elif algorithm_name == "evolution":
        evolution(area)


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

def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging.
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    return r


if __name__ == "__main__":
    main()
