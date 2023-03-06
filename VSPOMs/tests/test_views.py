from django.test import Client, TestCase
from VSPOMsApp.views import *

class ViewsTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "VSPOMs/index.html")

    def test_generate_patch_list_random(self):
        patch_list = generate_patch_list_random(30)
        self.assertEqual(len(patch_list), 30)

    def test_status_to_colour(self):
        statuses = [True, False, True]
        colours = status_to_colour(statuses)
        self.assertEqual(colours, ['green', 'red', 'green'])
        
    def test_index_data(self):
        response = self.client.get("/")
        self.assertContains(response, "graph1")
        self.assertContains(response, "graph2")
        self.assertContains(response, "graph3")
        self.assertContains(response, "graph4")
        self.assertContains(response, "map")