from django.test import TestCase
from simulator.patch import Patch
from simulator.simulator import Simulator
import pandas

class SimulatorTestCase(TestCase):
    """
    expands upon django TestCase to see if simulator is being properly initialised and the attributes are the proper datatype."
    """
    def setUp(self):
        # create patches
        patch1 = Patch(status="occupied", x_coord=1, y_coord=5, area=25)
        patch2 = Patch(status="occupied", x_coord=2, y_coord=4, area=25)
        patch3 = Patch(status="occupied", x_coord=3, y_coord=3, area=30)
        patch4 = Patch(status="occupied", x_coord=4, y_coord=2, area=12)
        patch5 = Patch(status="occupied", x_coord=5, y_coord=1, area=16)
        patches = [patch1, patch2, patch3, patch4, patch5]
         
        #set simulator parameters
        dispersal_alpha = 0.1
        area_exponent_b = 0.2
        species_specific_constant_y = 0.3
        species_specific_constant_u = 0.4
        patch_area_effect_x = 0.5
        steps = 100
        replicates = 1
        self.simulator = Simulator(patches, dispersal_alpha, area_exponent_b, species_specific_constant_y, species_specific_constant_u, patch_area_effect_x, steps, replicates)

    def test_simulator_attributes(self):
        self.assertIsInstance(self.simulator.patches, list)
        self.assertIsInstance(self.simulator.events, list)
        self.assertIsInstance(self.simulator.patches_backup, list)
        self.assertIsInstance(self.simulator.steps, int)
        self.assertIsInstance(self.simulator.replicates, int)
        self.assertIsInstance(self.simulator.completed_steps, int)
        self.assertIsInstance(self.simulator.completed_replicates, int)
        self.assertIsInstance(self.simulator.done, bool)
        self.assertIsInstance(self.simulator.dispersal_alpha, float)
        self.assertIsInstance(self.simulator.area_exponent_b, float)
        self.assertIsInstance(self.simulator.species_specific_constant_y, float)
        self.assertIsInstance(self.simulator.species_specific_constant_u, float)
        self.assertIsInstance(self.simulator.patch_area_effect_x, float)
        self.assertIsInstance(self.simulator.total_colonisation_rate, float)
        self.assertIsInstance(self.simulator.total_extinction_rate, float)
        self.assertIsInstance(self.simulator.proportion_occupied_patches, float)
        self.assertIsInstance(self.simulator.proportion_occupied_area, float)
        self.assertIsInstance(self.simulator.data, pandas.DataFrame)
        self.assertIsInstance(self.simulator.x_coords, list)
        self.assertIsInstance(self.simulator.y_coords, list)
        self.assertIsInstance(self.simulator.statuses, list)
        self.assertIsInstance(self.simulator.patch_dict, type(None))

    def test_simulator_parameters(self):
        self.assertEqual(len(self.simulator.patches), 5)
        self.assertEqual(self.simulator.steps, 100)
        self.assertEqual(self.simulator.replicates, 0)
        self.assertEqual(self.simulator.dispersal_alpha, 0.1)
        self.assertEqual(self.simulator.area_exponent_b, 0.2)
        self.assertEqual(self.simulator.species_specific_constant_y, 0.3)
        self.assertEqual(self.simulator.species_specific_constant_u, 0.4)
        self.assertEqual(self.simulator.patch_area_effect_x, 0.5)
        self.assertEqual(self.simulator.done, False)