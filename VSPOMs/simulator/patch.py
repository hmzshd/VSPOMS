"""
Contains Patch class for use within a simulator.Simulator object.

Classes:
    Patch
"""

# pylint: disable=line-too-long

from math import pi
import math
from events import ColonisationEvent, ExtinctionEvent


class Patch:
    """
    Creates a patch object.

    Attributes
    ---
        x_coord: float
        y_coord: float
            Coordinates of the patch's location.
        radius: float
            radius of the patch.
        area:
            area of the patch. calculated from radius.

        status: boolean
            true if occupied, false if unoccupied.
        events: list
            list of the two possible turnover events for the patch.
        colonisation_value: float
        extinction_value: float
            patch values calculated by simulator.Simulator.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, status, x_coord, y_coord, radius):
        """
        Initialises Patch object.
        """

        # static patch values
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.radius = radius
        self.area = pi * (radius**2)

        # runtime patch variables
        self.status = status  # true if occupied, false if unoccupied.
        self.events = []  # extinction, and colonisation event for patch
        self.colonisation_value = 1.0
        self.extinction_value = 1.0

    def event(self):
        """
        Toggles patch's occupation status, self.status.
        """
        match self.status:
            case True:  # if patch is occupied,
                self.status = False  # patch becomes unoccupied.
            case False:  # if patch is unoccupied,
                self.status = True  # patch becomes occupied.

    def distance(self, patch_j):
        """
        Returns the cartesian distance between this patch and another patch.
        Consider instead storing an adjacency matrix in each patch for computational efficiency.
        """

        i_coords = self.get_coords()
        j_coords = patch_j.get_coords()

        return math.sqrt((i_coords[0] - j_coords[0]) ** 2 + (i_coords[1] - j_coords[1]) ** 2)

    def create_events(self):
        """
        Creates an extinction event, and a colonisation event for the patch.

        Events are stored in self.events and returned.
        """
        self.events = [ColonisationEvent(self), ExtinctionEvent(self)]
        return self.events

    def update_events(self):
        """
        Events are updated as per the event's .update_probability() method.
        """
        for event_i in self.events:
            event_i.update_probability()

    def set_status(self, status):
        """set occupation status"""
        self.status = status

    def is_occupied(self):
        """return occupation status"""
        return self.status

    def set_coords(self, x_coord, y_coord):
        """set patch coordinates"""
        self.x_coord = x_coord
        self.y_coord = y_coord

    def get_coords(self):
        """return patch coordinates"""
        return self.x_coord, self.y_coord

    def set_radius(self, radius):
        """set patch radius"""
        self.radius = radius
        self.area = pi * (radius ** 2)

    def get_radius(self):
        """return patch radius"""
        return self.radius

    def get_area(self):
        """return patch area"""
        return self.area

    def set_colonisation_value(self, colonisation):
        """set patch colonisation rate"""
        self.colonisation_value = colonisation

    def get_colonisation_value(self):
        """return patch colonisation rate"""
        return self.colonisation_value

    def set_extinction_value(self, extinction):
        """set patch extinction rate"""
        self.extinction_value = extinction

    def get_extinction_value(self):
        """return patch extinction rate"""
        return self.extinction_value

    def __str__(self):
        """returns a pretty string containing some of the patch's important data"""
        return f"Status: {self.status}, coordinates: " \
               f"{self.x_coord}, {self.y_coord}, radius: {self.radius} area: {self.area}\n "
