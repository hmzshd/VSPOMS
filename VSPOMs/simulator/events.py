from abc import ABC, abstractmethod


class Event(ABC):
    # abstract class to provide super for belows.

    def __init__(self, patch):
        self.patch = patch
        self.probability = 0
        self.update_probability()

    # event types have their own probability functions.
    @abstractmethod
    def update_probability(self):
        pass

    def do_event(self):
        self.patch.event()  # patch toggles occupation status.

    def get_probability(self):
        return self.probability

    def __str__(self):
        match self.patch.is_occupied():
            case True:
                occupied_string = 'occupied'
            case False:
                occupied_string = 'unoccupied'
        return f"{type(self).__name__} of probability {self.probability} at {occupied_string} patch: {self.patch.get_coords()[0]},{self.patch.get_coords()[1]}"


class ColonisationEvent(Event):

    def __init__(self, patch):
        super().__init__(patch)

    def update_probability(self):
        self.probability = self.patch.get_colonisation_value()


class ExtinctionEvent(Event):

    def __init__(self, patch):
        super().__init__(patch)

    def update_probability(self):
        self.probability = self.patch.get_extinction_value()
