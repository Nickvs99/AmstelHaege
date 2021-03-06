import math

class Structure():
    """
    Structure object. This object stores:
    - bottom_left_cor
    - top_right_cor
    - the type ('Water' or 'House')
    - the name, a unique id ('water1', 'water2', etc.)
    """

    def __init__(self, name):
        
        self.bottom_left_cor = [None, None]
        self.top_right_cor = [None, None]
        self.name = name
        self.type = self.get_type(name)

    def get_type(self, name):
        """ 
        Returns the type of the house based on its name.
        ex. maison_23 -> maison
        """

        name_split = name.split("_")
        name_split.pop()
        name = "_".join(name_split)
        
        return name

    def set_corners(self):
        """ Sets the bottom right and top left coordinates of the object."""

        self.bottom_right_cor = [self.top_right_cor[0], self.bottom_left_cor[1]]
        self.top_left_cor = [self.bottom_left_cor[0], self.top_right_cor[1]]

        self.corners = [self.bottom_left_cor, self.bottom_right_cor, self.top_left_cor, self.top_right_cor]

    def __str__(self):

        return f"[{self.name}, {self.bottom_left_cor}, {self.top_right_cor}, {self.structur_type}]"

    def __repr__(self):
        return self.__str__()

class House(Structure):
    """
    House object. Inherits from the parent Structure class.
    Stores additional information, such as:
    - horizontal orientation
    - width and height
    - mandatory free space
    - base value
    - extra value
    - distances to neighbours
    
    Furthermore it provides the tools to:
    - calculate its worth

    """

    def __init__(self, name, horizontal):
        
        super().__init__(name)
        
        self.horizontal = horizontal

        self.neighbour_distances = {}

        if self.type == "bungalow":
            self.width = 11
            self.height = 7
            self.mandatory_free_space = 3
            self.state = 3
            self.value = 399000
            self.extra_value = 0.04

            self.set_orientation(horizontal)

        elif self.type == "maison":
            self.width = 12
            self.height = 10
            self.state = 4
            self.mandatory_free_space = 6
            self.value = 610000
            self.extra_value = 0.06

            self.set_orientation(horizontal)

        elif self.type == "one_person_home":
            self.width = 8
            self.height = 8
            self.state = 2
            self.mandatory_free_space = 2
            self.value = 285000
            self.extra_value = 0.03

            self.set_orientation(horizontal)

        else:
            print(f"Invalid type: {self.type}")

    def init_distances(self, houses):
        """ 
        Initializes the distances for all houses.
        The key is the name of all houses.
        Value is math.inf
        """

        self.neighbour_distances = {}

        for h in houses:

            if h == self:
                continue

            self.neighbour_distances[h.name] = math.inf

    def get_min_dist(self):
        """ Returns the minimum distance to a neighbour or if it does not exist the distance to the edge. """

        if self.neighbour_distances == {}:

            return min(self.bottom_left_cor[0], 160 - self.top_right_cor[0], self.bottom_left_cor[1], 180 - self.top_right_cor[1])
        
        else:
            return min(self.neighbour_distances.values())

    def set_orientation(self, horizontal):
        """ Adjusts the width and height of the house-object depending its orientation. """

        width = self.width
        height = self.height

        if horizontal:
            self.width = max(width, height)
            self.height = min(width, height)

        else:
            self.width = min(width, height)
            self.height = max(width, height)

        self.horizontal = horizontal
        
    def set_coordinates(self, bottom_left_cor, horizontal):
        """ Sets the coordinates based on its bottom left coordinates and its orientation"""

        self.set_orientation(horizontal)

        self.bottom_left_cor = bottom_left_cor
        self.top_right_cor = [bottom_left_cor[0] + self.width, bottom_left_cor[1] + self.height]

        self.set_corners()

    def calc_worth(self):
        """ 
        Calculates the worth of a house.
        worth = base_value + base_value * extra_value * (min_dist - mandatory_free_space)
        """

        base_value = self.value
        extra_value = self.value * self.extra_value * (self.get_min_dist() - self.mandatory_free_space)

        return base_value + extra_value

    def __str__(self):

        return f"{self.name}: {self.bottom_left_cor}, {self.top_right_cor}, {self.get_min_dist()}"

    def __repr__(self):

        return self.__str__()

