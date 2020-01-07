"""

"""

from area import area
import random

def main():

    set_random_seed()

    new_area = area()

    new_area.place_houses(20)

    new_area.ShowArea()


    # new_areanp = np.array(new_area)

    # fig, ax = plt.subplots()
    # im = ax.imshow(new_areanp)

    # fig.tight_layout()
    # plt.show()
    #new_area.loadwater()

def set_random_seed(r = random.random()):
    """ Sets a random seed. This seed can be used with debugging. 
    Use the same seed to get the same results. By default it uses a random seed."""

    random.seed(r)

    print(f"Seed: {r}")

if __name__ == "__main__":
    main()

