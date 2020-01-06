"""
    Responsible for making grid.


"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class area():

    def __init__(self):

        self.height = 10
        self.width = 5

        # self.area = self.createArea()

        self.area = [[ 0 for i in range(self.width)] for j in range(self.height)]


    def createArea(self):

        area = [[ 0 for i in range(self.width)] for j in range(self.height)]
        return area

    def ShowArea(self):
        plt.imshow(self.area, cmap=plt.cm.Accent)
        plt.show()
