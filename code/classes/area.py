import os
import csv
import matplotlib
import matplotlib.pyplot as plt
import math

from .structure import Structure, House


class Area():

    def __init__(self, neighbourhood, houses):
        self.height = 180
        self.width = 160

        # Stores all structures in their respective type
        self.structures = {"Water": [], "House":[]}

        self.load_water(neighbourhood)
    
        # Calculate the number of houses per type
        self.houses = houses
        self.one_person_house_count = int(0.6 * houses)
        self.bungalow_count = int(0.25 * houses)
        self.maison_count = int(0.15 * houses)

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
        location = "../../wijken/" + filename + ".csv"
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

        return total_worth

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

        if bottom_left_cor[0] < 0 or bottom_left_cor[1] < 0 or top_right_cor[0] > self.width or top_right_cor[1] > self.height:
            return False

        return True

    def make_csv_output(self):
        """ Function which commands to update the output """

        # Store values csv_output_list
        csv_output_list = self.make_csv_output_list()

        print(csv_output_list)

        # Use csv_output_list to make the csv-output
        # self.csv_output(csv_output_list)
    
    def make_csv_output_list(self):
        """ Stores house-coordinates in a nested list """

        water_count = 1
        one_person_count = 1
        bungalow_count = 1
        maison_count = 1

        csv_output_list = [['structure','bottom_left_xy','top_right_xy','type']]

        for key in self.structures:
            for area_type in self.structures[key]:
                if area_type.structur_type == 'Water':
                    structure = area_type.structur_type.lower() + str(water_count)
                    type_area = area_type.structur_type.upper()
                    water_count += 1
                elif area_type.type_house == 'one_person_home':
                    structure = area_type.type_house + '_' + str(one_person_count)
                    type_area = area_type.type_house.upper()
                    one_person_count += 1
                elif area_type.type_house == 'bungalow':
                    structure = area_type.type_house + '_' + str(bungalow_count)
                    type_area = area_type.type_house.upper()
                    bungalow_count += 1
                elif area_type.type_house == 'maison':
                    structure = area_type.type_house + '_' + str(maison_count)
                    type_area = area_type.type_house.upper()
                    maison_count += 1

                bottom_left_xy = str(area_type.bottom_left_cor[0]) + ',' + str(area_type.bottom_left_cor[1])
                top_right_xy = str(area_type.top_right_cor[0]) + ',' + str(area_type.top_right_cor[1])

                csv_output_list.append([structure,bottom_left_xy,top_right_xy,type_area])

        return csv_output_list

    def csv_output(self, csv_output_list):
        """ (Over)writes the houselist into the ouput.csv """

        # Specify the path of the csv-file
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../../csv-output/output.csv")

        # Open the current output.csv
        with open(path, 'w', newline='') as myfile:
            wr = csv.writer(myfile)

            # (Over)write each line of csv_output_list into the csv-file
            for house in csv_output_list:
                wr.writerow(house)