from django.urls import path
from VSPOMsApp import views

app_name = 'VSPOMs'

urlpatterns = [
    path('', views.simulate, name='simulate'),
    path('/graphs/', views.graphs, name='graphs'),
    path('/create/', views.graphs, name='create'),
    path('/settings/', views.graphs, name='settings'),
]
