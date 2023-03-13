"""
URL patterns for VSPOMs app
"""
from django.urls import path
from VSPOMsApp import views

APP_NAME = 'VSPOMs'

urlpatterns = [
    path('index', views.index, name='index'),
]
