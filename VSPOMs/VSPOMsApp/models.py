"""
Django models
"""
from django.db import models

class Scenario(models.Model):
    """
    Model for uploading scenario CSV files. Takes a file to upload.
    """
    file = models.FileField(upload_to='')
