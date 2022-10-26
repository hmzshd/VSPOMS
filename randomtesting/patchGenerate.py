from patch import  Patch
import random


def generatePatchListRandom(num):
    patchList = []
    for i in range(num):
        patchList.append(Patch(random.randint(0, 3), random.uniform(0.1, 25)))
        patchList[i].calculateProbability(random.uniform(0, 1))
    return patchList

