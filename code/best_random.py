"""
This python file iterates over a specific amount of randomly placed houses on the grid.
The seed of the grid with the highest calculated worth, will be shown and saved.
"""

import csv
import random
import operator
import timeit
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from classes.area import Area


def main():
    
    # Set runtime
    start = timeit.default_timer()
    
    # Find the seed with the highest worth and retrieve the grid
    # best_seed, Dict = best_random(1000)
    # set_random_seed(best_seed)
    new_area = Area('wijk2', 20)
    print(new_area.calc_worth_area())
    new_area.plot_area()
    new_area.make_csv_output()

    # End runtime and print the actual runtime
    stop = timeit.default_timer()
    print('Runtime: ', stop - start)

    # show_plot(Dict)

def best_random(n):
    """ 
    Iterates over n amount of random grids and returns 
    the seed with the highest calucalted worth 
    """

    Dict = {}

    # Iterate over n grids
    for i in range(n):
        
        # Set seed to retrieve the current grid
        seed = set_random_seed(random.random())

        # Make a random grid
        new_area = Area('wijk2', 20)

        # Add the seed with its worth in the dictionary
        Dict[seed] = int(new_area.calc_worth_area())

    # Retrieve the seed with highest calculated worth
    seed_most_worth = max(Dict, key=lambda key: Dict[key])

    return seed_most_worth, Dict

def show_plot(Dict):

    mylist = []

    for key in Dict:
        mylist.append(Dict[key])    
    
    num_bins = 10
    n, bins, patches = plt.hist(mylist, num_bins, facecolor='blue', alpha=0.5)

    plt.ylabel('Amount found')
    plt.xlabel('Area worth')
    plt.title('Title')

    plt.show()


def set_random_seed(r):
    """ Sets a random seed. This seed can be used with debugging. 
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    return r
    

if __name__ == "__main__":
    main()
