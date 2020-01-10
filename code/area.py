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

        # Stores all structures in their respective type
        self.structures = {"Water": [], "House":[]}

    def create_area(self):
        """ 
        Creates an listed list with self.height x self.width dimensions. 
        This list is filled with zeroes.
        """

        return [[ 0 for i in range(self.width)] for j in range(self.height)]

    def load_water(self, filename):
        """ Gets the water from the csv file and creates objects from them. """

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

                bottom, left, top, right = int(bottom), int(left), int(top), int(right)

                # Create the water object
                water = Structure("Water")

                water.bottom_left_cor = [bottom, left]
                water.top_right_cor = [top, right]
                water.set_corners()

                self.structures["Water"].append(water)

    def fill_area(self, area):
        """ Fill the area with the objects with the state of the structures"""

        for water in self.structures["Water"]:

            for y in range(water.bottom_left_cor[1], water.top_right_cor[1]):
                for x in range(water.bottom_left_cor[0], water.top_right_cor[0]):
                    area[y][x] = 1

        for house in self.structures["House"]:

            for y in range(house.bottom_left_cor[1], house.top_right_cor[1]):
                for x in range(house.bottom_left_cor[0], house.top_right_cor[0]):
                    try:
                        area[y][x] = house.state
                    except: 
                        print(x, y)

    def plot_area(self):
        """
        Plots the area.
        """
        
        area = self.create_area()
        self.fill_area(area)

        colorscheme = matplotlib.colors.ListedColormap(['#73b504', '#88AAFF', '#ee4035', '#ffb455', '#b266b2'])
        plt.imshow(area, cmap = colorscheme)
        plt.gca().invert_yaxis()
        plt.show()

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
            r = random.choice([True, False])
            houses.append(House("maison", r))

        for i in range(bungalow_count):
            r = random.choice([True, False])
            houses.append(House("bungalow", r))

        for i in range(one_person_house_count):
            houses.append(House("one_person_home", r))

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

            # Get random bottom_left x and y coordinate
            x = int(random.random() * (self.width - house.width))
            y = int(random.random() * (self.height - house.height))

            if self.check_valid(house, x, y):
                
                house.bottom_left_cor = [x, y]
                house.top_right_cor = [x + house.width, y + house.height]
                house.set_corners()

                self.structures["House"].append(house)

                house_placed = True

            while_count += 1

        if while_count == 1000:
            raise Exception("Something went wrong when placing a house. There was probably to little room to fit an extra house.") 

    def check_valid(self, test_house, x, y):
        """ 
        Returns True when satisfies the constrains.
        These constrains are:
            - The house must be fully placed on the grid.
            - The house is not allowed to overlap other houses.
            - The house has a mandatory free space. 
         """
        test_bottom_left = [x, y]
        test_top_right = [x + test_house.width, y + test_house.height]
        test_top_left = [x, y + test_house.height]
        test_bottom_right = [x + test_house.width, y]

        # Both the bottom_left coordinate as the top_right coordinate have to be in bounds
        if not self.check_in_bound(test_bottom_left, test_top_right):
            return False

        test_corners = [test_bottom_left, test_bottom_right, test_top_left, test_top_right]

        # Checks if any of the corners of the test_house are in a house or their mandatory free space
        for house in self.structures["House"]:
            if house == test_house:
                continue

            for test_corner in test_corners:
                
                # Get the corners of the non allowed space. This includes the mandatory space.
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
        """ 
        Returns True when a given x and y coordinate fall within a rectangle spanned
        from bottom_left_cor to top_right_cor. Border is excluded.
        """

        if x > bottom_left_cor[0] and x < top_right_cor[0] and y > bottom_left_cor[1] and y < top_right_cor[1]:
            return True

        return False

    def calc_worth_area(self):
        """ Calculates the worth of the area. """
        
        total_worth = 0
        for  house in self.structures["House"]:
            total_worth += self.calc_worth_house(house)

        return f"{int(total_worth)}"

    def calc_worth_house(self, house):
        """ 
        Calculates the worth of a house. The worth is
        worth = base_value + base_value * extra_value * (min_dist - mandatory_free_space)
        """

        # Get the minimum distance from one corner of the house to another corner of any house.
        min_dist = math.inf
        for h in self.structures["House"]:

            # Dont check distances if the house is the same as h
            if h == house:
                    continue
            
            for h_corner in h.corners:
                
                for house_corner in house.corners:
                    
                    x_dist = abs(h_corner[0] - house_corner[0])
                    y_dist = abs(h_corner[1] - house_corner[1])

                    # Use the maximum value, since the minimum value wouldnt reach the object
                    dist = max(x_dist, y_dist)

                    if dist < min_dist:
                        min_dist = dist

        base_value = house.value
        extra_value = house.value * house.extra_value * (min_dist - house.mandatory_free_space)

        value = base_value + extra_value

        return value

    def check_in_bound(self, bottom_left_cor, top_right_cor):
        """ Checks if a given x and y coordinates fall within the bounds. """

        if bottom_left_cor[0] < 0 or bottom_left_cor[1] < 0 or top_right_cor[0] >= self.width or top_right_cor[1] >= self.height:
            return False
        
        return True

    def make_csv(self):
        """ Function which commands to update the output """

        # Store values house_list
        house_list = self.make_house_list()

        # Use house_list to make the csv-output
        self.csv_output(house_list)
    
    def make_house_list(self):
        """ Stores house-coordinates in a nested list """

        # Startvalue housenumber
        one_person_count = 1
        bungalow_count = 1
        maison_count = 1

        house_list = [['structure','bottom_left_xy','top_right_xy','type']]

        for house in self.structures["House"]:
            # print(f"{house.type_house} - {house.bottom_left_cor} - {house.top_right_cor}")

            # Make structure of each house and update housenumber
            if house.type_house == 'one_person_home':
                structure = house.type_house + '_' + str(one_person_count)
                one_person_count += 1
            elif house.type_house == 'bungalow':
                structure = house.type_house + '_' + str(bungalow_count)
                bungalow_count += 1
            elif house.type_house == 'maison':
                structure = house.type_house + '_' + str(maison_count)
                maison_count += 1

            # Make string representation of the coordinates
            bottom_left_xy = str(house.bottom_left_cor[0]) + ',' + str(house.bottom_left_cor[1])
            top_right_xy = str(house.top_right_cor[0]) + ',' + str(house.top_right_cor[1])
            type_house = house.type_house.upper()
            
            # Append values to the house_list
            house_list.append([structure,bottom_left_xy,top_right_xy,type_house])

        return house_list

    def csv_output(self, house_list):
        """ (Over)writes the houselist into the ouput.csv """

        # Specify the path of the csv-file
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../csv-output/output.csv")

        # Open the current output.csv
        with open(path, 'w', newline='') as myfile:
            wr = csv.writer(myfile)

            # (Over)write each line of house_list into the csv-file
            for house in house_list:
                wr.writerow(house)

class Structure():
    """
    Structure object. This object stores:
    - bottom_left_cor
    - top_right_cor
    - the type ('Water', 'House' etc.)
    - the name, a unique id ('water1', 'water2')
    """

    def __init__(self, structur_type):

        self.structur_type = structur_type
        self.bottom_left_cor = [None, None]
        self.top_right_cor = [None, None]
        self.structure_name = None

    def get_corners(self):
        """ 
        Returns all corners.
        The order is bottom_left, bottom_right, top_left, top_right.
        """

        return self.corners

    def set_corners(self):
        """ Sets the bottom_right_cor and top_left_cor"""

        self.bottom_right_cor = [self.top_right_cor[0], self.bottom_left_cor[1]]
        self.top_left_cor = [self.bottom_left_cor[0], self.top_right_cor[1]]

        self.corners = [self.bottom_left_cor, self.bottom_right_cor, self.top_left_cor, self.top_right_cor]

    def __str__(self):

        return f"[{self.structure_name}, {self.bottom_left_cor}, {self.top_right_cor}, {self.structur_type}]"

    def __repr__(self):
        return self.__str__()

class House(Structure):

    def __init__(self, type_house, horizontal):
        super().__init__("House")

        self.type_house = type_house

        self.horizontal = horizontal

        # TODO changing horizontal should swap the width and height.
        if type_house == "bungalow":
            self.width = 11
            self.height = 7
            self.mandatory_free_space = 3
            self.state = 3
            self.value = 399000
            self.extra_value = 0.04

            self.set_orientation(horizontal)

        elif type_house == "maison":
            self.width = 12
            self.height = 10
            self.state = 4
            self.mandatory_free_space = 6
            self.value = 610000
            self.extra_value = 0.06

            self.set_orientation(horizontal)


        elif type_house == "one_person_home":
            self.width = 8
            self.height = 8
            self.state = 2
            self.mandatory_free_space = 2
            self.value = 285000
            self.extra_value = 0.03

            self.set_orientation(horizontal)

        else:
            print("Invalid type_house")

    def set_orientation(self, horizontal):
        """ Adjusts the width and height depending on the if the house object is placed horizontal or not. """

        width = self.width
        height = self.height

        if horizontal:
            self.width = max(width, height)
            self.height = min(width, height)

        else:
            self.width = min(width, height)
            self.height = max(width, height)

        self.horizontal = horizontal
        

    def __str__(self):

        return f"{self.type_house}: {self.bottom_left_cor}, {self.top_right_cor}"

    def __repr__(self):

        return self.__str__()


