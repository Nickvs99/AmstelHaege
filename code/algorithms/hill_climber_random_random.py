from classes.structure import House
import random

def hill_climber_random_random(area):

    # Iteration
    for i in range(10000):
        worth = area.calc_worth_area()

        # Picks random house and new coordinates
        j = int(random.random() * area.houses)
        house = area.structures["House"][j]
        old_x = house.bottom_left_cor[0]
        old_y = house.bottom_left_cor[1]
        x = int(random.random() * (area.width - house.width + 1))
        y = int(random.random() * (area.height - house.height + 1))

        # Checks if the move is valid and moves house
        if area.check_valid(house, x, y):
            move(area, house, x, y)
            new_worth = area.calc_worth_area()

            # Places house back if the move gets a lower score
            if worth > new_worth:
                move(area, house, old_x, old_y)

def move(area, house, x, y):
    """
    Moves a house.
    """

    house.bottom_left_cor = [x, y]
    house.top_right_cor = [x + house.width, y + house.height]
    house.set_corners()

    area.update_distances(house)
