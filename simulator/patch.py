from math import pi
import math
from events import ColonisationEvent, ExtinctionEvent


class Patch:
    def __init__(self, status, x_coord, y_coord, radius):
        # static patch values
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.radius = radius
        self.area = pi * (radius**2)

        # runtime patch variables
        self.status = status  # true if occupied, false if unoccupied.
        self.events = []  # extinction, and colonisation event for patch
        self.colonisation_value = 1
        self.extinction_value = 1

    def event(self):
        match self.status:
            case True: # if patch is occupied,
                self.status = False # patch becomes unoccupied.
            case False: # if patch is unoccupied,
                self.status = True # patch becomes occupied.

    def distance(self, patch_j):
        # think about making this a Patch class method
        # think about storing adjacency matrix in each Patch, for distances to each other patch

        i_coords = self.get_coords()
        j_coords = patch_j.get_coords()

        return math.sqrt((i_coords[0] - j_coords[0]) ** 2 + (i_coords[1] - j_coords[1]) ** 2)

    def create_events(self):
        self.events = [ColonisationEvent(self), ExtinctionEvent(self)]
        return self.events

    def update_events(self):
        for event_i in self.events:
            event_i.update_probability()

    def set_status(self, status):
        self.status = status

    def is_occupied(self):
        return self.status

    def set_coords(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def get_coords(self):
        return self.x_coord, self.y_coord

    def set_radius(self, radius):
        self.radius = radius
        self.area = pi * (radius ** 2)

    def get_radius(self):
        return self.radius

    def get_area(self):
        return self.area

    def set_colonisation_value(self, colonisation):
        self.colonisation_value = colonisation

    def get_colonisation_value(self):
        return self.colonisation_value

    def set_extinction_value(self, extinction):
        self.extinction_value = extinction

    def get_extinction_value(self):
        return self.extinction_value

    def __str__(self):
        return f"Status: {self.status}, coordinates: {self.x_coord}, {self.y_coord}, radius: {self.radius} area: {self.area}\n "
