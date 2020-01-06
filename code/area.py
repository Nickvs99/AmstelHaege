"""
    Responsible for making grid.


"""

class area():

    def __init__(self):

        self.height = 8
        self.width = 5

        self.area = self.createArea()

    def createArea(self):

        row = [0] * self.width

        return [row] * self.height