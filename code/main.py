"""

"""

import csv
from area import area
import random

def main():

    seed = set_random_seed()

    a = []

    for i in range(2):

        new_area = area()

        new_area.loadwater('wijk2')

        new_area.place_houses(20)

        # a.append(new_area.calc_worth_area)
        b = new_area.calc_worth_area

    # end loop, pick the greatest value, keep the seed of this format

    print(f"list = {b}")

    print(f"seed = {seed}")

    new_area.ShowArea()
    
    new_area.make_csv()

    
 
def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging. 
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    # print(f"Seed: {r}")

    return r
    

if __name__ == "__main__":
    main()
