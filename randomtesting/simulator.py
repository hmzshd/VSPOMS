import math
import random
from numpy.random import exponential
from itertools import accumulate
from bisect import bisect
from patch_generate import generate_patch_list_random
from events import ColonisationEvent, ExtinctionEvent


# to create simulator object


class Simulator:

    # Initialises empty Simulator.
    def __init__(self, patches):
        # list of patches, list of events.
        self.patches = patches
        self.events = []

        # simulation constants
        self.dispersal_alpha = 1  # Species specific dispersal constant, for kernel.
        self.area_exponent_b = 1  # for connectivity.
        self.species_specific_constant_y = 1  # for colonisation.
        self.species_specific_constant_u = 1  # for extinction.
        self.patch_area_effect_x = 1  # for extinction.

        # simulation variables
        self.total_colonisation_rate = 1
        self.total_extinction_rate = 1
        self.proportion_occupied = 0
        self.time = 0

        # set all interacting simulation variables
        self.setup()

    def simulate(self, steps, replicates):
        for replicate in range(replicates):
            print(f'Replicate {replicate + 1}:')
            for step in range(steps):
                self.gillespie_process()
                if (step + 1) % 20 == 0:
                    print(f'    Completed {step+1} steps.')

    def gillespie_process(self):
        # 1) Given the state of the system we calculate the rates for every possible
        #  event that can occur;
        self.update_rates()

        # 2) we use a random number to determine which event does occur;
        selected_event = self.select_event()
        selected_event.do_event()

        # 3) we use the sum of all the rates to calculate the time increment;
        # 4) we update time and the state of the system given the event that occurred;
        self.increment_time(selected_event)

    def increment_time(self, selected_event):
        # The waiting time to the next event is an exponentially distributed random variable with
        # mean equal to the inverse of the sum of the rates. So the faster everything is
        # happening the less time between successive events.
        if isinstance(selected_event, ColonisationEvent):
            self.time += exponential(1 / self.total_colonisation_rate)
        elif isinstance(selected_event, ExtinctionEvent):
            self.time += exponential(1 / self.total_extinction_rate)

    # updates colonisation and extinction rates for each patch and event.
    def update_rates(self):
        for patch_i in self.patches:
            patch_i.set_colonisation_value(self.colonization(patch_i))
            patch_i.set_extinction_value(self.extinction(patch_i))
            patch_i.update_events()

        self.update_total_colonisation_rate()
        self.update_total_extinction_rate()
        self.update_proportion_occupied()

    # sets up initial correct conditions for simulation.
    def setup(self):
        for patch_i in self.patches:
            patch_i.set_colonisation_value(self.colonization(patch_i))
            patch_i.set_extinction_value(self.extinction(patch_i))

            col_event, ext_event = patch_i.create_events()
            self.events.append(col_event)
            self.events.append(ext_event)

        self.update_total_colonisation_rate()
        self.update_total_extinction_rate()
        self.update_proportion_occupied()

    # returns event weighted-randomly, according to their probability.
    # cum_weights maintains an array of cumulated probabilities. Is therefore sorted.
    # generates random probability in this range.
    # probability is then used to bisect cum_weights, finding the event corresponding.
    def select_event(self):
        # based on random.choices()
        length = len(self.events)

        cum_weights = []
        for event in self.events:
            cum_weights.append(event.probability)
        cum_weights = list(accumulate(cum_weights))

        total = cum_weights[-1] + 0.0  # convert to float
        if total <= 0.0:
            raise ValueError('Total of weights must be greater than zero')

        upper = length - 1
        return self.events[bisect(cum_weights, random.random() * total, 0, upper)]

    def dispersal_kernel(self, patch_i, patch_j):
        return math.exp((-self.dispersal_alpha) * patch_i.distance(patch_j))

    def connectivity(self, patch_i):
        connectivity_total = 0
        for patch_j in self.patches:
            if patch_j != patch_i:
                connectivity_total += int(patch_j.is_occupied()) * self.dispersal_kernel(patch_i, patch_j) * (
                            patch_j.get_area() ** self.area_exponent_b)
        return connectivity_total

    def colonization(self, patch_i):
        if patch_i.is_occupied():
            return 0.0
        return 1 - math.exp(-self.species_specific_constant_y * self.connectivity(patch_i))

    def extinction(self, patch_i):
        if patch_i.is_occupied():
            extinction_value = self.species_specific_constant_u / (patch_i.get_area() ** self.patch_area_effect_x)
            if extinction_value > 1:
                return 1
            return extinction_value
        return 0

    def update_total_colonisation_rate(self):
        rate = 0
        for patch_i in self.patches:
            rate += patch_i.get_colonisation_value()
        self.total_colonisation_rate = rate

    def update_total_extinction_rate(self):
        rate = 0
        for patch_i in self.patches:
            rate += patch_i.get_extinction_value()
        self.total_extinction_rate = rate

    def update_proportion_occupied(self):
        patch_total = len(self.patches)

        occupied_total = 0
        for patch_i in self.patches:
            if patch_i.is_occupied():
                occupied_total += 1

        # proportion of patches that are occupied.
        self.proportion_occupied = occupied_total / patch_total


patch_list = generate_patch_list_random(30)
spom_sim = Simulator(patch_list)
spom_sim.simulate(100, 5)
