import math

# to create simulator object

class Simulator:

    # Initialises empty Simulator.
    def __init__(self):
        self.patches = []
        self.species_specific_dispersal_constant_a = 1
        self.area_factor_ab = 1
        self.species_specific_constant_y = 1
        self.species_specific_constant_u = 1
        self.patch_area_effect_x = 1

    def gillespie_process(self):
        pass

    def dispersal_kernel(self, patch_i, patch_j):
        # parameter a is the species-specific dispersal constant.

        return math.exp((-self.species_specific_dispersal_constant_a) * self.distance(patch_i, patch_j))

    def connectivity(self, patch_i):
        # MUST CLARIFY EXPONENT ON AREA FACTOR
        # b is area factor exponent ??? clarify!

        connectivity_total = 0
        for patch in self.patches:
            if patch != patch_i:
                connectivity_total += patch.get_probability() * self.dispersal_kernel(patch_i, patch) * patch.get_area()

        return connectivity_total

    def colonization(self, patch_i):
        # y is species-specific constant
        # MUST CLARIFY WHETHER y=a

        return 1 - math.exp(-self.species_specific_constant_y * self.connectivity(patch_i))

    def extinction(self, patch):
        # clarify x - as patch area factor exponent

        extinction_value = self.species_specific_constant_u / patch.get_area ** self.patch_area_effect_x
        if extinction_value > 1:
            return 1.0

        return extinction_value

    def distance(self, patch_i, patch_j):
        # think about making this a Patch class method
        # think about storing adjacency matrix in each Patch, for distances to each other patch

        i_coords = patch_i.get_coords()
        j_coords = patch_j.get_coords()

        return math.sqrt((i_coords[0] - j_coords[0]) ** 2 + (i_coords[1] - j_coords[1]) ** 2)
