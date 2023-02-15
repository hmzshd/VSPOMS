"""
Contains classes to create events for simulator.Simulator.

Classes
---
    Event
        Abstract class to provide superclass for ColonisationEvent and ExtinctionEvent
    ColonisationEvent
        Event whose probability is it's patches colonisation rate
    ExtinctionEvent
        Event whose probability is it's patches colonisation rate
"""

from abc import ABC, abstractmethod


class Event(ABC):
    """abstract class to provide super for belows"""

    def __init__(self, patch):
        """Constructor to be inherited."""
        self.patch = patch
        self.probability = 0
        self.update_probability()

    @abstractmethod
    def update_probability(self):
        """abstract because event types have their own probability functions."""

    def do_event(self):
        """toggles patch occupation status"""
        self.patch.event()

    def get_probability(self):
        """returns weight of event being selected"""
        return self.probability

    def __str__(self):
        """string :)"""

        occupied_string = "UNASSIGNED"
        match self.patch.is_occupied():
            case True:
                occupied_string = 'occupied'
            case False:
                occupied_string = 'unoccupied'
        return f"{type(self).__name__} of probability {self.probability} at" \
               f" {occupied_string} patch:" \
               f" {self.patch.get_coords()[0]},{self.patch.get_coords()[1]}"


class ColonisationEvent(Event):
    """colonisation event"""

    def update_probability(self):
        """sets probability using patch's colonisation function in context of the simulation."""
        self.probability = self.patch.get_colonisation_value()


class ExtinctionEvent(Event):
    """extinction event"""

    def update_probability(self):
        """sets probability using patch's extinction function in context of the simulation."""
        self.probability = self.patch.get_extinction_value()
