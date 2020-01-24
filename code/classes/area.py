import os
import csv
import matplotlib
import matplotlib.pyplot as plt
import math

from .structure import Structure, House


class Area():
    """ 
    Area object. This object stores information about:
    - width and height
    - the number of houses
    - the number of houses per house type
    - all Structure objects
    
    Furthermore it provides the tools to:
    - check if a house would be at a valid place
    - calc worth area
    - creates the csv output
    - updates the distances to neighbours for each house
    """

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

    def load_water(self, neighbourhood):
        """ Gets the water from the csv file and creates objects from them. """

        # Specify the path of the csv-file
        my_path = os.path.abspath(os.path.dirname(__file__))
        location = "..\..\wijken\\" + neighbourhood + ".csv"
        path = os.path.join(my_path, location)

        water_count = 0
        # Open the csv-file as a dictionary
        with open(path) as csv_file:

                csv_reader = csv.DictReader(csv_file)

                # Retrieve the coordinates of the bottom-left and top-right of the water(s)
                for row in csv_reader:
                    bottom,left = row['bottom_left_xy'].split(",")
                    top,right  = row['top_right_xy'].split(",")

                    bottom, left, top, right = int(bottom), int(left), int(top), int(right)

                    # Create the water object
                    water = Structure("water_" + str(water_count))

                    water.bottom_left_cor = [bottom, left]
                    water.top_right_cor = [top, right]
                    water.set_corners()

                    self.structures["Water"].append(water)

                    water_count += 1
        
    def fill_area(self, area):
        """ Fill the area with the objects with the state of the structures"""

        for water in self.structures["Water"]:

            for y in range(water.bottom_left_cor[1], water.top_right_cor[1]):
                for x in range(water.bottom_left_cor[0], water.top_right_cor[0]):
                    area[y][x] = 1

        for house in self.structures["House"]:

            for y in range(house.bottom_left_cor[1], house.top_right_cor[1]):
                for x in range(house.bottom_left_cor[0], house.top_right_cor[0]):
                    area[y][x] = house.state

    def plot_area(self, neighbourhood, houses, algorithm):
        """ Plots the area """
        
        area = self.create_area()
        self.fill_area(area)

        colorscheme = matplotlib.colors.ListedColormap(['#73b504', '#88AAFF', '#ee4035', '#ffb455', '#b266b2'])
        plt.imshow(area, cmap = colorscheme)
        plt.gca().invert_yaxis()
        plt.axis('off')
        plt.title(f"{neighbourhood.capitalize()} | {houses} Houses | {algorithm.capitalize()} | Area Worth = {self.calc_worth_area()}")
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

        # Checks if any of the corners of the test_house are in water
        for water in self.structures["Water"]:

            for test_corner in test_corners:
                if self.check_within_custom_bounds(test_corner[0], test_corner[1], water.corners[0], water.corners[3]):
                    return False

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
        
        for house in self.structures["House"]:
            total_worth += house.calc_worth()

        return total_worth


    def check_in_bound(self, bottom_left_cor, top_right_cor):
        """ Checks if a given x and y coordinates fall within the bounds. """

        if bottom_left_cor[0] < 0 or bottom_left_cor[1] < 0 or top_right_cor[0] > self.width or top_right_cor[1] > self.height:
            return False

        return True

    def make_csv_output(self):
        """ Function which updates the output file """

        # Store values csv_output_list
        csv_output_list = self.make_csv_output_list()

        # Use csv_output_list to make the csv-output
        self.csv_output(csv_output_list)
    
    def make_csv_output_list(self):
        """ Stores house-coordinates in a nested list """

        csv_output_list = [['structure','bottom_left_xy','top_right_xy','type']]

        for key in self.structures:
            for structure in self.structures[key]:

                # Make string representation of the coordinates
                bottom_left_xy = str(structure.bottom_left_cor[0]) + ',' + str(structure.bottom_left_cor[1])
                top_right_xy = str(structure.top_right_cor[0]) + ',' + str(structure.top_right_cor[1])

                # Append values to the csv_output_list
                csv_output_list.append([structure.name,bottom_left_xy,top_right_xy,structure.type])

        return csv_output_list

    def csv_output(self, csv_output_list):

        """ (Over)writes the houselist into the ouput.csv """

        # Specify the path of the csv-file
        my_path = os.path.abspath(os.path.dirname(__file__))

        path = os.path.join(my_path, "..\..\csv-output\output.csv")

        # Open the output.csv file
        with open(path, 'w', newline='') as myfile:
            wr = csv.writer(myfile)

            # (Over)write each line of house_list into the csv-file
            for structure in csv_output_list:
                wr.writerow(structure)
    
    def update_distances(self, house):
        """ Update the distances."""
        
        # Reset all distances for house
        house.init_distances(self.structures["House"])

        # Reset all distances related to the house
        for h in self.structures["House"]:
            
            if h == house:
                continue
            
            h.neighbour_distances[house.name] = math.inf
        
        for h in self.structures["House"]:
            
            if h == house:
                continue

            for corner in h.corners:

                for new_corner in house.corners:

                    x_dist = abs(corner[0] - new_corner[0])
                    y_dist = abs(corner[1] - new_corner[1])

                    # Use the maximum value, since the minimum value wouldnt reach the object
                    dist = max(x_dist, y_dist)

                    if dist < h.neighbour_distances[house.name]:
                        h.neighbour_distances[house.name] = dist
                    
                    if dist < house.neighbour_distances[h.name]:
                        house.neighbour_distances[h.name] = dist
