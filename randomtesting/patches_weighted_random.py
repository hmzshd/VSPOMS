# function randomly selects patch for event based on internally stored weight
import random
from itertools import accumulate
from bisect import bisect
from patchGenerate import generatePatchListRandom


def patches_weighted_random(patches):
    n = len(patches)

    cum_weights = []
    for patch in patches:
        cum_weights.append(patch.probability)
    cum_weights = list(accumulate(cum_weights))

    total = cum_weights[-1] + 0.0  # convert to float
    if total <= 0.0:
        raise ValueError('Total of weights must be greater than zero')

    hi = n - 1
    return patches[bisect(cum_weights, random.random() * total, 0, hi)]


# vvv TESTING vvv
patch_list = generatePatchListRandom(5)

selected_list =[]
for i in range(10000):
    selected_list.append(patches_weighted_random(patch_list))

counts = []
for i in selected_list:
    if [i.probability, selected_list.count(i), i] not in counts:
        counts.append([i.probability, selected_list.count(i), i])

for i in counts:
    print(i)
