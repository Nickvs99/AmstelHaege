"""
user_input.py

Asks the user for input for: the neighbourhood, amount of houses, algorithm 
and hill_climber. If a custom setting is possible, the user will be prompted 
to use the default settings or make their own custom settings. This file
stores and returns the stringvalues of the user-input.
"""

import settings

def user_input():
    """ Main program prompting user for input """

    print()
    print("|Welcome to AmstelHaege|")
    print()
    
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
    """ Returns value of neighbourhood """
    
    neighbourhood_list = ["wijk1", "wijk2", "wijk3"]

    neighbourhood = input(f"Choose from: {str(neighbourhood_list)[1:-1]}\n")
    print()

    # If the input for neighbourhood is invalid, prompt user again.
    if neighbourhood.lower() not in neighbourhood_list:
        
        print("Invalid neighbourhood")
        neighbourhood = get_neighbourhood()

    return neighbourhood.lower()

def get_houses():
    """ Returns amount of houses """

    houses = input()
    print()

    # if amount of houses is not a digit, prompt user again.
    if not houses.isdigit():
        
        print("Amount of houses must be a digit")
        houses = get_houses()

    return int(houses)

def get_algorithm():
    """ Returns which algorithm to apply """
    
    algorithm_list = ["random", "greedy", "greedy_random", "evolution"]

    algorithm = input(f"Choose from: {str(algorithm_list)[1:-1]}\n")
    print()

    if algorithm.lower() not in algorithm_list:
        
        print("Invalid algorithm")
        algorithm = get_algorithm()

    return algorithm.lower()

def get_hill_climber():
    """ Returns which hill climber to apply """

    hill_climber_list = ["hill_climber_steps", "hill_climber_random", 
                            "hill_climber_random_random", "simulated_annealing", "none"]

    hill_climber = input(f"Choose from: {str(hill_climber_list)[1:-1]}\n")
    print()

    if hill_climber.lower() not in hill_climber_list:

        print("Invalid hill_climber")
        hill_climber = get_hill_climber()

    elif hill_climber.lower() == "none":
        
        return None

    return hill_climber.lower()

def check_for_custom_settings(code_name):
    """ 
    Checks the code_name (algorithm or hill climber), 
    if it can have some custom settings. 
    """

    if code_name in CUSTOM_SETTINGS_LIST:
        
        print("Do you want the default settings or custom settings?")
        prompt_for_settings(code_name)

def prompt_for_settings(code_name):
    """ Prompts user for default or custom settings. """

    answer = input("1. Default\n2. Custom\n")
    print()

    try:
        answer = int(answer)
    
    except ValueError:
        print("Please type 1 or 2")
        prompt_for_settings(code_name)
    
    if answer == 1:
        pass
    
    elif answer == 2:
        custom_input(code_name)

    else:
        print("Please type 1 or 2")
        prompt_for_settings(code_name)

def custom_input(code_name):
    """ Prompts user for custom input """

    if code_name == "greedy_random":
        
        iterations = input(f"How many places on the area do you want to be checked for each house?\n \
        (Default value is {settings.greedy_random_settings['iterations']})\n")
        print()
        
        # Checks if the input is a digit
        check_digit_validity(iterations, code_name)  

        # Overwrites the input to the custom setting variable  
        settings.greedy_random_settings["iterations"] = int(iterations)

    elif code_name == "hill_climber_steps":
        
        iterations = input(f"How many times do you want to use a single hill climber, maximally?\n \
        (Default value is {settings.hill_climber_steps_settings['iterations']})\n")
        print()

        check_digit_validity(iterations, code_name)        
        settings.hill_climber_steps_settings["iterations"] = int(iterations)
        
        set_max_movement(code_name)

    elif code_name == "hill_climber_random":

        iterations = input(f"How many times do you want to move each house randomly?\n \
        (Default value is {settings.hill_climber_random_settings['iterations']})\n")
        print()
        
        check_digit_validity(iterations, code_name)        
        settings.hill_climber_random_settings["iterations"] = int(iterations)
        
    elif code_name == "hill_climber_random_random":

        iterations = input(f"How many times do you want to move each house randomly?\n \
        (Default value is {settings.hill_climber_random_random_settings['iterations']})\n")
        print()
        
        check_digit_validity(iterations, code_name)        
        settings.hill_climber_random_random_settings["iterations"] = int(iterations)

    elif code_name == "simulated_annealing":

        iterations = input(f"How many times do you want to move each house randomly?\n \
        (Default value is {settings.simulated_annealing_settings['iterations']})\n")
        print()
        
        check_digit_validity(iterations, code_name)        
        settings.simulated_annealing_settings["iterations"] = int(iterations)

    elif code_name == "evolution":
        custom_evolution()

def check_digit_validity(number, code_name):
    """ Checks if given number is a digit. """

    if not number.isdigit():
        custom_input(code_name)

def set_max_movement():
    """ 
    Sets the max_movement variable for the hill_climber_steps to the input-value, if valid. 
    """
        
    max_movement = input(f"In what range do you want to move each house-object?\n \
    (Default value is {settings.hill_climber_steps_settings['max_movement']})\n")
    print()
    
    check_digit_validity(max_movement, code_name)        
    settings.hill_climber_steps_settings["max_movement"] = int(max_movement)

def custom_evolution():
    """ Prompts the user for each evolution setting """

    variable_list = ["population", "stale_counter", "max_displacement", "fitness_power", 
                     "move_rate", "orientation_rate", "swap_rate", "sa"]

    for variable in variable_list:
        set_variable(variable)

def set_variable(variable):
    """ Sets each input-value in evolution_settings, if valid """

    variable_value = input(f"insert value for {variable}:\n \
    (Default value is {settings.evolution_settings[variable]})\n")
    print()
    
    if variable == "sa":
        
        if variable_value.lower() == "true":
            settings.evolution_settings['sa'] = True

        elif variable_value.lower() == "false":
            settings.evolution_settings['sa'] = False
        
        else:
            print("Please type true or false")
            set_variable(variable)

    # If input-value is for population and a float.
    if variable != "population":
        if "." in variable_value:
            if not variable_value.replace(".", "", 1).isdigit():
                print("Invalid input")
                set_variable(variable)
            else:
                settings.evolution_settings[variable] = float(variable_value)

    else:
        if not variable_value.isdigit():
            print("Invalid input")
            set_variable(variable)
        else:
            settings.evolution_settings[variable] = int(variable_value)


if __name__ == "__main__":
    user_input()