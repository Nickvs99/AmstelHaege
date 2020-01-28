"""
A settings file which will store settings specific
to an algorithms. For example the number of iterations for an algorithm.
"""

evolution_settings = dict(
    population = 5,             # Population size
    stale_counter = 1,          # How many iterations a population is allowed to not grow
    
    # Mutation rates without simulated annealing
    move_rate = 0.3,
    orientation_rate = 0.3,
    swap_rate = 0.1,

    # The maximum a house is allowed to move when its being mutated
    max_displacement = 5,

    # The exponent used in the fitness function. The higher the value
    # the more likely a good individual will be picked for mutations. This
    # is at the cost of population diversity.
    fitness_power = 3,

    # Set sa to True, if you want to add simulated annealing to the algorithm
    # NOTE: This is different than the simulated annealing algorithm. When set to
    # True, the mutation rates will slowly lower.
    sa = True,
)

greedy_random_settings = dict(
    iterations = 100,
)

hill_climber_random_random_settings = dict(
    iterations = 10000,
)

hill_climber_random_settings = dict(
    iterations = 100,
    iterations_house = 1000,
)

hill_climber_steps_settings = dict(
    iterations = 1000,
    max_displacement = 11,
)

simulated_annealing_settings = dict(
    iterations = 1000,
)