from simulator import Simulator
from simulator_testing import generate_patch_list_random

num_patches = 15
steps = 1000
reps = 5

patch_list = generate_patch_list_random(num_patches)
sim = Simulator(patch_list, steps, reps)

sim.simulate(debug=True)
