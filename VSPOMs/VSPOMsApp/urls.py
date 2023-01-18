from django.urls import path
from VSPOMsApp import views

app_name = 'VSPOMs'

urlpatterns = [
    path('graphs', views.graphs, name='graphs'),
    path('index', views.index, name='index'),
]
