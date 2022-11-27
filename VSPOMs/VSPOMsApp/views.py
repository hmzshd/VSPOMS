from django.shortcuts import render
from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.embed import components

def create(request):
    context_dict = {}
    return render(request, 'VSPOMs/create.html', context=context_dict)

def graphs(request):
    graph_size = 500 
    graphs = {'graph1':'','graph2':'','graph3':'','graph4':''}
    colours = {'graph1':'green','graph2':'red','graph3':'blue','graph4':'green'}
    for graph in graphs:
        graphs[graph] = figure(width=graph_size,height=graph_size,title=graph,x_axis_label='time',y_axis_label='y')
        graphs[graph].line([1,2,3,4,5,6,7,8],[6,2,9,14,16,19,11,16], legend_label="Something", line_width=1,color=colours[graph])
    script, div = components(graphs)  

    context_dict = {}
    context_dict['script'] = script
    context_dict['bokeh_div'] = div

    return render(request, 'VSPOMs/graphs.html', context=context_dict)

def settings(request):
    context_dict = {}
    return render(request, 'VSPOMs/settings.html', context=context_dict)

def simulate(request):
    context_dict = {}
    return render(request, 'VSPOMs/simulate.html', context=context_dict)
