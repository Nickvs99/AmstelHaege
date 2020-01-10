"""
This python file iterates over a specific amount of randomly placed houses on the grid.
The seed of the grid with the highest calculated worth, will be shown and saved.
"""

import csv
from area import area
import random
import operator
import sys
import timeit
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def main():
    
    # Set runtime
    start = timeit.default_timer()
    
    # Find the seed with the highest worth and retrieve the grid
    best_seed = best_random(10)
    set_random_seed(best_seed)
    new_area = area()
    new_area.loadwater('wijk2')
    new_area.place_houses(20)
    print(new_area.calc_worth_area())
    # new_area.ShowArea()
    # new_area.make_csv()

    # End runtime and print the actual runtime
    stop = timeit.default_timer()
    print('Runtime: ', stop - start)

    #showplot


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
        new_area = area()
        new_area.loadwater('wijk2')
        new_area.place_houses(20)

        # Add the seed with its worth in the dictionary
        Dict[seed] = int(new_area.calc_worth_area())

    # Retrieve the seed with highest calculated worth
    seed_most_worth = max(Dict, key=lambda key: Dict[key])

    # show_plot(Dict)

    return seed_most_worth

def show_plot(Dict):

    mylist = []

    for key in Dict:
        mylist.append(Dict[key])    
    
    num_bins = 10
    n, bins, patches = plt.hist(mylist, num_bins, normed=1, facecolor='blue', alpha=0.5)

    plt.ylabel('Amount found (in %)')
    plt.xlabel('Area worth (in milion)')
    plt.title('Title')

    plt.show()


def set_random_seed(r):
    """ Sets a random seed. This seed can be used with debugging. 
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    return r
    

if __name__ == "__main__":
    main()
