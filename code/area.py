"""
    Responsible for making grid.


"""

import random

class area():

    def __init__(self):

        self.height = 160
        self.width = 180

        self.area = self.createArea()

    def createArea(self):

        row = [0] * self.width

        return [row] * self.height

    def place_houses(self, houses_count):
        """ Places the houses randomly. """

        # Calculate the number of houses per type
        one_person_house_count = int(0.6 * houses_count)
        bungalow_count = int(0.25 * houses_count)
        maison_count = int(0.15 * houses_count)

        houses = self.create_houses(one_person_house_count, bungalow_count, maison_count)

        for house in houses:
            self.place_house(house)

        print(houses)
            
    def create_houses(self, one_person_house_count, bungalow_count, maison_count):
        
        houses = []
        for i in range(one_person_house_count):
            houses.append(House("one_person_home"))

        for i in range(bungalow_count):
            houses.append(House("bungalow"))
        
        for i in range(maison_count):
            houses.append(House("maison"))

        return houses

    def place_house(self, house):

        house_placed = False
        while_count = 0
        while not house_placed and while_count < 1000:

            x = int(random.random() * self.width)
            y = int(random.random() * self.height)

            house.x = x
            house.y = y

            house_placed = True

            while_count += 1


class House():

    def __init__(self, type_house):

        self.type_house = type_house
        self.x = 0
        self.y = 0

        if type_house == "bungalow":
            self.width = 11
            self.height = 7
        elif type_house == "maison":
            self.width = 12
            self.height = 10
        elif type_house == "one_person_home":
            self.width = 8
            self.height = 8
        else:
            print("Invalid type_house")
    
    def __str__(self):

        return f"{self.type_house}: {self.x}, {self.y}"

    def __repr__(self):

        return self.__str__()

