from django.shortcuts import render
from django.http import HttpResponse
from bokeh.embed import components
from bokeh.sampledata.stocks import MSFT
from bokeh.models import Button, Slider, DatetimeTickFormatter, Legend
from bokeh.models.ranges import FactorRange
from bokeh.io import curdoc
import time
from functools import partial
import pandas as pd
from bokeh.plotting import figure, output_file, show, Column
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource

from simulator.simulator import Simulator
from simulator.patch import Patch
import random

def generate_patch_list_random(num):
    patch_list = []
    for i in range(num):
        patch_list.append(Patch(bool(random.randint(0, 1)), random.uniform(0, 25), random.uniform(0, 25), random.uniform(0, 5)))
    return patch_list

def status_to_colour(statuses):
    return ["green" if status else "red" for status in statuses]


def index(request):
    ## Prepare Data
    map_size = 30
    patch_list = generate_patch_list_random(map_size)
    spom_sim = Simulator(patch_list, 60, 5)
    spom_sim.simulate()
    patches = spom_sim.get_turnovers()
    
    msft_df = pd.DataFrame(MSFT)
    msft_df["date"] = pd.to_datetime(msft_df["date"])

    graphs = {'graph1':'','graph2':'','graph3':'','graph4':''}
    for graph in graphs:
        days = 90

        graphs[graph] = figure(x_axis_type="datetime", width=500, height=500,
                     title = "Microsoft Candlestick Chart")

        line1 = graphs[graph].line(x="date", y="open", color="dodgerblue", source=msft_df[:days])
        line2 = graphs[graph].line(x="date", y="high", color="lime", source=msft_df[:days])
        line3 = graphs[graph].line(x="date", y="low", color="tomato", source=msft_df[:days])
        line4 = graphs[graph].line(x="date", y="close", color="orange", source=msft_df[:days])

        graphs[graph].xaxis.axis_label="Date"
        graphs[graph].yaxis.axis_label="Price ($)"

        graphs[graph].xaxis.formatter = DatetimeTickFormatter(days="%m-%d-%Y")

        legend = Legend(items=[
            ("Open",   [line1]),
            ("High",   [line2]),
            ("Low",   [line3]),
            ("Close",   [line4]),
        ], location=(0, 100))

        graphs[graph].add_layout(legend, 'right')


    p = figure(x_range=(-map_size//10, map_size*1.1), y_range=(0, map_size*1.1), tools=[],
           title='Point Draw Tool')

    source = ColumnDataSource({
    'x': patches["x_coords"], 'y': patches["y_coords"], 'color': status_to_colour(patches["statuses"]), 'size':patches["x_coords"]
    })

    renderer = p.scatter(x="x", y="y", source=source,color='color', size="size")
    columns = [TableColumn(field="x", title="x"),
               TableColumn(field="y", title="y"),
               TableColumn(field='color', title='color'),
               TableColumn(field='size', title='size')
              ]
    table = DataTable(source=source, columns=columns, editable=True, height=200)

    draw_tool = PointDrawTool(renderers=[renderer], empty_value=50)
    p.add_tools(draw_tool)
    p.toolbar.active_tap = draw_tool

    graphs['map'] = p

    script, div = components(graphs)

    context_dict = {}
    context_dict['script'] = script
    context_dict['bokeh_div'] = div
    context_dict['table'] = table

    return render(request, 'VSPOMs/index.html', context=context_dict)

def graphs(request):

    ## Prepare Data
    msft_df = pd.DataFrame(MSFT)
    msft_df["date"] = pd.to_datetime(msft_df["date"])

    graphs = {'graph1':'','graph2':'','graph3':'','graph4':''}
    for graph in graphs:
        days = 90

        graphs[graph] = figure(x_axis_type="datetime", width=500, height=500,
                     title = "Microsoft Candlestick Chart")

        line1 = graphs[graph].line(x="date", y="open", color="dodgerblue", source=msft_df[:days])
        line2 = graphs[graph].line(x="date", y="high", color="lime", source=msft_df[:days])
        line3 = graphs[graph].line(x="date", y="low", color="tomato", source=msft_df[:days])
        line4 = graphs[graph].line(x="date", y="close", color="orange", source=msft_df[:days])

        graphs[graph].xaxis.axis_label="Date"
        graphs[graph].yaxis.axis_label="Price ($)"

        graphs[graph].xaxis.formatter = DatetimeTickFormatter(days="%m-%d-%Y")

        legend = Legend(items=[
            ("Open",   [line1]),
            ("High",   [line2]),
            ("Low",   [line3]),
            ("Close",   [line4]),
        ], location=(0, 100))

        graphs[graph].add_layout(legend, 'right')


    p = figure(x_range=(0, 10), y_range=(0, 10), tools=[],
           title='Point Draw Tool')

    source = ColumnDataSource({
    'x': [1, 5, 9], 'y': [1, 5, 9], 'color': ['red', 'green', 'yellow'],'size':[20,10,40]
    })

    renderer = p.scatter(x='x', y='y', source=source, color='color', size='size')
    columns = [TableColumn(field="x", title="x"),
               TableColumn(field="y", title="y"),
               TableColumn(field='color', title='color'),
               TableColumn(field='size', title='size')
              ]
    table = DataTable(source=source, columns=columns, editable=True, height=200)

    draw_tool = PointDrawTool(renderers=[renderer], empty_value=50)
    p.add_tools(draw_tool)
    p.toolbar.active_tap = draw_tool

    graphs['map'] = p

    script, div = components(graphs)

    context_dict = {}
    context_dict['script'] = script
    context_dict['bokeh_div'] = div
    context_dict['table'] = table

    return render(request, 'VSPOMs/graphs.html', context=context_dict)