"""
user_input.py

Asks the user for input
"""

import settings

def user_input():

    print("Welcome to AmstelHaege")
    
    print("Which neighbourhood would you like?")
    neighbourhood = get_neighbourhood()

    print("How many houses would you like to place?")
    houses = get_houses()

    print("Which algorithm would you like to use?")
    algorithm = get_algorithm()

    check_for_custom_settings(algorithm)

    print("Which hill climber would you like to use?")
    hill_climber = get_hill_climber()

    check_for_custom_settings(hill_climber)

    return neighbourhood, houses, algorithm, hill_climber


def get_neighbourhood():
    
    neighbourhood_list = ["wijk1", "wijk2", "wijk3"]

    neighbourhood = input(f"Choose from: {str(neighbourhood_list)[1:-1]}\n")

    if neighbourhood.lower() not in neighbourhood_list:
        
        print("Invalid neighbourhood")
        
        neighbourhood = get_neighbourhood()

    return neighbourhood.lower()

def get_houses():

    houses = input()

    if not houses.isdigit():
        
        print("Amount of houses must be a digit")

        houses = get_houses()

    return int(houses)

def get_algorithm():
    
    algorithm_list = ["random", "greedy", "greedy_random", "evolution"]

    algorithm = input(f"Choose from: {str(algorithm_list)[1:-1]}\n")

    if algorithm.lower() not in algorithm_list:

        print("Invalid algorithm")

        algorithm = get_algorithm()

    return algorithm.lower()

def check_for_custom_settings(code_name):

    custom_settings_list = ["greedy_random", "hill_climber_steps", "hill_climber_random", "hill_climber_random_random"]

    if code_name in custom_settings_list:
        print("Do you want the default settings or custom settings?")
        ask_for_settings(code_name)

def ask_for_settings(code_name):

    answer = int(input("1. Default\n2. Custom\n"))

    if answer == 1:
        pass
    
    elif answer == 2:
        iteration_input(code_name)

    else:
        print("Please choose 1 or 2")
        answer = ask_for_settings(code_name)

def iteration_input(code_name):

    if code_name == "greedy_random":
        
        iterations = input(f"How many places on the area do you want to be checked for each house?\n \
                            (Default value is {settings.greedy_random_settings['iterations']})\n")
        
        if not iterations.isdigit():
            
            iterations = iteration_input(code_name)
        
        settings.greedy_random_settings["iterations"] = int(iterations)

    elif code_name == "hill_climber_steps":
        
        iterations = input(f"How many times do you want to use a single hill climber, maximally?\n \
                            (Default value is {settings.hill_climber_steps_settings['iterations']})\n")

        if not iterations.isdigit():
            
            iterations = iteration_input(code_name)
        
        settings.greedy_random_settings["iterations"] = int(iterations)
        
        max_displacement = get_max_displacement(code_name)

    elif code_name == "hill_climber_random":

        iterations = input(f"How many times do you want to move each house randomly?\n \
                            (Default value is {settings.hill_climber_random_settings['iterations']})\n")
        
        if not iterations.isdigit():
            
            iterations = iteration_input(code_name)
        
        settings.greedy_random_settings["iterations"] = int(iterations)
        
    elif code_name == "hill_climber_random_random":

        iterations = input(f"How many times do you want to move each house randomly?\n \
                            (Default value is {settings.hill_climber_random_random_settings['iterations']})\n")
        
        if not iterations.isdigit():
            
            iterations = iteration_input(code_name)
        
        settings.greedy_random_settings["iterations"] = int(iterations)

def get_max_displacement(code_name):

    if code_name == "hill_climber_steps":
        
        max_displacement = input(f"In what range do you want to displace each house-object?\n \
                            (Default value is {settings.hill_climber_steps_settings['max_displacement']})\n")
        
        if not max_displacement.isdigit():
            
            max_displacement = get_max_displacement(code_name)
        
        settings.hill_climber_steps_settings["max_displacement"] = int(max_displacement)

def get_hill_climber():

    hill_climber_list = ["hill_climber_steps", "hill_climber_random", 
                            "hill_climber_random_random", "simulated_annealing", "none"]

    hill_climber = input(f"Choose from: {str(hill_climber_list)[1:-1]}\n")

    if hill_climber.lower() not in hill_climber_list:

        print("Invalid hill_climber")

        hill_climber = get_hill_climber()

    elif hill_climber.lower() == "none":

        return None

    return hill_climber.lower()


if __name__ == "__main__":
    user_input()