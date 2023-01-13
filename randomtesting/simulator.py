"""
VSPOM Simulator.

Classes:
    Simulator
"""

# pylint: disable=line-too-long

import math
import random
from itertools import accumulate
from bisect import bisect
from numpy.random import exponential
from events import ColonisationEvent, ExtinctionEvent


class Simulator:
    """
    Creates simulator object.


    Attributes
    ---

    patches: list
        list of patches contained within the simulation.
    events: list
        list of possible events contained within the simulation.
    patches_backup: list
        maintains initial list of patches for the purpose of resetting the simulation for multiple replicates.

    dispersal_alpha: int
    area_exponent_b: int
    species_specific_constant_y: int
    species_specific_constant_u: int
    patch_area_effect_x: int
        Above are simulation constants.

    total_colonisation_rate: int
    total_extinction_rate: int
    proportion_occupied: int
    time: int
        Above are simulation variables.
    """

    # pylint: disable=too-many-instance-attributes

    # Initialises Simulator.
    def __init__(self, patches):
        """
        Initialises Simulator object.

        Parameters:
            patches (list): a list of patch.py Patch objects.
        """

        # list of patches, list of events.
        self.patches = list(patches)
        self.events = []

        # patch list backup for reset during setup.
        self.patches_backup = list(patches)

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
        """
        Performs specified amount of simulation replicates with specified steps.

        Parameters:
            steps (int): number of steps to perform in each simulation.
            replicates (int): number of replicates to perform of the simulation.
        """

        for replicate in range(replicates):
            self.setup()
            print(f'Replicate {replicate + 1}:')
            for step in range(steps):
                self.gillespie_process()
                if (step + 1) % 20 == 0:
                    print(f'    Completed {step+1} steps.')

    def gillespie_process(self):
        """
        Performs gillespie process using object attributes.

        Gillespie process:
            1) Given the state of the system we calculate the rates for every possible event that can occur;
            2) we use a random number to determine which event does occur;
            3) we use the sum of all the rates to calculate the time increment;
            4) we update time and the state of the system given the event that occurred;
        """

        self.update_rates()

        selected_event = self.select_event()
        selected_event.do_event()

        self.increment_time(selected_event)

    def increment_time(self, selected_event):
        """
        Increments self.time. The waiting time to the next event is an exponentially distributed random variable with
        mean equal to the inverse of the sum of the rates. So the faster everything is happening the less time between
        successive events.

        Parameters:
            selected_event (Event): event selected to happen by select_event().
        """

        if isinstance(selected_event, ColonisationEvent):
            self.time += exponential(1 / self.total_colonisation_rate)
        elif isinstance(selected_event, ExtinctionEvent):
            self.time += exponential(1 / self.total_extinction_rate)

    def update_rates(self):
        """
        Updates colonisation and extinction rates for each patch.
        Updates possible event for each patch.
        Updates proportion of total occupied area.
        """

        for patch_i in self.patches:
            patch_i.set_colonisation_value(self.colonization(patch_i))
            patch_i.set_extinction_value(self.extinction(patch_i))
            patch_i.update_events()

        self.update_total_colonisation_rate()
        self.update_total_extinction_rate()
        self.update_proportion_occupied()

    def setup(self):
        """
        sets up initial correct conditions for simulation.

        Steps:
            Resets self.patches to self.patches_backup.
            Sets each patch's colonisation value.
            Sets each patch's extinction value.
            Creates events for each patch.
            Updates total colonisation and extinction rates.
            Updates proportion occupied.
        """

        self.patches = list(self.patches_backup)

        for patch_i in self.patches:
            patch_i.set_colonisation_value(self.colonization(patch_i))
            patch_i.set_extinction_value(self.extinction(patch_i))

            col_event, ext_event = patch_i.create_events()
            self.events.append(col_event)
            self.events.append(ext_event)

        self.update_total_colonisation_rate()
        self.update_total_extinction_rate()
        self.update_proportion_occupied()

    def select_event(self):
        """
        Returns event randomly, weighted by their probability, selected from self.events.
        cum_weights maintains an array of cumulative probabilities of each self.events, so is therefore sorted
        ascending.
        Generates random float in the range of 0 to the sum of probabilities.
        bisect() is used to find the first index of cum_weights whose value is greater than this float.

        Based on random.choices().

        Returns:
            Event selected randomly weighted by it's probability.
        """

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
        """
        Calculates dispersal kernel, which describes the probability for an occupant of a patch to disperse from this
        patch to another.

        Parameters:
            patch_i (patch): origin patch
            patch_j (patch): destination patch

        Returns:
            dispersal kernel
        """

        return math.exp((-self.dispersal_alpha) * patch_i.distance(patch_j))

    def connectivity(self, patch_i):
        """
        Calculates total connectivity of a patch.

        Parameters:
            patch_i (patch): patch to calculate the connectivity of

        Returns:
            Connectivity of patch_i
        """

        connectivity_total = 0
        for patch_j in self.patches:
            if patch_j != patch_i:
                connectivity_total += int(patch_j.is_occupied()) * self.dispersal_kernel(patch_i, patch_j) * (
                            patch_j.get_area() ** self.area_exponent_b)
        return connectivity_total

    def colonization(self, patch_i):
        """
        Calculates colonisation rate of a patch.

        Parameters:
            patch_i (patch): patch to calculate colonisation rate of

        Returns:
            colonisation rate of patch_i
        """

        if patch_i.is_occupied():
            return 0.0
        return 1 - math.exp(-self.species_specific_constant_y * self.connectivity(patch_i))

    def extinction(self, patch_i):
        """
        Calculates extinction rate of a patch.

        Parameters:
            patch_i (patch): patch to calculate extinction rate of

        Returns:
            extinction rate of patch_i
        """

        if patch_i.is_occupied():
            extinction_value = self.species_specific_constant_u / (patch_i.get_area() ** self.patch_area_effect_x)
            if extinction_value > 1:
                return 1
            return extinction_value
        return 0

    def update_total_colonisation_rate(self):
        """
        Updates self.total_colonisation_rate.
        """

        rate = 0
        for patch_i in self.patches:
            rate += patch_i.get_colonisation_value()
        self.total_colonisation_rate = rate

    def update_total_extinction_rate(self):
        """
        Updates self.total_extinction_rate.
        """

        rate = 0
        for patch_i in self.patches:
            rate += patch_i.get_extinction_value()
        self.total_extinction_rate = rate

    def update_proportion_occupied(self):
        """
        Updates self.proportion_occupied.
        """

        patch_total = len(self.patches)

        occupied_total = 0
        for patch_i in self.patches:
            if patch_i.is_occupied():
                occupied_total += 1

        # proportion of patches that are occupied.
        self.proportion_occupied = occupied_total / patch_total
