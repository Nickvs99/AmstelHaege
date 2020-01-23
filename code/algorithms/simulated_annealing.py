from classes.structure import House
import random

def simulated_annealing(area):

    for j in range(1,1000):
        T = 1000 - j
        worth = area.calc_worth_area()
        while True:
            k = int(random.random() * area.houses)
            house = area.structures["House"][k]
            old_x = house.bottom_left_cor[0]
            old_y = house.bottom_left_cor[1]
            x = int(random.random() * (area.width - house.width + 1))
            y = int(random.random() * (area.height - house.height + 1))
            if area.check_valid(house, x, y):
                move(area, house, x, y)
                new_worth = area.calc_worth_area()
                if worth > new_worth:
                    chance = random.random() * 1000
                    if T < chance:
                        move(area, house, old_x, old_y)
                break

def move(area, house, x, y):
    """
    Moves a house.
    """

    house.bottom_left_cor = [x, y]
    house.top_right_cor = [x + house.width, y + house.height]
    house.set_corners()

    area.update_distances(house)
