    def greedy(self, house, area):
        best_worth
        best_x = 0
        best_y = 0

        # Checks place for house
        for i in range(100):
            x = int(random.random() * (self.width - house.width + 1))
            y = int(random.random() * (self.height - house.height + 1))
            if area.check_valid(house, x, y):
                area.place_housegreedy(house, x, y)
                worth = area.calc_worth_area()

                    # Selects best place for house
                if worth > best_worth:
                    best_worth = worth
                    best_x = x
                    best_y = y

        # Places house in best place
        area.place_housegreedy(house, best_x, best_y)
