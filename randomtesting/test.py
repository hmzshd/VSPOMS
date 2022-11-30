from patch import Patch
import time
import random
from patchGenerate import generatePatchListRandom
from PatchDisplay import displayPatch
import pandas as pd

n = 5000
probabilityList = [0.8, 0.2, 0.4, 0.64]
valuesList = [.8, .2, .4, .64]
start_time = time.time()
for i in range(n):
    random.choices(valuesList, weights=probabilityList, k=1)

randomTime = time.time() - start_time
print(f"inbuilt: {randomTime}")

x_coords,y_coords,areas,colour = [],[],[],[]
df = pd.DataFrame(columns=["x","y","area","status"])
counter = 0

for patch in generatePatchListRandom(25):
    print(patch)

    #making four seperate listes to send for graphing
    x_coords.append(patch.x_coord)
    y_coords.append(patch.y_coord)
    areas.append(patch.area)
    if (patch.status == 0):
        colour.append("red")
    elif (patch.status == 1):
        colour.append("green")

    #same as above but using df instead
    df.loc[counter] = pd.Series({'x':patch.x_coord,"y":patch.y_coord,"area":patch.area,"status":patch.status})
    counter +=1
    
print(df)
patches = [x_coords,y_coords,areas,colour]
displayPatch(patches)
