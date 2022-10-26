from math import pi

class Patch:
    def __init__(self, status, x, y, r):
        self.status = status
        self.probability = 0
        self.x_coord = x
        self.y_coord = y
        self.radius = r
        self.area = pi * (r**2)

    def event(self):
        match self.status:
            case 1:
                self.status = 0
            case 2:
                self.status = 1

    def calculateProbability(self, probability):
        self.probability = probability

    def __str__(self):
        return f"Status: {self.status}, event probability: {self.probability}\n coordinates: {self.x_coord}, {self.y_coord}, radius: {self.radius} area: {self.area}\n"

