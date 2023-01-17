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

    steps (int): number of steps to perform in each simulation.
    replicates (int): number of replicates to perform of the simulation.

    dispersal_alpha: float
    area_exponent_b: float
    species_specific_constant_y: float
    species_specific_constant_u: float
    patch_area_effect_x: float
        Above are simulation constants.

    total_colonisation_rate: float
    total_extinction_rate: float
    proportion_occupied: float
    time: float
        Above are simulation variables.
    """

    # pylint: disable=too-many-instance-attributes

    # Initialises Simulator.
    def __init__(self, patches, steps, replicates):
        """
        Initialises Simulator object.

        For now, uses default SPOM definition from diamina.par.

        Parameters:
            patches (list): a list of patch.py Patch objects.
        """

        # list of patches, list of events.
        self.patches = list(patches)
        self.events = []

        # patch list backup for reset during setup.
        self.patches_backup = list(patches)

        # number of steps and replicates.
        self.steps = steps
        self.replicates = replicates - 1
        self.completed_steps = 0
        self.completed_replicates = 0

        # true if a full simulation has been completed.
        self.done = False

        # simulation constants
        self.dispersal_alpha = 0.71  # Species specific dispersal constant, for dispersal kernel.
        self.area_exponent_b = 0.5  # for connectivity.
        self.species_specific_constant_y = 5.22  # for colonisation.
        self.species_specific_constant_u = 0.0593  # for extinction.
        self.patch_area_effect_x = 1.08  # for extinction.

        # simulation variables
        self.total_colonisation_rate = 0
        self.total_extinction_rate = 0
        self.proportion_occupied = 0
        self.time = 0

        # set all interacting simulation variables
        self.setup()

    def simulate(self):
        """
        Performs self.replicates full simulations with self.steps steps.
        """

        while not self.done:
            self.step()

    def step(self):
        """
        Performs Gillespie process once.

        Increments self.step, or self.replicate if the current replicate ends.

        Calls self.end() if the simulation is done.
        """

        if self.completed_steps == 0:
            print(f'Replicate {self.completed_replicates + 1}:')
        elif self.completed_steps % 20 == 0:
            print(f'    Completed {self.completed_steps} steps.')
            # self.print_status()
        if self.completed_steps < self.steps:  # sim does not need to start new replicate. does one step.
            self.gillespie_process()
            self.completed_steps += 1
        elif self.completed_replicates < self.replicates:  # starts new replicate.
            self.completed_steps = 0
            self.completed_replicates += 1
            self.setup()
        else:  # all replicates have been completed.
            self.end()

    def gillespie_process(self):
        """
        Performs Gillespie process using object attributes.

        Gillespie process:
            1) Given the state of the system we calculate the rates for every possible event that can occur;
            2) we use a random number to determine which event does occur;
            3) we use the sum of all the rates to calculate the time increment;
            4) we update time and the state of the system given the event that occurred;
        """

        self.update_rates()  # step 1

        selected_event = self.select_event()  # step 2
        selected_event.do_event()

        self.increment_time(selected_event)  # step 4

    def increment_time(self, selected_event):
        """
        Increments self.time. The waiting time to the next event is an exponentially distributed random variable with
        mean equal to the inverse of the sum of the rates. So the faster everything is happening the less time between
        successive events.

        Parameters:
            selected_event (Event): event selected to happen by select_event().
        """

        # if total rates are 0, skips time increment.
        # not ideal, must find out what should happen in this case.
        if isinstance(selected_event, ColonisationEvent):
            if self.total_colonisation_rate > 0:
                self.time += exponential(1 / self.total_colonisation_rate)
        elif isinstance(selected_event, ExtinctionEvent):
            if self.total_extinction_rate > 0:
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
        sets up initial correct conditions for a replicate.

        Steps:
            Resets self.patches to self.patches_backup.
            Sets each patch's colonisation value.
            Sets each patch's extinction value.
            Creates events for each patch.
            Updates total colonisation and extinction rates.
            Updates proportion occupied.
        """

        self.patches = list(self.patches_backup)
        self.time = 0

        for patch_i in self.patches:
            patch_i.set_colonisation_value(self.colonization(patch_i))
            patch_i.set_extinction_value(self.extinction(patch_i))

            col_event, ext_event = patch_i.create_events()
            self.events.append(col_event)
            self.events.append(ext_event)

        self.update_total_colonisation_rate()
        self.update_total_extinction_rate()
        self.update_proportion_occupied()

    def reset(self):
        """
        Reset simulation status.
        Use after simulation is completed to start a fresh simulation.
        """

        self.setup()
        self.done = False
        self.completed_steps = 0
        self.completed_replicates = 0

    def end(self):
        """Ends current simulation run"""

        self.done = True
        print('donezo')

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

    def print_status(self):
        """Temp debug function to observe changes."""

        print(f'      Time: {self.time}, Proportion occupied: {self.proportion_occupied}')
