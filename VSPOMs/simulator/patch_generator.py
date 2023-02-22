"""Just testing the simulator."""

from simulator import Simulator

from patch import Patch
import random


def generate_patch_list_random(num):
    patch_list = []
    for i in range(num):
        patch_list.append(Patch(bool(random.randint(0, 1)), random.uniform(0, 25), random.uniform(0, 25), random.uniform(0, 5)))
    return patch_list

# patch_list = generate_patch_list_random(30)
# spom_sim = Simulator(patch_list, 60, 5)
# spom_sim.simulate()
# spom_sim.print_frame()
# print(spom_sim.get_turnovers())
# print(type(spom_sim.get_data()))
