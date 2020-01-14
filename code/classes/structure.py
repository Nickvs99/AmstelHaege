import math

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

        self.neighbour_distances = {}

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

    def init_distances(self, houses):
        """ 
        Initiialize the distances for all houses.
        The key is a the structure_name for all houses.
        Value is math.inf
        """

        self.neighbour_distances = {}

        for h in houses:

            if h == self:
                continue

            self.neighbour_distances[h.structure_name] = math.inf

    

    def get_min_dist(self):
        """ Returns the minimum distance from all distances. """

        return min(self.neighbour_distances.values())

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

        return f"{self.structure_name}: {self.bottom_left_cor}, {self.top_right_cor}, {self.get_min_dist()}"

    def __repr__(self):

        return self.__str__()