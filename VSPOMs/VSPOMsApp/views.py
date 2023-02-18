import random

import pandas as pd
import plotly.express as px
from bokeh.embed import components
from bokeh.models import CustomJS
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from bokeh.models.widgets import RadioButtonGroup
from bokeh.plotting import figure
from bokeh.sampledata.stocks import MSFT
from django.shortcuts import render
from django.http import JsonResponse

from simulator.patch import Patch
from simulator.simulator import Simulator


def generate_patch_list_random(num):
    patch_list = []
    for i in range(num):
        patch_list.append(
            Patch(
                bool(random.randint(0, 1)),
                random.uniform(0, 25),
                random.uniform(0, 25),
                random.uniform(0, 5))
            )
    return patch_list


def status_to_colour(statuses):
    return ["green" if status else "red" for status in statuses]


def index(request):
    # Prepare Data
    map_size = 30
    patch_list = generate_patch_list_random(map_size)
    spom_sim = Simulator(patch_list, 60, 5)
    spom_sim.simulate()
    patches = pd.DataFrame.from_dict(spom_sim.get_turnovers())

    graph_data = spom_sim.get_data().loc[0, :]
    graph_df = pd.DataFrame()
    for i in range(len(graph_data.index)):
        dfa = graph_data.head(i).copy()
        dfa['step'] = i
        graph_df = pd.concat([graph_df, dfa])

    msft_df = pd.DataFrame(MSFT)
    msft_df["date"] = pd.to_datetime(msft_df["date"])

    graphs = {
        'graph1': '',
        'graph2': '',
        'graph3': '',
        'graph4': ''
    }
    graph_labels = [
        "time",
        "proportion occupied patches",
        "proportion occupied area",
        "extinction"
    ]

    for idx, graph in enumerate(graphs.keys()):

        fig = px.line(
            graph_df,
            x='time',
            y=graph_labels[idx],
            animation_frame='step',
            # template = 'plotly_dark',
            width=1000,
            height=600,
        )

        # attribute adjustments
        fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True

        fig.update_traces(line_width=3)

        fig.update_layout(
            autosize=False,
            width=500,
            height=400,
        )
        graphs[graph] = fig.to_html(full_html=False)

    patch_map = {'map': ''}

    plot = figure(
        x_range=(-map_size // 10, map_size * 1.1),
        y_range=(0, map_size * 1.1),
        tools=[],
        title='Point Draw Tool'
    )

    source = ColumnDataSource({
        'x': patches["x_coords"],
        'y': patches["y_coords"],
        'color': status_to_colour(patches["statuses"]),
        ## this needs to be changed into actual size rather than using the x right now!
        'size': patches["x_coords"]},
        name='patch_data_source'
    )

    size_source = ColumnDataSource(data={'size': []})

    renderer = plot.scatter(x="x", y="y", source=source, color='color', size="size")
    columns = [TableColumn(field='size', title='size')]
    table = DataTable(source=size_source, columns=columns, editable=True, height=200, visible=False)

    draw_tool = PointDrawTool(renderers=[renderer], empty_value=50)
    plot.add_tools(draw_tool)
    plot.toolbar.active_tap = draw_tool

    radio_button_group = RadioButtonGroup(labels=['Colonised', 'Extinct'], active=None, visible=False)

    callback_select = """
    if(source.selected.indices.length > 0){
        radio_button_group.visible = true;
        table.visible = true;
        if (source.data.color[source.selected.indices[0]] == 'green'){
            radio_button_group.active = 0;
        }
        if (source.data.color[source.selected.indices[0]] == 'red'){
            radio_button_group.active = 1;
        }
        const size = []
        for(let i = 0; i < source.selected.indices.length; i++) {
            size[i] = source.data.size[source.selected.indices[i]];
        }
        size_source.data.size = size;
    }
    if (source.selected.indices.length == 0){
        radio_button_group.visible = false;  
        radio_button_group.active = null;
        size_source.data.size = [];
        table.visible = false;
         
    }
    source.change.emit();
    size_source.change.emit();
    """

    callback_button = """
    if(radio_button_group.active == 0){
        for(const index of source.selected.indices) {
            source.data.color[index] = 'green';
        }
    }
    if(radio_button_group.active == 1){
        for(const index of source.selected.indices) {
            source.data.color[index] = 'red';
        }
    }
    source.change.emit();
    """

    callback_resize = """
    for(const index of source.selected.indices) {
        source.data.size[index] = size_source.data.size[0];
    }
    source.change.emit();
    """

    source.selected.js_on_change(
        'indices',
        CustomJS(
            args=dict(
                source=source,
                radio_button_group=radio_button_group,
                size_source=size_source,
                table=table
            ),
            code=callback_select
        )
    )
    radio_button_group.js_on_event(
        "button_click",
        CustomJS(
            args=dict(
                source=source,
                radio_button_group=radio_button_group
            ),
            code=callback_button
        )
    )
    size_source.js_on_change(
        'patching',
        CustomJS(
            args=dict(
                source=source,
                size_source=size_source,
                table=table
            ),
            code=callback_resize
        )
    )

    patch_map['map'] = plot
    patch_map['display'] = table
    patch_map['button'] = radio_button_group


    script, div = components(patch_map)

    context_dict = {
        'script': script,
        'bokeh_div': div,
        'table': table,
        'graphs': graphs,
    }


    return render(request, 'VSPOMs/index.html', context=context_dict)

def colourToStatus(colours):
    return [True if "green" else False for colour in colours]

def postPatches(request):
    if (request.is_ajax and request.method == "POST"):
        source = request.POST
        data = source.data
        patch_data = dict(
            x=data["x"],
            y=data["y"],
            size=data["size"],
            status=colourToStatus(data["color"])
        )
        patch_list = []
        for item in patch_data:
            patch_list.add( Patch(
                item["x"],
                item["y"],
                item["status"],
                item["size"]
            ))
        
        simulation = Simulator(patch_list,60,5)
        simulation.simulate()
        
        return JsonResponse({"message": "ALL GOOD"}, status=200)
    else:
        return JsonResponse({"error": "error"}, status=400)
    
    return JsonResponse({"error": "error"}, status=400)

