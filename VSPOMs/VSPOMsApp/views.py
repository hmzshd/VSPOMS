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
import numpy as np
import plotly.express as px
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

    # input data and start of first graph template
    dfi = px.data.stocks().head(50)
    dfi['date'] = pd.to_datetime(dfi['date'])
    start = 12
    obs = len(dfi)

    # new datastructure for animation
    df = pd.DataFrame()  # container for df with new datastructure
    for i in np.arange(start, obs):
        dfa = dfi.head(i).copy()
        dfa['ix'] = i
        df = pd.concat([df, dfa])

    # plotly figure
    fig1 = px.line(df, x='date', y=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
                  animation_frame='ix',
                  # template = 'plotly_dark',
                  width=1000, height=600)

    # attribute adjusments
    fig1.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True

    fig1.update_layout(
        autosize=False,
        width=500,
        height=400,
    )
    graph1 = fig1.to_html(full_html=False)

    # input data and start of third graph template
    dfi = px.data.stocks().head(50)
    dfi['date'] = pd.to_datetime(dfi['date'])
    start = 12
    obs = len(dfi)

    # new datastructure for animation
    df = pd.DataFrame()  # container for df with new datastructure
    for i in np.arange(start, obs):
        dfa = dfi.head(i).copy()
        dfa['ix'] = i
        df = pd.concat([df, dfa])

    # plotly figure
    fig2 = px.line(df, x='date', y=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
                  animation_frame='ix',
                  # template = 'plotly_dark',
                  width=1000, height=600)

    # attribute adjusments
    fig2.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True

    fig2.update_layout(
        autosize=False,
        width=500,
        height=400,
    )
    graph2 = fig2.to_html(full_html=False)

    # input data and start of first graph template
    dfi = px.data.stocks().head(50)
    dfi['date'] = pd.to_datetime(dfi['date'])
    start = 12
    obs = len(dfi)

    # new datastructure for animation
    df = pd.DataFrame()  # container for df with new datastructure
    for i in np.arange(start, obs):
        dfa = dfi.head(i).copy()
        dfa['ix'] = i
        df = pd.concat([df, dfa])

    # plotly figure
    fig3 = px.line(df, x='date', y=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
                  animation_frame='ix',
                  # template = 'plotly_dark',
                  width=1000, height=600)

    # attribute adjusments
    fig3.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True

    fig3.update_layout(
        autosize=False,
        width=500,
        height=400,
    )
    graph3 = fig3.to_html(full_html=False)

    # input data and start of fourth graph template
    dfi = px.data.stocks().head(50)
    dfi['date'] = pd.to_datetime(dfi['date'])
    start = 12
    obs = len(dfi)

    # new datastructure for animation
    df = pd.DataFrame()  # container for df with new datastructure
    for i in np.arange(start, obs):
        dfa = dfi.head(i).copy()
        dfa['ix'] = i
        df = pd.concat([df, dfa])

    # plotly figure
    fig4 = px.line(df, x='date', y=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
                  animation_frame='ix',
                  # template = 'plotly_dark',
                  width=1000, height=600)

    # attribute adjusments
    fig4.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True

    fig4.update_layout(
        autosize=False,
        width=500,
        height=400,
    )
    graph4 = fig4.to_html(full_html=False)

    graphs = {'map':''}

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
    context_dict ['graphs'] = {'graph1': graph1, 'graph2': graph2, 'graph3': graph3, 'graph4': graph4}

    return render(request, 'VSPOMs/index.html', context=context_dict)

def graphs(request):
    import pandas as pd
    import numpy as np
    import plotly.express as px

    # input data
    dfi = px.data.stocks().head(50)
    dfi['date'] = pd.to_datetime(dfi['date'])
    start = 12
    obs = len(dfi)

    # new datastructure for animation
    df = pd.DataFrame()  # container for df with new datastructure
    for i in np.arange(start, obs):
        dfa = dfi.head(i).copy()
        dfa['ix'] = i
        df = pd.concat([df, dfa])

    # plotly figure
    fig = px.line(df, x='date', y=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
                  animation_frame='ix',
                  # template = 'plotly_dark',
                  width=1000, height=600)

    # attribute adjusments
    fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True

    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    context_dict = {'graph': graph}

    return render(request, 'VSPOMs/graphs.html', context=context_dict)
