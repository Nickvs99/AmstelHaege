"""
This python file iterates over a specific amount of randomly placed houses on the grid.
The average area worth with standard deviation and average runtime will be s
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
from main import algorithm, hill_climber, set_random_seed
from algorithms.hill_climber_steps import hill_climber_steps


HOUSES = 60
ITERATIONS = 1000
NEIGHBOURHOOD = "wijk1"
ALGORITHM = "random"
# HILL_CLIMBER = "hill_climber_random_random"
HILL_CLIMBER = None

def best_result():
    """
    Iterates over n amount of random grids and returns
    the area with the highest calucalted worth
    """

    best_worth = 0
    best_seed = 0
    
    area_worths = []
    runtimes= []

    # Iterate the algorithm by the given amount of times
    for i in range(ITERATIONS):

        start = time()

        seed = set_random_seed(random.random())

        area = Area(NEIGHBOURHOOD, HOUSES)

        algorithm(area, ALGORITHM)
        
        if HILL_CLIMBER:

            hill_climber(area, HILL_CLIMBER)

            hill_climber_steps(area)

        area_worth = area.calc_worth_area()
        
        # Store the highest area_worth with its corresponding seed
        if area_worth > best_worth:

            best_worth = area_worth

            best_seed = seed
        
        end = time()

        runtimes.append(end - start)

        area_worths.append(area_worth)

    # Calculate average area_worth and its standard deviation
    avg_worth = calc_avg(area_worths)

    std_dev_worth = calc_std_dev(area_worths)

    print(f"Avg worth: {avg_worth} +- {std_dev_worth}")

    print(f"Avg runtime: {calc_avg(runtimes)}")

    # Retrieve area with the highest area_worth
    set_random_seed(best_seed)

    area = Area(NEIGHBOURHOOD, HOUSES)

    algorithm(area, ALGORITHM)

    area.make_csv_output()

    area.plot_area(NEIGHBOURHOOD, HOUSES, ALGORITHM)

    show_hist(area_worths, avg_worth, std_dev_worth)

    
def show_hist(area_worths, avg_worth, std_dev): 
    """
    Returns a histogram with all the saved area_worths and a box with 
    """

    num_bins = 50

    fig, ax = plt.subplots()

    n, bins, patches = plt.hist(area_worths, num_bins, facecolor='blue', edgecolor='black', alpha=0.5)

    plt.ylabel('Amount found')
    plt.xlabel('Area worth')
    plt.title('All found area worths')

    power = 6
    avg_worth /= 10 ** power
    std_dev /= 10 ** power

    # Box with avg and stddev values
    textstr = '$avg = %.2f * 10 ^ %d$\n$stddev= %.2f * 10 ^ %d$' %(avg_worth, power, std_dev, power)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        va='top', ha='right', bbox = props)

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
