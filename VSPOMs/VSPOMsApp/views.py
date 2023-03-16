# pylint: disable=no-member, too-many-locals
"""
Django views for VSPOMs
"""
import math
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

# pylint: disable=line-too-long

# necessary to wrap this in try except due to the location of manage.py
try:
    from simulator.patch import Patch
    from simulator.simulator import Simulator
    from simulator.parser import parse_csv
except ModuleNotFoundError:
    from ..simulator.patch import Patch
    from ..simulator.simulator import Simulator
    from ..simulator.parser import parse_csv


def index(request):
    """
    Returns a request to serve index page.
    """

    # Prepare Data
    patch_list = parse_csv('media/demo.csv')[0]
    scenario_settings = parse_csv('media/demo.csv')[1]
    scaling_factor = parse_csv('media/demo.csv')[2]
    patches = pd.DataFrame.from_dict(patch_list)
    graph_df = pd.DataFrame(columns=[
        "time",
        "proportion occupied patches",
        "proportion occupied area",
        "extinction",
        "step"
    ])

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

        # Attribute adjustments
        fig.update_traces(line_width=1)
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
        'size': patches["radiuses"].values.tolist(),
        'scaling': scale_per_patch(patches["radiuses"], scaling_factor)},
        name='patch_data_source'
    )
    max_radius = max(source.data['size'])
    # max_diameter = max_radius + min(source.data['x']) / 500
    plot = figure(
        # x_range=((min(source.data['x']) - max_diameter), (max(source.data['x']) + max_diameter)),
        # y_range=((min(source.data['y']) - max_diameter), (max(source.data['y']) + max_diameter)),
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
    columns = [TableColumn(field='size', title='Radius')]
    table = DataTable(
        source=size_source,
        columns=columns,
        editable=True,
        height=200,
        visible=False
    )

    draw_tool = PointDrawTool(
        renderers=[renderer],
        empty_value=50 + max_radius // 2
    )
    plot.add_tools(draw_tool)
    plot.toolbar.active_tap = draw_tool

    radio_button_group = RadioButtonGroup(
        labels=['Colonised', 'Extinct'],
        active=None,
        visible=False
    )

    # Custom JS callbacks
    callback_select = """
    if(source.selected.indices.length > 0) {
        radio_button_group.visible = true;
        table.visible = true;
        if (source.data.color[source.selected.indices[0]] == 'green') {
            radio_button_group.active = 0;
        }
        if (source.data.color[source.selected.indices[0]] == 'red') {
            radio_button_group.active = 1;
        }
        const size = []
        for(let i=0;i<source.selected.indices.length;i++) {
            size[i] = source.data.size[source.selected.indices[i]];
        }
        size_source.data.size = size;
    }
    if (source.selected.indices.length == 0) {
        radio_button_group.visible = false;  
        radio_button_group.active = null;
        size_source.data.size = [];
        table.visible = false;
    }
    source.change.emit();
    size_source.change.emit();
    """

    callback_button = """
    if(radio_button_group.active == 0) {
        for(const index of source.selected.indices) {
            source.data.color[index] = 'green';
        }
    }
    if(radio_button_group.active == 1) {
        for(const index of source.selected.indices) {
            source.data.color[index] = 'red';
        }
    }
    source.change.emit();
    """

    callback_resize = """
    for(const index of source.selected.indices) {
        let size_float = parseFloat(size_source.data.size[0]);
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
            args={
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
            args={
                "source": source,
                "radio_button_group": radio_button_group
            },
            code=callback_button
        )
    )
    size_source.js_on_change(
        'patching',
        CustomJS(
            args={
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
        'media_files': media_files,
        'scenario_settings' : scenario_settings
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


def scale_per_patch(sizes, scale):
    """
    Creates a list of how much each patch was scaled by, stored alongside it in a ColumnDataSource.

    Args:
        sizes: A list of sizes
        scale: The factor by which to scale by

    Returns:
        :(float): Returns the scaling aplied
    """
    return [scale for _ in sizes]


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
            math.pi * ((patch_data["size"][i]/patch_data["scaling"][i]) ** 2)
        ))

    print(patch_data)

    # Run simulation
    simulation = Simulator(patch_list,
                           species_specific_dispersal_constant=float(data["species_specific_dispersal_constant"]),
                           area_exponent_connectivity_b=float(data["area_exponent_connectivity_b"]),
                           species_specific_constant_colonisation_y=float(data["species_specific_constant_colonisation_y"]),
                           species_specific_extinction_constant_u=float(data["species_specific_extinction_constant_u"]),
                           patch_area_effect_extinction_x=float(data["patch_area_effect_extinction_x"]),
                           steps=int(data["steps"]),
                           replicates=int(data["replicates"])
                           )
    simulation.simulate()

    # Graphs
    graph_data = simulation.get_data()
    graph_df = pd.DataFrame(graph_data)

    graph_df = graph_df.reset_index()

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
            color='replicates',
            width=1000,
            height=600,
        )

        # Attribute adjustments
        fig.update_traces(line_width=1)
        fig.update_layout(
            autosize=False,
            width=500,
            height=400,
        )
        graphs[graph] = fig.to_json()
    turnovers = json.dumps(simulation.get_turnovers())
    replicates = json.dumps(simulation.replicates + 1)

    return JsonResponse({
        "graph1": json.loads(graphs["graph1"]),
        "graph2": json.loads(graphs["graph2"]),
        "graph3": json.loads(graphs["graph3"]),
        "graph4": json.loads(graphs["graph4"]),
        "turnovers": json.loads(turnovers),
        "replicates": json.loads(replicates)
    }, status=200)


def generate_patch_list_random(num, min_x, max_x, min_y, max_y, min_area, max_area):
    """
    Generates a list of patches.
    The patches with random parameters  for [status, x, y, radius]

    Args:
        num (int): The number of patches to be generated
        min_x (int): Min value for x axis
        max_x (int): Max value for x axis
        min_y (int): Min value for y axis
        max_y (int): Max value for y axis
        min_area (int): Min value for patch area
        max_area (int): Max value for patch area

    Returns:
        patch_list (list): A list of the generated patches
    """
    patch_list = []
    for _ in range(num):
        patch_list.append(
            Patch(
                bool(random.randint(0, 1)),
                random.uniform(min_x, max_x),
                random.uniform(min_y, max_y),
                random.uniform(min_area, max_area)
            )
        )
    return patch_list


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

    # Read Scenario
    if data["command"] == "load":
        address = 'media/' + data["address"]
        scaling = data["scaling"]
        try:
            parsed_file = parse_csv(address, scaling)
            patch_list = parsed_file[0]
            scenario_settings = parsed_file[1]
            scaling_factor = parsed_file[2]
        except (ValueError, UnicodeDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=500)

        patches = pd.DataFrame.from_dict(patch_list)
        random_patch_source = json.dumps({
            'x': patches["x_coords"].values.tolist(),
            'y': patches["y_coords"].values.tolist(),
            'color': status_to_colour(patches["statuses"]),
            'size': patches["radiuses"].values.tolist(),
            'scaling': scale_per_patch(patches["radiuses"], scaling_factor)}
        )
        print(patches["x_coords"])

        parameters = json.dumps({
            "species_specific_dispersal_constant": scenario_settings["species_specific_dispersal_constant"],
            "area_exponent_connectivity_b": scenario_settings["area_exponent_connectivity_b"],
            "species_specific_constant_colonisation_y": scenario_settings["species_specific_constant_colonisation_y"],
            "species_specific_extinction_constant_u": scenario_settings["species_specific_extinction_constant_u"],
            "patch_area_effect_extinction_x": scenario_settings["patch_area_effect_extinction_x"],
            "rescue_effect": random.uniform(0, 10),
            "stochasticity": random.uniform(0, 10)
        })


    # Random Scenario
    elif data["command"] == "random":
        fields = data["fields"]
        patch_list = generate_patch_list_random(
            fields["num"],
            fields["min_x"],
            fields["max_x"],
            fields["min_y"],
            fields["max_y"],
            fields["min_area"],
            fields["max_area"]
        )

        random_patch_source = json.dumps({
            'x': [patch.get_coords()[0] for patch in patch_list],
            'y': [patch.get_coords()[1] for patch in patch_list],
            'color': status_to_colour([patch.is_occupied() for patch in patch_list]),
            'size': [patch.get_area() for patch in patch_list],
            'scaling': [1 for _ in patch_list]
        })

        # Calculate scenario parameters
        param_u = ((fields["min_area"] + fields["max_area"]) / 2) / 10
        param_a = (((fields["max_x"] - fields["min_x"]) + (fields["max_y"] - fields["min_y"])) / 40) / 50
        param_x = 1
        param_b = 1
        param_y = 3  # not sure if this is suitable

        parameters = json.dumps({
            "species_specific_dispersal_constant": param_a,  # a
            "area_exponent_connectivity_b": param_b,  # b
            "species_specific_constant_colonisation_y": param_y,  # y
            "species_specific_extinction_constant_u": param_u,  # u
            "patch_area_effect_extinction_x": param_x,  # x
            # "rescue_effect": 0,
            # "stochasticity": 0
        })

    return JsonResponse({
            "patch_source": json.loads(random_patch_source),
            "parameters": json.loads(parameters)
        },
        status=200
    )
