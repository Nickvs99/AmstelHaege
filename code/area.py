"""
    Responsible for making grid.


"""
import csv
import os.path
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class area():

    def __init__(self):

        self.height = 160
        self.width = 180

        # self.area = self.createArea()

        self.area = [[ 0 for i in range(self.width)] for j in range(self.height)]


    def createArea(self):

        area = [[ 0 for i in range(self.width)] for j in range(self.height)]
        return area

    def loadwater(self):
        
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../wijken/wijk2.csv")
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                bottom,left = row['bottom_left_xy'].split(",")
                top,right  = row['top_right_xy'].split(",")

                for i in range(int(bottom),int(top)):
                    for j in range(int(left),int(right)):
                        self.area[i][j] = 1


    def ShowArea(self):
        plt.imshow(self.area, cmap=plt.cm.Accent)
        plt.show()


    def place_houses(self, houses_count):
        """ Places the houses randomly. """

        # Calculate the number of houses per type
        one_person_house_count = int(0.6 * houses_count)
        bungalow_count = int(0.25 * houses_count)
        maison_count = int(0.15 * houses_count)

        self.houses = self.create_houses(one_person_house_count, bungalow_count, maison_count)

        for house in self.houses:
            self.place_house(house)

        # print(self.houses)
            
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

            x = int(random.random() * (self.width - house.width))
            y = int(random.random() * (self.height - house.height))
            
            
            if self.check_valid(house, x, y):
                house.x = x
                house.y = y
                house_placed = True
            
            while_count += 1

        for i in range(house.width):
            for j in range(house.height):

                self.area[house.y + j][house.x + i] = house.state

    def check_valid(self, house, x, y):
        
        for i in range(house.width):
            for j in range(house.height):
                if self.area[y + j][x + i] != 0:
                    return False

        return True

    def make_csv(self):

        values = self.retrieve_values(self.houses)
        print(values)

        self.csv_output(values)
    
    def retrieve_values(self, houses):

        one_person_count = 1
        bungalow_count = 1
        maison_count = 1
        house_list = []

        for house in self.houses:
            if house.type_house == 'one_person_home':
                structure = house.type_house + '_' + str(one_person_count)
                for i in house_list:
                    if structure in i:
                        one_person_count += 1
                        structure = house.type_house + '_' + str(one_person_count)
            if house.type_house == 'bungalow':
                structure = house.type_house + '_' + str(bungalow_count)
                for i in house_list:
                    if structure in i:
                        bungalow_count += 1
                        structure = house.type_house + '_' + str(bungalow_count)
            if house.type_house == 'maison':
                structure = house.type_house + '_' + str(maison_count)
                for i in house_list:
                    if structure in i:
                        maison_count += 1
                        structure = house.type_house + '_' + str(maison_count)

            bottom_left_xy = str(house.x) + ',' + str(house.y)
            top_right_x = house.x + house.width - 1
            top_right_y = house.y + house.height - 1
            top_right_xy = str(top_right_x) + ',' + str(top_right_y)
            type_house = house.type_house.upper()
            
            house_list.append([structure,bottom_left_xy,top_right_xy,type_house])

        return house_list

    def csv_output(self, house_list):

        # make csv-file

        pass



class House():

    def __init__(self, type_house):

        self.type_house = type_house
        self.x = 0
        self.y = 0

        if type_house == "bungalow":
            self.width = 11
            self.height = 7
            self.state = 3
        elif type_house == "maison":
            self.width = 12
            self.height = 10
            self.state = 4
        elif type_house == "one_person_home":
            self.width = 8
            self.height = 8
            self.state = 2
        else:
            print("Invalid type_house")
    
    def __str__(self):

        return f"{self.type_house}: {self.x}, {self.y}"

    def __repr__(self):

        return self.__str__()

