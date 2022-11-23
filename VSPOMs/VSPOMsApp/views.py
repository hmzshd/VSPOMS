from django.shortcuts import render
from django.http import HttpResponse

def create(request):
    context_dict = {}
    return render(request, 'VSPOMs/create.html', context=context_dict)

def graphs(request):
    context_dict = {}
    return render(request, 'VSPOMs/graphs.html', context=context_dict)

def settings(request):
    context_dict = {}
    return render(request, 'VSPOMs/settings.html', context=context_dict)

def simulate(request):
    context_dict = {}
    return render(request, 'VSPOMs/simulate.html', context=context_dict)
