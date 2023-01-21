"""Just testing the simulator."""

from patch_generate import generate_patch_list_random
from simulator import Simulator

patch_list = generate_patch_list_random(30)
spom_sim = Simulator(patch_list)
spom_sim.simulate(100, 5)
