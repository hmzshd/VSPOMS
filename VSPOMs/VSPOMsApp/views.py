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
