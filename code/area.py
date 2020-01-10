"""
    Responsible for making grid.


"""
import csv
import os.path
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

class area():

    def __init__(self):

        self.height = 180
        self.width = 160

        self.structures = {"Water": [], "House":[]}

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

                bottom, left, top, right = int(bottom), int(left), int(top), int(right)

                water = Structure("Water")

                water.bottom_left_cor = [bottom, left]
                water.top_right_cor = [top, right]

                water.set_corners(water.bottom_left_cor, water.top_right_cor)

                self.structures["Water"].append(water)

    def fill_area(self):
        self.area = self.createArea()

        for water in self.structures["Water"]:
            # print(water.bottom_left_cor, water.top_right_cor)
            for y in range(water.bottom_left_cor[1], water.top_right_cor[1]):
                for x in range(water.bottom_left_cor[0], water.top_right_cor[0]):
                    self.area[y][x] = 1

        for house in self.structures["House"]:
            for y in range(house.bottom_left_cor[1], house.top_right_cor[1]):
                for x in range(house.bottom_left_cor[0], house.top_right_cor[0]):
                    try:
                        self.area[y][x] = house.state
                    except:
                        print(x, y)

    def ShowArea(self):

        self.fill_area()
        colorscheme = matplotlib.colors.ListedColormap(['#73b504', '#88AAFF', '#ee4035', '#ffb455', '#b266b2'])
        plt.imshow(self.area, cmap = colorscheme)
        plt.gca().invert_yaxis()
        plt.show()

    def place_housesgreedy(self, houses_count):
        """ Places the houses randomly. """

        # Calculate the number of houses per type
        one_person_house_count = int(0.6 * houses_count)
        bungalow_count = int(0.25 * houses_count)
        maison_count = int(0.15 * houses_count)
        houses = self.create_houses(one_person_house_count, bungalow_count, maison_count)
        counter = 0
        for house in houses:
            counter += 1
            print(counter)
            if counter >= 1:
                house.bottom_left_cor = [0, 0]
                house.top_right_cor = [0 + house.width, 0 + house.height]
                house.set_corners(house.bottom_left_cor, house.top_right_cor)
                self.structures["House"].append(house)
                greedyalgorithm = greedy()
                greedyalgorithm.greedy(house, self)
                print(self.calc_worth_area())
            else:
                house.bottom_left_cor = [74, 85]
                house.top_right_cor = [74 + house.width, 85 + house.height]

                house.set_corners(house.bottom_left_cor, house.top_right_cor)

                self.structures["House"].append(house)
        self.ShowArea()

    def place_housegreedy(self, house, x, y):
        """
        Place a house.
        It picks a random x and y coordinate and then checks if there is room for the new house.
        If it does not succeed, try new coordinates.
        """

        house.bottom_left_cor = [x, y]
        house.top_right_cor = [x + house.width, y + house.height]
        house.set_corners(house.bottom_left_cor, house.top_right_cor)


    def place_houses(self, houses_count):
        """ Places the houses randomly. """

        # Calculate the number of houses per type
        one_person_house_count = int(0.6 * houses_count)
        bungalow_count = int(0.25 * houses_count)
        maison_count = int(0.15 * houses_count)

        houses = self.create_houses(one_person_house_count, bungalow_count, maison_count)

        for house in houses:
            self.place_house(house)

    def create_houses(self, one_person_house_count, bungalow_count, maison_count):
        """ Creates a list with houses. """

        houses = []
        for i in range(maison_count):
            houses.append(House("maison"))

        for i in range(bungalow_count):
            houses.append(House("bungalow"))

        for i in range(one_person_house_count):
            houses.append(House("one_person_home"))

        return houses

    def place_house(self, house):
        """
        Place a house.
        It picks a random x and y coordinate and then checks if there is room for the new house.
        If it does not succeed, try new coordinates.
        """

        # TODO not sure if this works when large houses gets placed first and then the smaller

        house_placed = False
        while_count = 0
        while not house_placed and while_count < 1000:

            # Get random bottom_left x and y coordinate
            x = int(random.random() * (self.width - house.width))
            y = int(random.random() * (self.height - house.height))

            if self.check_valid(house, x, y):

                house.bottom_left_cor = [x, y]
                house.top_right_cor = [x + house.width, y + house.height]

                house.set_corners(house.bottom_left_cor, house.top_right_cor)

                self.structures["House"].append(house)

                house_placed = True

            while_count += 1

        if while_count == 1000:
            raise Exception("Something went wrong when placing a house")


    def check_valid(self, test_house, x, y):
        """ Returns True when there is enough room for a house. """

        test_bottom_left = [x, y]
        test_top_right = [x + test_house.width, y + test_house.height]
        test_top_left = [x, y + test_house.height]
        test_bottom_right = [x + test_house.width, y]

        # print("TESTHOUSE", test_bottom_left, test_top_right)
        if not self.check_in_bound(test_bottom_left, test_top_right):
            return False

        test_corners = [test_bottom_left, test_bottom_right, test_top_left, test_top_right]

        # Checks if any of the corners of the test_house are in a house
        for house in self.structures["House"]:
            if house == test_house:
                continue
            for test_corner in test_corners:
                corner_bottom_left = [house.corners[0][0] - house.mandatory_free_space, house.corners[0][1] - house.mandatory_free_space]
                corner_top_right = [house.corners[3][0] + house.mandatory_free_space, house.corners[3][1] + house.mandatory_free_space]
                if self.check_within_custom_bounds(test_corner[0], test_corner[1], corner_bottom_left, corner_top_right):
                    return False

        # Checks if any of the corners of the test_house are in water
        for water in self.structures["Water"]:

            for test_corner in test_corners:
                if self.check_within_custom_bounds(test_corner[0], test_corner[1], water.corners[0], water.corners[3]):
                    return False


        return True

    def check_within_custom_bounds(self, x, y, bottom_left_cor, top_right_cor):
        """ Returns True when a given x and y coordinate fall within a rectangle spanned
        from bottom_left_cor to top_right_cor. """

        if x > bottom_left_cor[0] and x < top_right_cor[0] and y > bottom_left_cor[1] and y < top_right_cor[1]:
            return True

        return False

    def calc_worth_area(self):
        """ Calculates the worth of the area. """

        total_worth = 0
        for  house in self.structures["House"]:
            total_worth += self.calc_worth_house(house)
        return total_worth

    def calc_worth_house(self, house):
        """ Calculates the worth of a house. """

        min_dist = math.inf
        for h in self.structures["House"]:
            if h == house:
                    continue
            for h_corner in h.corners:

                for house_corner in house.corners:

                    x_dist = abs(h_corner[0] - house_corner[0])
                    y_dist = abs(h_corner[1] - house_corner[1])
                    dist = max(x_dist, y_dist)

                    if dist < min_dist:
                        min_dist = dist

        base_value = house.value
        extra_value = house.value * house.extra_value * (min_dist - house.mandatory_free_space)
        value = base_value + extra_value
        return value

    def getBorder(self, bottom_left_cor, top_right_cor):
        """
        Returns all elements on the border from a rectangle spanned from
        the bottom_left_cor to the top_right_cor.
        """

        elements = []

        width = abs(top_right_cor[0] - bottom_left_cor[0]) +  1
        height = abs(top_right_cor[1] - bottom_left_cor[1]) + 1

        # Get the bottom border
        for i in range(width):

            x = bottom_left_cor[0] + i
            y = bottom_left_cor[1]
            self.appendElement(elements, x, y)

        # Get the top border
        for i in range(width):

            x = bottom_left_cor[0] + i
            y = top_right_cor[1]
            self.appendElement(elements, x, y)

        # Get the left border, excluding corners
        for i in range(1, height - 1):

            x = bottom_left_cor[0]
            y = bottom_left_cor[1] + i
            self.appendElement(elements, x, y)

        # Get the right border, excluding corners
        for i in range(1, height - 1):

            x = top_right_cor[0]
            y = bottom_left_cor[1] + i
            self.appendElement(elements, x, y)

        return elements

    def appendElement(self, elements, x, y):
        """ Appends an element to the listif it isn't out of bounds."""

        if not self.check_in_bound(x, y):
            return

        elements.append(self.area[y][x])

    def check_in_bound(self, bottom_left_cor, top_right_cor):
        """ Checks if a given x and y coordinates fall within the bounds. """

        if bottom_left_cor[0] < 0 or bottom_left_cor[1] < 0 or top_right_cor[0] >= self.width or top_right_cor[1] >= self.height:
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

class Structure():

    def __init__(self, structur_type):
        self.structur_type = structur_type
        self.bottom_left_cor = [None, None]
        self.top_right_cor = [None, None]
        self.structure_name = None

    def get_corners(self, bottom_left_cor, top_right_cor):

        bottom_right_cor = [top_left_cor[0], bottom_left_cor[1]]
        top_left_cor = [bottom_left_cor[0], top_right_cor[1]]

        return [bottom_left_cor, bottom_right_cor, top_left_cor, top_right_cor]

    def set_corners(self, bottom_left_cor, top_right_cor):
        """ Sets the bottom_right_cor and top_left_cor"""

        self.bottom_right_cor = [top_right_cor[0], bottom_left_cor[1]]
        self.top_left_cor = [bottom_left_cor[0], top_right_cor[1]]

        self.corners = [self.bottom_left_cor, self.bottom_right_cor, self.top_left_cor, self.top_right_cor]

    def __str__(self):

        return f"[{self.structure_name}, {self.bottom_left_cor}, {self.top_right_cor}, {self.structur_type}]"

    def __repr__(self):
        return self.__str__()

class House(Structure):

    def __init__(self, type_house):
        super().__init__("House")

        self.type_house = type_house
        self.x = 0
        self.y = 0

        # TODO presets or something, code doesnt look clean. Maybe three seperate object,
        # which inherit from this.
        if type_house == "bungalow":
            self.width = 11
            self.height = 7
            self.mandatory_free_space = 3
            self.state = 3
            self.value = 399000
            self.extra_value = 0.04
            self.horizontal = True

        elif type_house == "maison":
            self.width = 12
            self.height = 10
            self.state = 4
            self.mandatory_free_space = 6
            self.value = 610000
            self.extra_value = 0.06
            self.horizontal = True

        elif type_house == "one_person_home":
            self.width = 8
            self.height = 8
            self.state = 2
            self.mandatory_free_space = 2
            self.value = 285000
            self.extra_value = 0.03
            self.horizontal = True

        else:
            print("Invalid type_house")

    def __str__(self):

        return f"{self.type_house}: {self.bottom_left_cor}, {self.top_right_cor}"

    def __repr__(self):

        return self.__str__()

class greedy():

    def __init__(self):
        self.worth = 0

    def greedy(self, house, area):
        best_x = 0
        best_y = 0
        for y in range(area.height - house.height):
            for x in range(area.width - house.width):
                if area.check_valid(house, x, y):
                    area.place_housegreedy(house, x, y)
                    worth = area.calc_worth_area()
                    if worth > self.worth:
                        self.worth = worth
                        best_x = x
                        best_y = y
        area.place_housegreedy(house, best_x, best_y)
