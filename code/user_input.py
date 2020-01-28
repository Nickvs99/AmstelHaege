"""
user_input.py

Asks the user for input
"""


def user_input():

    print("Welcome to AmstelHaege")

    neighbourhood = get_neighbourhood()

    houses = get_houses()

    algorithm = get_algorithm()

    hill_climber = get_hill_climber()


def get_neighbourhood():
    
    neighbourhood_list = ["wijk1", "wijk2", "wijk3"]

    neighbourhood = input("Which neigbourhood would you like?\nChoose from: ")

def get_houses():


def get_algorithm():
    
    algorithm_list = ["random", "greedy", "greedy_random", "evolution"]


def get_hill_climber():

if __name__ == "__main__":
    user_input()