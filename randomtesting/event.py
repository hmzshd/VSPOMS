
class Event:

    # if event_type = 0, event is colonisation.
    # if event_type = 1, event is extinction.
    def __init__(self, patch, event_type):
        self.patch = patch
        self.event_type = event_type

        match self.event_type:
            case 0:  # event is colonisation.
                match self.patch.is_occupied():
                    case True:
                        self.probability = 0
                    case False:
                        self.probability = self.patch.get_colonisation_value()
            case 1:  # event is extinction.
                match self.patch.is_occupied():
                    case True:
                        self.probability = self.patch.get_extinction_value()
                    case False:
                        self.probability = 0

    def update_probability(self):
        match self.event_type:
            case 0:  # event is colonisation.
                match self.patch.is_occupied():
                    case True:
                        self.probability = 0
                    case False:
                        self.probability = self.patch.get_colonisation_value()
            case 1:  # event is extinction.
                match self.patch.is_occupied():
                    case True:
                        self.probability = self.patch.get_extinction_value()
                    case False:
                        self.probability = 0

    def do_event(self):
        self.patch.event()
        self.update_probability()
