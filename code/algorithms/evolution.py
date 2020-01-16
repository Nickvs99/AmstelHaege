"""
Evolution

Thanks wikipedia
Step One: Generate the initial population of individuals randomly. (First generation)

Step Two: Evaluate the fitness of each individual in that population (time limit, sufficient fitness achieved, etc.)

Step Three: Repeat the following regenerational steps until termination:

    Select the best-fit individuals for reproduction. (Parents)
    Breed new individuals through crossover and mutation operations to give birth to offspring.
    Evaluate the individual fitness of new individuals.
    TODO Replace least-fit population with new individuals.

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
    
    # Sort individuals
    individuals.sort(key=lambda x: x.worth, reverse=True)

    # Lists to keep track of the progress op the populations
    avg_worths, best_worths = [avg_individuals(individuals)], [get_best_individual(individuals).worth]
    best_worth = 0
    best_individual = None
    stale_counter = 0

    print("Evolve")
    i = 0
    # while stale_counter < 5:
    while i < 100:
        print("Generaton: ", i, best_worths[-1])

        individuals = evolve(individuals)

        # Append statistics to lists
        avg_worth = avg_individuals(individuals)

        if avg_worth == avg_worths[-1]:
            stale_counter += 1
        else:
            stale_counter = 0

        avg_worths.append(avg_individuals(individuals))
        best_worths.append(get_best_individual(individuals).worth)

        i += 1

    print("Worth: ", best_worths[-1])

    # Plot the progress of the population
    plt.plot(avg_worths)
    plt.plot(best_worths)
    
    plt.show()

    # Set area to the best area. Then the main function can use it further
    area = get_best_individual(individuals).area

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

    mutations = []
    # Fill the new generation
    for i in range(POPULATION):
        r = random.random()

        # Pick the random individual
        for individual in individuals:
            if individual.cum_fitness > r:
                
                mutations.append(copy.deepcopy(individual))
                break

    # Mutate individuals
    for individual in mutations:
        individual.mutate()
    
    mutations.sort(key=lambda x: x.worth, reverse=True)

    # Get the n best from both generations
    old_generation_count = 0
    mutation_count = 0
    new_generation = []
    for i in range(POPULATION):
        if individuals[old_generation_count].worth > mutations[mutation_count].worth:
            new_generation.append(individuals[old_generation_count])
            old_generation_count += 1
        else:
            new_generation.append(mutations[mutation_count])
            mutation_count += 1

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

