"""
Automated tests for patch.py
"""
from django.test import TestCase
from simulator.patch import Patch

class PatchTestCase(TestCase):
    """expands upon the django TestCase to see if patch
    is being properly initialised"""
    def test_patch_init(self):
        """
        Create and test a patch
        """
        x_coord = 10.0
        y_coord = 20.0
        area = 50.0
        status = True
        patch = Patch(status, x_coord, y_coord, area)
        self.assertEqual(patch.x_coord, x_coord)
        self.assertEqual(patch.y_coord, y_coord)
        self.assertEqual(patch.area, area)
        self.assertEqual(patch.status, status)
        self.assertEqual(patch.events, [])
        self.assertEqual(patch.colonisation_value, 1.0)
        self.assertEqual(patch.extinction_value, 1.0)
