import time
from simulator import Simulator
from simulator_testing import generate_patch_list_random

n = 500

patch_list = generate_patch_list_random(15)
sim = Simulator(patch_list, 1000, 5)
run_time_avg = 0
for i in range(n):
    start_time = time.time()
    sim.simulate(debug=False)
    run_time = time.time() - start_time
    run_time_avg = run_time + run_time_avg

print(run_time_avg)
print(run_time_avg / n)
# sim.simulate(debug=True)
