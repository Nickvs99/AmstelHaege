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
from matplotlib.ticker import PercentFormatter

from classes.area import Area
from main import algorithm, set_random_seed


ALGORITHM = "random"
NEIGHBOURHOOD = "wijk1"
HOUSES = 20
ITERATIONS = 1000

def best_result():
    """
    Iterates over n amount of random grids and returns
    the seed with the highest calucalted worth
    """
    start = time()

    best_worth = 0
    best_seed = 0
    
    area_worths = []
    runtimes= []

    for i in range(ITERATIONS):

        start = time()

        seed = set_random_seed(random.random())

        area = Area(NEIGHBOURHOOD, HOUSES)

        algorithm(area, ALGORITHM)

        area_worth = area.calc_worth_area()

        end = time()

        runtimes.append(end - start)

        area_worths.append(area_worth)

        if area_worth > best_worth:
            best_worth = area_worth
            best_seed = seed

    set_random_seed(best_seed)

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    print(f"Best worth: {best_worth}")

    print(f"Avg worth: {calc_avg(area_worths)} +- {calc_std_dev(area_worths)}")

    print(f"Avg runtime: {calc_avg(runtimes)}")

    end = time()

    print(f"Runtime: {end - start}")

    # area.plot_area(int(best_worth))

    show_hist(area_worths)

    return area
    
def show_hist(area_worths): 

    # TODO fitting through histogram
    num_bins = 50
    n, bins, patches = plt.hist(area_worths, num_bins, facecolor='blue', edgecolor='black', alpha=0.5)

    plt.ylabel('Amount found')
    plt.xlabel('Area worth')
    plt.title('All found area worths')

    plt.gca().yaxis.set_major_formatter(PercentFormatter(ITERATIONS))

    plt.show()

def calc_std_dev(array):
    """Returns the standard deviation of a list of numbers."""

    avg = calc_avg(array)
    avg_squared = avg ** 2                           # <x>^2

    # Creates a list whose values are the squared versions of lijst
    list_squared = []
    for i in range(len(array)):
        list_squared.append(array[i] ** 2)

    avg_of_squared = calc_avg(list_squared)    # <x**2>

    return (avg_of_squared - avg_squared) ** 0.5

def calc_avg(array):
    """Returns the average of a list of numbers """

    total  = 0
    for i in array:
        total += i

    return total / len(array)

if __name__ == "__main__":
    best_result()
