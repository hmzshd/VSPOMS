"""
VSPOM Simulator.

Should output:

    proportion of occupied patches (p) per time
        plot average if multiple replicates
    proportion of occupied area (pA) per time
        plot average if multiple replicates
    log10(P[extinction]) per time (?)
    turnover events (ext. + col. events) per time
    proportion of surviving replicates per time


Classes:
    Simulator
"""

# pylint: disable=line-too-long

import math
import random
from itertools import accumulate
from bisect import bisect
import pandas
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
    proportion_occupied_patches: float
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
        self.proportion_occupied_patches = 0
        self.proportion_occupied_area = 0
        self.time = 0

        # pandas dataframe to store results
        self.data = pandas.DataFrame(columns=[
            "time", "proportion occupied patches",
            "proportion occupied area", "extinction"])

        # lists for storing x,y coords of patches that
        # have had events happen to them, and the status of said patches
        # used to create a CDS for communication with the backend
        self.x_coords = []
        self.y_coords = []
        self.statuses = []

        # dict for storing the data the frontend needs, in the format
        # the frontend needs, to display the patches getting
        # colonised or going extinct.

        self.patch_dict = None

        # set all interacting simulation variables
        self.setup()

    def simulate(self):
        """
        Performs self.replicates full simulations with self.steps steps.
        When done returns the dict generated
        """

        while not self.done:
            self.step()

        if self.patch_dict == None:
            raise ValueError
        else:
            return self.patch_dict

    def step(self):
        """
        Performs Gillespie process once.

        Increments self.step, or self.replicate if the current replicate ends.

        Calls self.end() if the simulation is done.
        """

        self.update_frame()

        if self.completed_steps == 0:
            print(f'Replicate {self.completed_replicates + 1}:')
        elif self.completed_steps % 20 == 0:
            print(f'    Completed {self.completed_steps} steps.')
            # self.print_status()

        if self.completed_steps < self.steps:  # sim does not need to start new replicate. does one step.
            selected_patch = self.gillespie_process()
            self.update_patch_lists(selected_patch)
            self.completed_steps += 1
        elif self.completed_replicates < self.replicates:  # starts new replicate.
            self.completed_steps = 0
            self.completed_replicates += 1
            self.setup()
        else:  # all replicates have been completed.
            self.generate_dict()
            self.end()

    def gillespie_process(self):
        """
        Performs Gillespie process using object attributes.

        Gillespie process:
            1) Given the state of the system we calculate the rates for every possible event that can occur;
            2) we use a random number to determine which event does occur;
            3) we use the sum of all the rates to calculate the time increment;
            4) we update time and the state of the system given the event that occurred;
            returns the patch that has been selected on completion
        """

        self.update_rates()  # step 1

        selected_event = self.select_event()  # step 2
        selected_event.do_event()

        self.increment_time(selected_event)  # step 4

        return selected_event.patch

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
        self.update_proportion_occupied_patches()
        self.update_proportion_occupied_area()

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
        self.turnover_events = 0
        self.time = 0

        for patch_i in self.patches:
            patch_i.set_colonisation_value(self.colonization(patch_i))
            patch_i.set_extinction_value(self.extinction(patch_i))

            col_event, ext_event = patch_i.create_events()
            self.events.append(col_event)
            self.events.append(ext_event)

        self.update_total_colonisation_rate()
        self.update_total_extinction_rate()
        self.update_proportion_occupied_patches()
        self.update_proportion_occupied_area()

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
        print('End.')

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

    def update_proportion_occupied_patches(self):
        """
        Updates self.proportion_occupied_patches.
        """

        patch_total = len(self.patches)

        occupied_total = 0
        for patch_i in self.patches:
            if patch_i.is_occupied():
                occupied_total += 1

        # proportion of patches that are occupied.
        self.proportion_occupied_patches = occupied_total / patch_total

    def update_proportion_occupied_area(self):
        """
        Updates self.proportion_occupied_area.
        """

        area_total = 0
        area_occupied = 0

        for patch_i in self.patches:
            area_total += patch_i.get_area()
            if patch_i.is_occupied():
                area_occupied += patch_i.get_area()

        # proportion of area that is occupied.
        self.proportion_occupied_area = area_occupied / area_total

    def print_status(self):
        """Temp debug function to observe changes."""

        print(f'      Time: {self.time}, Proportion occupied: {self.proportion_occupied_patches}')

    def get_frame(self):
        """TEMP returns internal dataframe as a nice pretty lil stringy wingy."""
        return self.data.to_string()

    def update_frame(self):
        """
        Concats new row onto DataFrame self.data containing current data.
        """
        new_frame = pandas.DataFrame({
            "time": [self.time],
            "proportion occupied patches": [self.proportion_occupied_patches],
            "proportion occupied area": [self.proportion_occupied_area],
            "extinction": [self.total_extinction_rate]
        })

        self.data = pandas.concat([self.data, new_frame], ignore_index=True)

    def update_patch_lists(self, patch):
        """
        function to update the patch lists, needed for backend
        """
        self.x_coords.append(patch.x_coord)
        self.y_coords.append(patch.y_coord)
        self.statuses.append(patch.status)

    def generate_dict(self):
        self.patch_dict = {"x_coords": self.x_coords, "y_coords": self.y_coords, "statuses": self.statuses}
