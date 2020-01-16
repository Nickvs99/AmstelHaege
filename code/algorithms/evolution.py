"""
Evolution

Thanks wikipedia
Step One: Generate the initial population of individuals randomly. (First generation)

Step Two: Evaluate the fitness of each individual in that population (time limit, sufficient fitness achieved, etc.)

Step Three: Repeat the following regenerational steps until termination:

    Select the best-fit individuals for reproduction. (Parents)
    Breed new individuals through crossover and mutation operations to give birth to offspring.
    Evaluate the individual fitness of new individuals.
    Replace least-fit population with new individuals.

"""

import copy
import random

import matplotlib.pyplot as plt

from algorithms.greedy_random import place_housesgreedyrandom
from algorithms.random import random_placement
from classes.area import Area

MUTATE_RATE = 0.1
POPULATION = 50
EVOLVE_ITERATIONS = 100

class Individual(Area):
    """ An individual from the population. Stores an area object and the worth and fitness values."""

    def __init__(self, area):

        self.area = area
        self.calc_fitness()

    def calc_fitness(self):
        """
        Calculates fitness value. This value is used to determine the
        chance that this individual can reproduce.
        """

        self.worth = self.area.calc_worth_area()
        self.fitness = (self.worth / 1000000) ** 3

    def mutate(self):
        """ 
        Mutates the individual. Mutations are:
        - switch orientation
        - move coordinates
        """

        r = random.random()

        for house in self.area.structures["House"]:

            r = random.random()
            if r > 0.3:
                continue
            
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            while_count = 0
            while while_count < 1000:

                # Random coordinates shift
                diff_x = int(random.random() * 10 - 5)
                diff_y = int(random.random() * 10 - 5)

                x = initial_x + diff_x
                y = initial_y + diff_y

                house.set_coordinates([x, y], house.horizontal)

                if self.area.check_valid(house, x, y):

                    break

                while_count += 1
            self.area.update_distances(house)

        self.calc_fitness()
        

def evolution(area):
    """ The main program. """

    # Create an initial set of solutions with the random_greedy algorithm
    print("creating initial set of solutions...")
    individuals = []
    for i in range(POPULATION):
        copy_area = copy.deepcopy(area)
        random_placement(copy_area)
        individuals.append(Individual(copy_area))
    
    # Lists to keep track of the progress op the populations
    avg_worths, best_worths, total_best = [], [], []
    best_worth = 0
    best_individual = None

    print("Evolve")
    for i in range(EVOLVE_ITERATIONS):
        print("Generaton: ", i)

        individuals = evolve(individuals)

        # Append statistics to lists
        avg_worths.append(avg_individuals(individuals))

        new_best_individual = get_best_individual(individuals)
        new_best_worth = new_best_individual.worth
        if new_best_worth > best_worth:
            best_worth = new_best_worth
            best_individual = new_best_individual

        best_worths.append(new_best_worth)
        total_best.append(best_worth)

    # Plot the progress of the population
    plt.plot(avg_worths)
    plt.plot(best_worths)
    plt.plot(total_best)

    plt.show()

    best_individual.area.plot_area()

def evolve(individuals):
    """ Evolve the population one generation further."""    

    # Accumulate fitness
    total_fitness = 0
    for individual in individuals:
        total_fitness += individual.fitness

    # Normalize fitness
    norm_fitness = 0
    for individual in individuals:
        norm_fitness += individual.fitness / total_fitness
        individual.norm_fitness = norm_fitness

    # Accumulate norm fitness
    cum_fitness = 0
    for individual in individuals:
        cum_fitness += individual.norm_fitness
        individual.cum_fitness = cum_fitness

    new_generation = []
    # Fill the new generation
    for i in range(POPULATION):
        r = random.random()

        # Pick the random individual
        for individual in individuals:
            if individual.cum_fitness > r:
                
                new_generation.append(copy.deepcopy(individual))
                break

    # Mutate individuals
    for individual in new_generation:
        individual.mutate()
            

    return new_generation

def avg_individuals(individuals):
    """ Returns the average worth of all individuals."""

    total = 0
    for individual in individuals:
        total += individual.worth

    return total / len(individuals)

def get_best_individual(individuals):
    """ Returns the individual with the most worth. """

    best_worth = 0
    for individual in individuals:
        if individual.worth > best_worth:
            best_individual = individual
            best_worth = individual.worth

    return best_individual

