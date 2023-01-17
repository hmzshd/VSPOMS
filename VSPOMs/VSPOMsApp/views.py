from django.shortcuts import render
from django.http import HttpResponse
from bokeh.embed import components
from bokeh.sampledata.stocks import MSFT
from bokeh.models import Button, Slider, DatetimeTickFormatter, Legend
from bokeh.plotting import figure, column, row
from bokeh.models.ranges import FactorRange
from bokeh.io import curdoc
from bokeh.client import pull_session
from bokeh.embed import server_session
import time
from functools import partial
import pandas as pd

def create(request):
    context_dict = {}
    return render(request, 'VSPOMs/create.html', context=context_dict)

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

    script, div = components(graphs)

    context_dict = {}
    context_dict['script'] = script
    context_dict['bokeh_div'] = div

    return render(request, 'VSPOMs/graphs.html', context=context_dict)

def settings(request):
    context_dict = {}
    return render(request, 'VSPOMs/settings.html', context=context_dict)

def simulate(request):
    from bokeh.plotting import figure, output_file, show, Column
    from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource

    output_file("tools_point_draw.html")

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
    script, div = components(p) 

    context_dict = {}
    context_dict['script'] = script
    context_dict['bokeh_div'] = div
    context_dict['table'] = table
    return render(request, 'VSPOMs/simulate.html', context=context_dict)
