"""
Django Admin configuration
"""
from django.contrib import admin
from .models import Scenario
# Register your models here.

# Scenario upload field
admin.site.register(Scenario)
