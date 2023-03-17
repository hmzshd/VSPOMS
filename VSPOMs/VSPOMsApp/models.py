"""
Django models
"""
from django.db import models

class Scenario(models.Model):
    """
    Model for uploading scenario CSV files. Takes a name and a file to upload.
    """
    name = models.TextField()
    file = models.FileField(upload_to='')
