
# pylint: disable=no-member, too-many-locals
"""
Disables no-member and too-many-locals warnings.
"""
import os
import json
import random
import pandas as pd
import plotly.express as px

from bokeh.embed import components
from bokeh.models import CustomJS
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from bokeh.models.widgets import RadioButtonGroup
from bokeh.plotting import figure
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# necessary to wrap this in try except due to the location of manage.py
try:
    from simulator.patch import Patch
    from simulator.simulator import Simulator
    from simulator.parser import parse_csv
except ModuleNotFoundError:
    from ..simulator.patch import Patch
    from ..simulator.simulator import Simulator
    from ..simulator.parser import parse_csv


def generate_patch_list_random(num):
    """
    Generates a list of patches.
    The patches with random parameters  for [status, x, y, radius]

    Args:
        num (int): The number of patches to be generated

    Returns:
        patch_list (list): A list of the generated patches
    """
    patch_list = []
    for _ in range(num):
        patch_list.append(
            Patch(
                bool(random.randint(0, 1)),
                random.uniform(0, 25),
                random.uniform(0, 25),
                random.uniform(0, 5)
            )
        )
    return patch_list




def index(request):
    """
    Returns a request to serve index page.
    """

    # Prepare Data
    patch_list = parse_csv('static/data/demo.csv')[0]
    patches = pd.DataFrame.from_dict(patch_list)
    graph_df = pd.DataFrame(columns= ["time",
        "proportion occupied patches",
        "proportion occupied area",
        "extinction","step"])

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
            width=1000,
            height=600,
        )

        # attribute adjustments
        fig.update_traces(line_width=3)
        fig.update_layout(
            autosize=False,
            width=500,
            height=400,
        )
        graphs[graph] = fig.to_html(full_html=False)

    patch_map = {'map': ''}

    source = ColumnDataSource({
        'x': patches["x_coords"].values.tolist(),
        'y': patches["y_coords"].values.tolist(),
        'color': status_to_colour(patches["statuses"]),
        'size': patches["radiuses"].values.tolist()},
        name='patch_data_source'
    )
    max_radius = max(source.data['size'])
    plot = figure(
        tools=[]
    )
    plot.sizing_mode = "scale_both"

    size_source = ColumnDataSource(data={'size': []})

    renderer = plot.scatter(
        x="x",
        y="y",
        source=source,
        color='color',
        size="size",
        name="vspoms"
    )
    columns = [TableColumn(field='size', title='size')]
    table = DataTable(
        source=size_source,
        columns=columns,
        editable=True,
        height=200,
        visible=False
    )

    draw_tool = PointDrawTool(
        renderers=[renderer],
        empty_value=50 + max_radius//2
    )
    plot.add_tools(draw_tool)
    plot.toolbar.active_tap = draw_tool

    radio_button_group = RadioButtonGroup(
        labels=['Colonised', 'Extinct'],
        active=None,
        visible=False
    )

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
        let size_float = parseFloat(size_source.data.size[0])
        let is_valid = !isNaN(size_float);
        if (is_valid){
            source.data.size[index] = size_float;
        }
    }
    source.change.emit();
    """

    source.selected.js_on_change(
        'indices',
        CustomJS(
            args = {
                "source": source,
                "radio_button_group": radio_button_group,
                "size_source": size_source,
                "table": table
            },
            code=callback_select
        )
    )
    radio_button_group.js_on_event(
        "button_click",
        CustomJS(
            args = {
                "source": source,
                "radio_button_group": radio_button_group
            },
            code=callback_button
        )
    )
    size_source.js_on_change(
        'patching',
        CustomJS(
            args = {
                "source": source,
                "size_source": size_source,
                "table": table
            },
            code=callback_resize
        )
    )

    patch_map['map'] = plot
    patch_map['display'] = table
    patch_map['button'] = radio_button_group

    script, div = components(patch_map)

    # List all files in media folder for create page
    media_folder = os.path.join(settings.MEDIA_ROOT)
    media_files = os.listdir(media_folder)

    context_dict = {
        'script': script,
        'bokeh_div': div,
        'table': table,
        'graphs': graphs,
        'media_files': media_files
    }

    return render(request, 'VSPOMs/index.html', context=context_dict)


def status_to_colour(statuses):
    """
    Maps statuses to colours to display on frontend graphs.

    Args:
        statuses: A list of statuses

    Returns:
        :(string): Returns "green" or "red" depending on status
    """
    return ["green" if status else "red" for status in statuses]

def colour_to_status(colour):
    """
    Maps colours to statuses
    """
    return colour == "green"


def post_patches(request):
    """
    Catches request from ajax and runs the simulation with the data extracted from the client.

    Args:
        request: JSON request
    
    Returns:
        JsonResponses with either success or error message.
    """

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({"error": "error"}, status=400)
    
    data = json.loads(request.body)
    patch_data = data["bokeh"]
    patch_list = []
    for i in range(len(patch_data["x"])):
        patch_list.append(Patch(
            patch_data["x"][i],
            patch_data["y"][i],
            colour_to_status(patch_data["color"][i]),
            patch_data["size"][i]
        ))

    #Simulate
    simulation = Simulator(patch_list,
        dispersal_alpha=float(data["dispersal_kernel"]),
        area_exponent_b=float(data["connectivity"]),
        species_specific_constant_y=float(data["colonization_probability"]),
        species_specific_constant_u=float(data["patch_extinction_probability_u"]),
        patch_area_effect_x=float(data["patch_extinction_probability_x"]))
    simulation.simulate()

    # Graphs 
    graph_data = simulation.get_data()
    graph_df = pd.DataFrame()
    for i in range(len(graph_data.index)):
        dfa = graph_data.head(i).copy()
        dfa['step'] = i
        graph_df = pd.concat([graph_df, dfa])

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
        graphs[graph] = fig.to_json()

    return JsonResponse({"message": json.loads(graphs["graph1"])}, status=200)

        

def post_create(request):
    """
    Catches request from ajax and determines the requested action 
    then provides the appropriate patch data and settings

    Args:
        request: JSON request
            link: Either 'Nothing' or a file name under media

    Returns:
        JsonResponses with either the patch data and settings, or error message.
    """
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({"error": "error"}, status=400)
    
    data = json.loads(request.body)
    #Read Scenario
    if data != "Nothing":
        address = 'media/'+data
        patch_list,settings = parse_csv(address)

        patches = pd.DataFrame.from_dict(patch_list)
        random_patch_source = json.dumps({
            'x': patches["x_coords"].values.tolist(),
            'y': patches["y_coords"].values.tolist(),
            'color': status_to_colour(patches["statuses"]),
            'size': patches["radiuses"].values.tolist()}
        )

        parameters = json.dumps({
            "dispersal_kernel": settings["dispersal_alpha"],
            "connectivity": settings["area_exponent_b"],
            "colonization_probability": settings["species_specific_constant_y"],
            "patch_extinction_probability_u": settings["species_specific_constant_u"],
            "patch_extinction_probability_x": settings["patch_area_effect_x"],
            "rescue_effect": random.uniform(0, 10),
            "stochasticity": random.uniform(0, 10)
        })
        
        
    #Random Scenario
    else:
        patch_list = generate_patch_list_random(100)

        random_patch_source = json.dumps({
            'x': [patch.get_coords()[0] for patch in patch_list],
            'y': [patch.get_coords()[1] for patch in patch_list],
            'color': status_to_colour([patch.is_occupied() for patch in patch_list]),
            'size': [patch.get_area() for patch in patch_list]
            })
        
        parameters = json.dumps({
            "dispersal_kernel": random.uniform(0, 10),
            "connectivity": random.uniform(0, 10),
            "colonization_probability": random.uniform(0, 10),
            "patch_extinction_probability_u": random.uniform(0, 10),
            "patch_extinction_probability_x": random.uniform(0, 10),
            "rescue_effect": random.uniform(0, 10),
            "stochasticity": random.uniform(0, 10)
        })

    return JsonResponse(
        {"patch_source": json.loads(random_patch_source),
        "parameters": json.loads(parameters)
        }, 
        status=200
        )
        
