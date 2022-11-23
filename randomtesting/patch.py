from math import pi
import math


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
            case 0:
                self.status = 1

    def distance(self, patch_j):
        # think about making this a Patch class method
        # think about storing adjacency matrix in each Patch, for distances to each other patch

        i_coords = self.get_coords()
        j_coords = patch_j.get_coords()

        return math.sqrt((i_coords[0] - j_coords[0]) ** 2 + (i_coords[1] - j_coords[1]) ** 2)


    def set_probability(self, prob):
        self.probability = prob

    def get_probability(self):
        return self.probability

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_coords(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def get_coords(self):
        return self.x_coord, self.y_coord

    def set_radius(self, radius):
        self.radius = radius
        self.area = pi * (radius ** 2)

    def get_radius(self):
        return self.radius

    def get_area(self):
        return self.area

    def __str__(self):
        return f"Status: {self.status}, event probability: {self.probability}\n coordinates: {self.x_coord}, {self.y_coord}, radius: {self.radius} area: {self.area}\n "
