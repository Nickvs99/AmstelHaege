#from area import area

class greedy():

    def __init__(self):
        self.worth = 0

    def greedy(self, house):
        for x in range(area.width):
            for y in range(area.height):
                new_area = area
                if new_area.check_valid(house, x, y):
                    worth = new_area.calc_worth_area()
                    if worth > self. worth:
                        self.worth = worth
                        best_x = x
                        best_y = y
        area.place_house(house, best_x, best_y)
