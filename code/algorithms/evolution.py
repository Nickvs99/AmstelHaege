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
from algorithms.greedy import place_housesgreedy
from classes.area import Area

POPULATION = 50
EVOLVE_ITERATIONS = 200
STALE_COUNTER = 1

MOVE_RATE = 0.3
ORIENTATION_RATE = 0.1
SWAP_RATE = 0.1

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

        # Move houses around
        for house in self.area.structures["House"]:
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            initial_orientation = house.horizontal

            # TODO seperate functions
            r = random.random()
            if r > MOVE_RATE:
                continue
            
            while_count = 0
            while while_count < 1000:

                # Random coordinates shift
                # TODO small changes should have a higher probability than larger changes
                diff_x = int(random.random() * 10 - 5)
                diff_y = int(random.random() * 10 - 5)

                x = initial_x + diff_x
                y = initial_y + diff_y

                house.set_coordinates([x, y], house.horizontal)

                if self.area.check_valid(house, x, y):

                    break

                while_count += 1
            else:
                house.set_coordinates([initial_x, initial_y], initial_orientation)
            
            self.area.update_distances(house)

        # Change orientation of houses
        for house in self.area.structures["House"]:
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            initial_orientation = house.horizontal

            r = random.random()
            if r > ORIENTATION_RATE:
                continue

            house.set_coordinates([initial_x, initial_y], random.choice([True, False]))

            if not self.area.check_valid(house, initial_x, initial_y):

                house.set_coordinates([initial_x, initial_y], initial_orientation)
            
            self.area.update_distances(house)

        # Swap houses
        for house in self.area.structures["House"]:
            initial_x = house.bottom_left_cor[0]
            initial_y = house.bottom_left_cor[1]
            initial_orientation = house.horizontal

            r = random.random()
            if r > ORIENTATION_RATE:
                continue

            house2 = random.choice(self.area.structures["House"])
            initial_x2 = house2.bottom_left_cor[0]
            initial_y2 = house2.bottom_left_cor[1]
            initial_orientation2 = house2.horizontal
            if house == house2:
                continue

            # Swap the two houses, if the swap is not valid, nothing happens.
            house.set_coordinates([initial_x2, initial_y2], initial_orientation2)
            house2.set_coordinates([initial_x, initial_y], initial_orientation)

            # TODO this line fucks things up
            if not (self.area.check_valid(house, initial_x2, initial_y2) and self.area.check_valid(house2, initial_x, initial_y)):

                # reset houses if not valid
                house.set_coordinates([initial_x, initial_y], initial_orientation)
                house2.set_coordinates([initial_x2, initial_y2], initial_orientation2)

            self.area.update_distances(house)
            self.area.update_distances(house2)

        self.calc_fitness()

    
def evolution(area):
    """ The main program. """

    # Create an initial set of solutions with the random_greedy algorithm
    print("Creating initial set of solutions...")
    individuals = []
    for i in range(POPULATION):
        copy_area = copy.deepcopy(area)
        random_placement(copy_area)
        individuals.append(Individual(copy_area))
    
    # When initial method is greedy
    # individuals = []
    # copy_area = copy.deepcopy(area)
    # place_housesgreedy(copy_area)
    # for i in range(POPULATION):
    #     individuals.append(Individual(copy.deepcopy(copy_area)))
    
    # Sort individuals
    individuals.sort(key=lambda x: x.worth, reverse=True)

    # Lists to keep track of the progress op the populations
    avg_worths, best_worths = [avg_individuals(individuals)], [get_best_individual(individuals).worth]
    best_worth = 0
    best_individual = None
    stale_counter = 0

    i = 0
    # while stale_counter < STALE_COUNTER:
    while i < 10:
        print("Generaton: ", i, best_worths[-1], avg_worths[-1])

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

    # # Plot the progress of population
    plt.plot(avg_worths)
    plt.plot(best_worths)   
    plt.show()


    # Copy all values to the original area. Now main can do all of its operations on the best area
    area.structures = get_best_individual(individuals).area.structures
    for h in area.structures["House"]:
        area.update_distances(h)

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

    # Fill the new generation
    mutations = []
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

