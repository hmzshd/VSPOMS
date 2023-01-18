from bokeh.models import DataTable, ColumnDataSource
import numpy as np
from simulator import Simulator
from patch_generate import generate_patch_list_random

patch_list = generate_patch_list_random(15)
simulator = Simulator(patch_list, 50, 5)
event_list = []
for i in range(20):
    event_list.append(simulator.select_event())


# print(event_list)

def event_list_to_datatable(event_list):
    x_coords = []
    y_coords = []
    statuses = []
    for event in event_list:
        current_patch = event.patch
        x_coords.append(current_patch.x_coord)
        y_coords.append(current_patch.y_coord)
        statuses.append(current_patch.statuses)

    dict_source = {"x_coords": x_coords, "y_coords": y_coords, "statuses": statuses}
    source = ColumnDataSource(dict_source)
    print(source)


event_list_to_datatable(event_list)
