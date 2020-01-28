"""
Evolution

Generate the initial population of individuals with the greedy_random algorithm.

Evaluate the fitness of each individual in the population.

Repeat:

    Select the best-fit individuals for reproduction based on their fitness value.
    Breed new individuals through mutations to give birth to offspring.
    Evaluate the individual fitness of new individuals.
    Replace least-fit population with new individuals.
"""

import copy
import random
import math

import matplotlib.pyplot as plt

from algorithms.greedy_random import place_housesgreedyrandom
from classes.area import Area

from settings import evolution_settings as settings


class Individual():
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
        self.fitness = (self.worth / 1000000) ** settings["fitness_power"]

    def mutate(self):
        """ 
        Mutates the individual. Mutations are:
        - switch orientation of a house
        - move coordinates of a house
        - swap houses
        """

        self.move_houses()
        self.change_orientation()
        self.swap_houses()

        self.calc_fitness()

    def move_houses(self):
        """ 
        Mutates the position of the houses. 
        Each house has a MOVE_RATE % chance to move a number of coordinates. 
        """

        for house in self.area.structures["House"]:
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            initial_orientation = house.horizontal

            r = random.random()
            if r > settings["move_rate"]:
                continue

            while_count = 0
            valid = False
            while not valid:
                
                max_displacement = 5
                # Random coordinates shift

                diff_x = int(random.random() * settings["max_displacement"] - settings["max_displacement"])
                diff_y = int(random.random() * settings["max_displacement"] - settings["max_displacement"])

                x = initial_x + diff_x
                y = initial_y + diff_y

                house.set_coordinates([x, y], house.horizontal)

                if self.area.check_valid(house, x, y):
                    valid = True

                # Set house to its initial state, if no valid place has been found
                if while_count == 1000:
                    house.set_coordinates([initial_x, initial_y], initial_orientation)
                    break

                while_count += 1
                
            self.area.update_distances(house)

    def change_orientation(self):
        """
        Mutates the orientation of the houses.
        Each house has a ORIENTATION_RATE % change to switch orientation.
        """

        for house in self.area.structures["House"]:
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            initial_orientation = house.horizontal

            r = random.random()
            if r > settings["orientation_rate"]:
                continue

            house.set_coordinates([initial_x, initial_y], not initial_orientation)

            # Revert back if the new orientation is not allowed
            if not self.area.check_valid(house, initial_x, initial_y):

                house.set_coordinates([initial_x, initial_y], initial_orientation)
            
            self.area.update_distances(house)

    def swap_houses(self):
        """
        Swaps houses.
        Each house has a SWAP_RATE % chance to swap with a random house.
        """

        for house in self.area.structures["House"]:

            r = random.random()
            if r > settings["swap_rate"]:
                continue

            # Pick a randomly chosen house
            house2 = random.choice(self.area.structures["House"])
            if house == house2:
                continue

            # Get initial values for both houses
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            initial_orientation = house.horizontal

            initial_x2 = house2.bottom_left_cor[0]
            initial_y2 = house2.bottom_left_cor[1]
            initial_orientation2 = house2.horizontal

            # Swap the two houses
            house.set_coordinates([initial_x2, initial_y2], initial_orientation2)
            house2.set_coordinates([initial_x, initial_y], initial_orientation)
            
            # If the swap is not valid, reset all values
            if not (self.area.check_valid(house, initial_x2, initial_y2) and self.area.check_valid(house2, initial_x, initial_y)):

                house.set_coordinates([initial_x, initial_y], initial_orientation)
                house2.set_coordinates([initial_x2, initial_y2], initial_orientation2)

            self.area.update_distances(house)
            self.area.update_distances(house2)
   
def evolution(area):
    """ The main program. """

    # Create an initial set of solutions with the random_greedy algorithm
    print("Creating initial set of solutions...")
    individuals = []
    for i in range(settings["population"]):
        copy_area = copy.deepcopy(area)
        place_housesgreedyrandom(copy_area)
        individuals.append(Individual(copy_area))
    
    # Sort individuals by their worth
    individuals.sort(key=lambda x: x.worth, reverse=True)

    # Lists to keep track of the progress op the population
    best_individual = get_best_individual(individuals)
    avg_worths = [calc_avg_individuals(individuals)]
    best_worths = [best_individual.worth]
    
    stale_counter = 0
    generation_count = 0
    
    while stale_counter < settings["stale_counter"]:
        print("Generaton: ", generation_count, best_worths[-1], avg_worths[-1], settings["move_rate"])

        individuals = evolve(individuals)

        avg_worth = calc_avg_individuals(individuals)

        if avg_worth == avg_worths[-1]:
            stale_counter += 1
        else:
            stale_counter = 0

        # Append statistics to lists
        avg_worths.append(calc_avg_individuals(individuals))
        best_worths.append(get_best_individual(individuals).worth)

        generation_count += 1

        if settings["sa"]:
            update_mutate_rates(generation_count)

    # # Plot the progress of population
    plt.plot(avg_worths)
    plt.plot(best_worths)  
    plt.title("Progress of population")
    plt.xlabel("Generations") 
    plt.ylabel("Worth")
    plt.show()

    # Copy all values to the original area. Now main can do all of its operations on the best area
    area.structures = get_best_individual(individuals).area.structures
    for h in area.structures["House"]:
        area.update_distances(h)

def evolve(individuals):
    """ Evolve the population one generation further."""    

    # Cumulate fitness
    total_fitness = 0
    for individual in individuals:
        total_fitness += individual.fitness

    # Normalize fitness
    norm_fitness = 0
    for individual in individuals:
        norm_fitness += individual.fitness / total_fitness
        individual.norm_fitness = norm_fitness

    # Cumulate norm fitness
    cum_fitness = 0
    for individual in individuals:
        cum_fitness += individual.norm_fitness
        individual.cum_fitness = cum_fitness

    # Fill the new generation with the best individuals from the
    # old generation and the mutated versions.
    mutations = []
    for i in range(settings["population"]):
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
    for i in range(settings["population"]):
        if individuals[old_generation_count].worth > mutations[mutation_count].worth:
            new_generation.append(individuals[old_generation_count])
            old_generation_count += 1
        else:
            new_generation.append(mutations[mutation_count])
            mutation_count += 1

    return new_generation

def calc_avg_individuals(individuals):
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

def update_mutate_rates(generation_count):
    """ Updates the mutation rates, when simulated annealing is enabled. """


    MOVE_RATE = cool_function(generation_count)
    ORIENTATION_RATE = cool_function(generation_count)
    SWAP_RATE = cool_function(generation_count)

def cool_function(generation_count):

    return 2 / generation_count + 0.04
