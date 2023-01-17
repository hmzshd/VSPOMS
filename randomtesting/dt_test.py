##deprecated

from simulator import  Simulator
from patch_generate import generate_patch_list_random

patch_list = generate_patch_list_random(15)
simulator = Simulator(patch_list)
event_list = []
for i in range(20):
    event_list.append(simulator.select_event())
print(event_list)
for i in event_list:
    patch = i.patch
    print(f"x: {patch.x_coord}, y: {patch.y_coord}")

