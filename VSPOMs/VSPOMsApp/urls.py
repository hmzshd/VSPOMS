from django.urls import path
from VSPOMsApp import views

app_name = 'VSPOMs'

urlpatterns = [
    path('', views.simulate, name='simulate'),
    path('create', views.create, name='create'),
    path('graphs', views.graphs, name='graphs'),
    path('settings', views.settings, name='settings'),
    path('index', views.index, name='index'),
]
