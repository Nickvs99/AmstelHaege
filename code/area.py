"""
    Responsible for making grid.


"""
import csv
import os.path
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
                print(f"{bottom} , {left} - {top} , {right}")

                for i in range(int(bottom),int(top)):
                    for j in range(int(left),int(right)):
                        self.area[i][j] = 1


    def ShowArea(self):
        plt.imshow(self.area, cmap=plt.cm.Accent)
        plt.show()
