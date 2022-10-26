import time
import random

n = 5000
probabilityList = [0.8, 0.2, 0.4,0.64]
valuesList = [.8,.2,.4,.64]
start_time = time.time()
for i in range(n):
    random.choices(valuesList, weights=probabilityList, k=1)

randomTime = time.time() - start_time
print(f"inbuilt: {randomTime}")
 