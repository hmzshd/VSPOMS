from math import pi

class Patch:
    def __init__(self, status, x, y, r):
        self.status = status
        self.probability = 0.0
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


    def set_probability(self, prob):
        self.probability = prob


    def calculateProbability(self, probability):
        self.probability = probability


    def set_status(self, status):
        self.status = status


    def get_status(self):
        return self.status


    def set_coords(self, x, y):
        self.x_coord = x
        self.y_coord = y


    def get_coords(self):
        return (self.x_coord, self.y_coord)


    def set_radius(self, radius):
        self.radius = radius
        self.area = pi * (radius ** 2)


    def get_radius(self):
        return self.radius


    def get_area(self):
        return self.area


    def __str__(self):
        return f"Status: {self.status}, event probability: {self.probability}\n coordinates: {self.x_coord}, {self.y_coord}, radius: {self.radius} area: {self.area}\n"
