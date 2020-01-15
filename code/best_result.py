"""
This python file iterates over a specific amount of randomly placed houses on the grid.
The seed of the grid with the highest calculated worth, will be shown and saved.
"""

import csv
import random
import timeit
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from classes.area import Area
from algorithms.random import random_placement
from algorithms.greedy import place_housesgreedy


ALGORITHM = "random"
NEIGHBOURHOOD = "wijk2"
HOUSES = 20
ITERATIONS = 1000

def main():
    
    best_result()


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

    worth = area.calc_worth_area() 

    return worth

def best_result():
    """ 
    Iterates over n amount of random grids and returns 
    the seed with the highest calucalted worth 
    """
    start = timeit.default_timer()

    best_worth = 0
    best_seed = 0
    area_worths = []

    for i in range(ITERATIONS):
        
        seed = set_random_seed(random.random())

        area = Area(NEIGHBOURHOOD, HOUSES)
    
        algorithm(area, ALGORITHM)

        area_worth = area.calc_worth_area()

        area_worths.append(area_worth)

        if area_worth > best_worth:
            best_worth = area_worth
            best_seed = seed

    set_random_seed(best_seed)
    
    area = Area(NEIGHBOURHOOD, HOUSES)
    
    algorithm(area, ALGORITHM)

    print(f"Worth: {best_worth}")
    
    stop = timeit.default_timer()
    print('Runtime: ', stop - start)

    area.plot_area()

    show_plot(area_worths)

    return area
    
def show_plot(area_worths): 

    num_bins = 50
    n, bins, patches = plt.hist(area_worths, num_bins, facecolor='blue', edgecolor='black', alpha=0.5)

    plt.ylabel('Amount found')
    plt.xlabel('Area worth')
    plt.title('All found area worths')

    plt.gca().yaxis.set_major_formatter(PercentFormatter(ITERATIONS))

    plt.show()

def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging. 
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    return r
    

if __name__ == "__main__":
    main()
