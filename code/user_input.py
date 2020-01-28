"""
user_input.py

Asks the user for input for: the neighbourhood, amount of houses, algorithm and hill_
"""

import settings

def user_input():

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
    
    neighbourhoodvariable_list = ["wijk1", "wijk2", "wijk3"]

    neighbourhood = input(f"Choose from: {str(neighbourhoodvariable_list)[1:-1]}\n")
    print()

    if neighbourhood.lower() not in neighbourhoodvariable_list:
        
        print("Invalid neighbourhood")
        neighbourhood = get_neighbourhood()

    return neighbourhood.lower()

def get_houses():

    houses = input()
    print()

    if not houses.isdigit():
        
        print("Amount of houses must be a digit")
        houses = get_houses()

    return int(houses)

def get_algorithm():
    
    algorithmvariable_list = ["random", "greedy", "greedy_random", "evolution"]

    algorithm = input(f"Choose from: {str(algorithmvariable_list)[1:-1]}\n")
    print()

    if algorithm.lower() not in algorithmvariable_list:
        
        print("Invalid algorithm")
        algorithm = get_algorithm()

    return algorithm.lower()

def get_hill_climber():

    hill_climbervariable_list = ["hill_climber_steps", "hill_climber_random", 
                            "hill_climber_random_random", "simulated_annealing", "none"]

    hill_climber = input(f"Choose from: {str(hill_climbervariable_list)[1:-1]}\n")
    print()

    if hill_climber.lower() not in hill_climbervariable_list:

        print("Invalid hill_climber")
        hill_climber = get_hill_climber()

    elif hill_climber.lower() == "none":

        return None

    return hill_climber.lower()

def check_for_custom_settings(code_name):

    custom_settingsvariable_list = ["greedy_random", "evolution", "hill_climber_steps", "hill_climber_random", "hill_climber_random_random", "simulated_annealing"]

    if code_name in custom_settingsvariable_list:
        
        print("Do you want the default settings or custom settings?")
        ask_for_settings(code_name)

def ask_for_settings(code_name):

    answer = int(input("1. Default\n2. Custom\n"))
    print()

    if answer == 1:
        pass
    
    elif answer == 2:
        custom_input(code_name)

    else:
        print("Please choose 1 or 2")
        answer = ask_for_settings(code_name)

def custom_input(code_name):

    if code_name == "greedy_random":
        
        iterations = input(f"How many places on the area do you want to be checked for each house?\n \
                            (Default value is {settings.greedy_random_settings['iterations']})\n")
        print()
        
        if not iterations.isdigit():
            
            iterations = custom_input(code_name)
        
        settings.greedy_random_settings["iterations"] = int(iterations)

    elif code_name == "hill_climber_steps":
        
        iterations = input(f"How many times do you want to use a single hill climber, maximally?\n \
                            (Default value is {settings.hill_climber_steps_settings['iterations']})\n")
        print()

        if not iterations.isdigit():
            
            iterations = custom_input(code_name)
        
        settings.hill_climber_steps_settings["iterations"] = int(iterations)
        
        max_displacement = get_max_displacement(code_name)

    elif code_name == "hill_climber_random":

        iterations = input(f"How many times do you want to move each house randomly?\n \
                            (Default value is {settings.hill_climber_random_settings['iterations']})\n")
        print()
        
        if not iterations.isdigit():
            
            iterations = custom_input(code_name)
        
        settings.hill_climber_random_settings["iterations"] = int(iterations)
        
    elif code_name == "hill_climber_random_random":

        iterations = input(f"How many times do you want to move each house randomly?\n \
                            (Default value is {settings.hill_climber_random_random_settings['iterations']})\n")
        print()
        
        if not iterations.isdigit():
            
            iterations = custom_input(code_name)
        
        settings.hill_climber_random_random_settings["iterations"] = int(iterations)

    elif code_name == "simulated_annealing":

        iterations = input(f"How many times do you want to move each house randomly?\n \
                            (Default value is {settings.simulated_annealing_settings['iterations']})\n")
        print()
        
        if not iterations.isdigit():
            
            iterations = custom_input(code_name)
        
        settings.simulated_annealing_settings["iterations"] = int(iterations)

    elif code_name == "evolution":

        custom_evolution()

def get_max_displacement(code_name):

    if code_name == "hill_climber_steps":
        
        max_displacement = input(f"In what range do you want to displace each house-object?\n \
                            (Default value is {settings.hill_climber_steps_settings['max_displacement']})\n")
        print()
        
        if not max_displacement.isdigit():
            
            max_displacement = get_max_displacement(code_name)
        
        settings.hill_climber_steps_settings["max_displacement"] = int(max_displacement)

def custom_evolution():

    variable_list = ["population", "stale_counter", "max_displacement", "fitness_power", "move_rate", "orientation_rate", "swap_rate", "sa"]

    for variable in variable_list:

        if variable == "sa":
            set_variable_sa(variable)

        else:
            set_variable(variable)
        

def set_variable(variable):

    variable_value = input(f"insert value for {variable}:\n(Default value is {settings.evolution_settings[variable]})\n")
    print()

    if "." in variable_value:
        if variable != "population":
            store_variable = variable_value
            if not variable_value.replace(".", "", 1).isdigit():
                set_variable(variable)
            else:
                settings.evolution_settings[variable] = float(variable_value)
        else:
            print("This variable needs to be a integer")
            set_variable(variable)

    else:
        if not variable_value.isdigit():
            set_variable(variable)

        settings.evolution_settings[variable] = int(variable_value)

def set_variable_sa(variable):

    variable_value = input(f"This form of simulated annealing slowes down the mutation rate if turned True\ninsert value for {variable}:\n(Default value is {settings.evolution_settings[variable]})\n")
    print()

    if variable_value.lower() not in ["true", "false"]:
        set_variable_sa(variable)

    variable_value = variable_value.replace('"','').capitalize()
    settings.evolution_settings[variable] = variable_value

if __name__ == "__main__":
    user_input()
    # custom_evolution()