from django.test import Client, TestCase
import json
from VSPOMsApp.views import *

class ViewsTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "VSPOMs/index.html")

    def test_generate_patch_list_random(self):
        patch_list = generate_patch_list_random(30)
        self.assertEqual(len(patch_list), 30)

    def test_generate_patch_list_randomness(self):
        patch_list = generate_patch_list_random(5)
        patch_list2 = generate_patch_list_random(5)
        self.assertNotEqual(patch_list, patch_list2)
    
    def test_generate_patch_list_properties(self):
        patch_list = generate_patch_list_random(5)
        for patch in patch_list:
            self.assertIsInstance(patch.status, bool)
            self.assertGreaterEqual(patch.x_coord, 0)
            self.assertLessEqual(patch.x_coord, 25)
            self.assertGreaterEqual(patch.y_coord, 0)
            self.assertLessEqual(patch.y_coord, 25)
            self.assertGreaterEqual(patch.radius, 0)
            self.assertLessEqual(patch.radius, 5)

    def test_status_to_colour(self):
        statuses = [True, False, True]
        colours = status_to_colour(statuses)
        self.assertEqual(colours, ['green', 'red', 'green'])
        
    def test_index_graphs(self):
        response = self.client.get("/")
        self.assertContains(response, "graph1")
        self.assertContains(response, "graph2")
        self.assertContains(response, "graph3")
        self.assertContains(response, "graph4")
    
    def test_index_maps(self):
        response = self.client.get("/")
        self.assertContains(response, "map")

    def test_index_table(self):
        response = self.client.get("/")
        self.assertContains(response, "table")

    def test_index_patch_data_source(self):
        response = self.client.get("/")
        self.assertContains(response, "patch_data_source")

    def test_index_size_source(self):
        response = self.client.get("/")
        self.assertContains(response, "size_source")

    def test_index_patches(self):
        response = self.client.get("/")
        self.assertContains(response, "patches")

    def test_index_view_has_renderer(self):
        response = self.client.get("/")
        self.assertContains(response, "renderer")

    def test_index_plot(self):
        response = self.client.get("/")
        self.assertContains(response, "plot")

    def setUp(self):
        self.client = Client()

    def test_post_patches(self):
        # create JSON data for the request
        # WIP
        request_data = {
            "bokeh": {
                "x": [1, 2, 3],
                "y": [4, 5, 6],
                "color": ["red", "green", "blue"],
                "size": [1.0, 2.0, 3.0]
            },
            "dispersal_kernel": 0.5,
            "connectivity": 0.6,
            "colonization_probability": 0.7,
            "patch_extinction_probability_u": 0.8,
            "patch_extinction_probability_x": 0.9
        }