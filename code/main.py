import csv
from area import area
import random

def main():

    set_random_seed()

    new_area = area()

    new_area.load_water('wijk2')

    new_area.place_houses(20)

    # print(new_area.structures)

    print(new_area.calc_worth_area())

    new_area.plot_area()
    
    new_area.make_csv()

    
 
def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging. 
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    print(f"Seed: {r}")
    

if __name__ == "__main__":
    main()