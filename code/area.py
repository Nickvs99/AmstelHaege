"""
    Responsible for making grid.


"""

class area():

    def __init__(self):

        self.height = 160
        self.width = 180

        self.area = self.createArea()

    def createArea(self):

        row = [0] * self.width

        return [row] * self.height