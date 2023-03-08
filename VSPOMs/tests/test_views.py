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