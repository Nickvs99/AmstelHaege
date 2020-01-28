"""
A settings file which will store settings specific
to an algorithms. These are the default values.
"""

evolution_settings = dict(
    population = 50,             # Population size
    stale_counter = 15,          # How many iterations a population is allowed to not grow
    
    # Mutation rates without simulated annealing
    move_rate = 0.3,
    orientation_rate = 0.1,
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

hill_climber_steps_settings = dict(
    max_movement = 11,
)

iterations = dict(

    "greedy_random" = 100,

    "hill_climber_random" = 100,

    "hill_climber_random_random" = 10000,

    "hill_climber_steps" = 1000,
    
    "simulated_annealing" = 1000,

)