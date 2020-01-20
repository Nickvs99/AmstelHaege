"""
This python file iterates over a specific amount of randomly placed houses on the grid.
The seed of the grid with the highest calculated worth, will be shown and saved.
"""

import csv
import random
from time import time

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.ticker import PercentFormatter

from classes.area import Area
from main import algorithm, set_random_seed


ALGORITHM = "random"
NEIGHBOURHOOD = "wijk1"
HOUSES = 20
ITERATIONS = 100

def best_result():
    """ 
    Iterates over n amount of random grids and returns 
    the seed with the highest calucalted worth 
    """
    start = time()

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

    print(f"Best worth: {best_worth}")
    
    end = time()

    print(f"Runtime: {end - start}")

    # area.plot_area(int(best_worth))

    show_hist(area_worths)

    return area
    
def show_hist(area_worths): 

    num_bins = 50
    n, bins, patches = plt.hist(area_worths, num_bins, facecolor='blue', edgecolor='black', alpha=0.5)

    plt.ylabel('Amount found')
    plt.xlabel('Area worth')
    plt.title('All found area worths')

    plt.gca().yaxis.set_major_formatter(PercentFormatter(ITERATIONS))

    plt.show()
    

if __name__ == "__main__":
    best_result()
