import numpy as np
import time
import random

n = 1000_000
rng = np.random.default_rng()
# probabilityList = [0.8, 0.2, 0.4,0.64]
valuesList = [.8,.2,.4,.64]
start_time = time.time()
for i in range(n):
    rng.choice(valuesList, 1, p=[0.3,0.25,0.05,0.4])

npTime = time.time() - start_time
start_time = time.time()
for i in range(n):
    random.choices(valuesList, weights=[0.3,0.25,0.05,0.4], k=1)

randomTime = time.time() - start_time
print(f"inbuilt: {randomTime}, not: {npTime}")
