# pylint: disable=C0116
"""
Automated tests for views.py
"""
import json
from django.test import TestCase
from VSPOMsApp.views import status_to_colour, generate_patch_list_random, Patch

class ViewsTestCase(TestCase):
    """
    Expands upon django TestCase, tests index, 
    test_generate_patch_list_random, test_status_to_colour
    """

    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "VSPOMs/index.html")

    def test_generate_patch_list_random(self):
        num = 10
        min_x = 0
        max_x = 100
        min_y = 0
        max_y = 100
        min_area = 25
        max_area = 100

        patch_list = generate_patch_list_random(
            num,
            min_x,
            max_x,
            min_y,
            max_y,
            min_area,
            max_area
        )

        self.assertEqual(len(patch_list), num)

        for patch in patch_list:
            self.assertIsInstance(patch, Patch)
            self.assertGreaterEqual(patch.x_coord, min_x)
            self.assertLessEqual(patch.x_coord, max_x)
            self.assertGreaterEqual(patch.y_coord, min_y)
            self.assertLessEqual(patch.y_coord, max_y)
            self.assertGreaterEqual(patch.area, min_area)
            self.assertLessEqual(patch.area, max_area)

    def test_status_to_colour(self):
        statuses = [True, False, True]
        colours = status_to_colour(statuses)
        self.assertEqual(colours, ["green", "red", "green"])

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

    def test_post_patches(self):
        # create JSON data for the request
        request_data = {
            "bokeh": {
                "x": [1, 2, 3],
                "y": [4, 5, 6],
                "color": ["red", "green", "blue"],
                "size": [1.0, 2.0, 3.0],
                "scaling": [1, 2, 3]
            },
            "dispersal_kernel": 0.5,
            "connectivity": 0.6,
            "colonization_probability": 0.7,
            "patch_extinction_probability_u": 0.8,
            "patch_extinction_probability_x": 0.9,
            "steps": 100,
            "replicates": 1
        }

        # send the POST request with the JSON data
        response = self.client.post(
            '/post_patches',
            data=json.dumps(request_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # check that the response contains the expected JSON data
        self.assertEqual(response.status_code, 200)
        self.assertIn("graph1", response.json())
        self.assertIn("graph2", response.json())
        self.assertIn("graph3", response.json())
        self.assertIn("graph4", response.json())
        self.assertIn("turnovers", response.json())
        self.assertIn("replicates", response.json())

    def test_load_command(self):
        # prepare file to be loaded
        load = {
            'command': 'load',
            'address': 'bigdan.csv'
        }

        # make POST request
        response = self.client.post(
            '/post_create', 
            data=json.dumps(load), 
            content_type='application/json', 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # check response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn("patch_source", response_data)
        self.assertIn("parameters", response_data)
        self.assertIsNotNone(response_data["patch_source"])
        self.assertIsNotNone(response_data["parameters"])
    