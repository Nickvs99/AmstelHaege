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

    def loadwater(self, filename):
        """ Reads the given csv-file and uses the coordinates to fill in the water """

        # Specify the path of the csv-file
        my_path = os.path.abspath(os.path.dirname(__file__))
        location = "../wijken/" + filename + ".csv"
        path = os.path.join(my_path, location)

        # Open the csv-file as a dictionary
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Retrieve the coordinates of the bottom-left and top-right of the water(s)
            for row in csv_reader:
                bottom,left = row['bottom_left_xy'].split(",")
                top,right  = row['top_right_xy'].split(",")

                # Replace each position in the nested list of area 
                # with 1, to indicate water
                for i in range(int(bottom),int(top)):
                    for j in range(int(left),int(right)):
                        self.area[i][j] = 1


    def ShowArea(self):
        colorscheme = matplotlib.colors.ListedColormap(['#73b504', '#88AAFF', '#ee4035', '#ffb455', '#b266b2'])
        plt.imshow(self.area, cmap = colorscheme)
        plt.gca().invert_yaxis()
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
            
    def create_houses(self, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with houses. """

        houses = []
        for i in range(one_person_house_count):
            houses.append(House("one_person_home"))

        for i in range(bungalow_count):
            houses.append(House("bungalow"))

        for i in range(maison_count):
            houses.append(House("maison"))

        return houses

    def place_house(self, house):
        """
        Place a house.
        It picks a random x and y coordinate and then checks if there is room for the new house.
        If it does not succeed, try new coordinates.
        """

        house_placed = False
        while_count = 0
        while not house_placed and while_count < 1000:

            # Get random x and y coordinate
            x = int(random.random() * (self.width - house.width))
            y = int(random.random() * (self.height - house.height))

            if self.check_valid(house, x, y):
                house.x = x
                house.y = y
                house_placed = True

            while_count += 1

        # Place the house in the area
        for i in range(house.width):
            for j in range(house.height):

                self.area[house.y + j][house.x + i] = house.state

    def check_valid(self, house, x, y):
        """ Returns True when there is enough room for a house. """

        # Check if the house overlaps with anything but land
        for i in range(house.width):
            for j in range(house.height):
                if self.area[y + j][x + i] != 0:
                    return False

        # Get the bottomleft coordinate of the mandatory free space
        xCor = x - house.mandatory_free_space
        yCor = y - house.mandatory_free_space

        # Check if the mandatory free space is actually free
        # TODO now the loop loops over a rectangle of spaces, but it only has to loop over the border
        # around the house
        for i in range(house.width + 2 * house.mandatory_free_space):
            for j in range(house.height + 2 * house.mandatory_free_space):

                x_temp = xCor + i
                y_temp = yCor + j

                # If the mandatory free space falls outside of the grid, continue
                if x_temp < 0 or y_temp < 0 or x_temp > self.width - 1 or y_temp > self.height - 1:
                    continue

                # Check if the mandatory free space overlaps with a building
                if self.area[y_temp][x_temp] in [2,3,4]:
                    return False

        return True

    def make_csv(self):
        """ Function which commands to update the output """

        house_list = self.make_house_list()
        print(house_list)

        self.csv_output(house_list)
    
    def make_house_list(self):
        """ Stores house-coordinates in a nested list """

        one_person_count = 1
        bungalow_count = 1
        maison_count = 1
        house_list = [['structure','bottom_left_xy','top_right_xy','type']]

        for house in self.houses:
            type_house = house.type_house
            if type_house == 'one_person_home':
                structure = type_house + '_' + str(one_person_count)
                one_person_count += 1
            elif type_house == 'bungalow':
                structure = type_house + '_' + str(bungalow_count)
                bungalow_count += 1
            elif type_house == 'maison':
                structure = type_house + '_' + str(maison_count)
                maison_count += 1

            bottom_left_xy = str(house.x) + ',' + str(house.y)
            top_right_x = house.x + house.width - 1
            top_right_y = house.y + house.height - 1
            top_right_xy = str(top_right_x) + ',' + str(top_right_y)
            type_house = house.type_house.upper()
            
            house_list.append([structure,bottom_left_xy,top_right_xy,type_house])

        return house_list

    def csv_output(self, house_list):
        """ (Over)writes the houselist into the ouput.csv """

        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../csv-output/output.csv")
        with open(path, 'w', newline='') as myfile:
            wr = csv.writer(myfile)
            for house in house_list:
                wr.writerow(house)


class House():

    def __init__(self, type_house):

        self.type_house = type_house
        self.x = 0
        self.y = 0

        if type_house == "bungalow":
            self.width = 11
            self.height = 7
            self.mandatory_free_space = 3
            self.state = 3

        elif type_house == "maison":
            self.width = 12
            self.height = 10
            self.state = 4
            self.mandatory_free_space = 6

        elif type_house == "one_person_home":
            self.width = 8
            self.height = 8
            self.state = 2
            self.mandatory_free_space = 2
        else:
            print("Invalid type_house")

    def __str__(self):

        return f"{self.type_house}: {self.x}, {self.y}"

    def __repr__(self):

        return self.__str__()
