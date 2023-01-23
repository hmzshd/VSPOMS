"""Just testing the simulator."""

from patch_generate import generate_patch_list_random
from simulator import Simulator

patch_list = generate_patch_list_random(30)
spom_sim = Simulator(patch_list, 60, 5)
spom_sim.simulate()
spom_sim.print_frame()
print(spom_sim.get_turnovers())
print(type(spom_sim.get_data()))
