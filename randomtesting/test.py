import numpy as np
import time
import random


# probabilityList = [0.8, 0.2, 0.4,0.64]
valuesList = [.8,.2,.4,.64]
start_time = time.time()
for i in range(1000):
    print(np.random.choice(valuesList, 1, p=[0.3,0.25,0.05,0.4]))

npTime = time.time() - start_time
start_time = time.time()
for i in range(1000):
    print(random.choices(valuesList, weights=[0.3,0.25,0.05,0.4], k=1)[0])

randomTime = time.time() - start_time
print(randomTime, npTime)
