from patch import Patch
import random


def generate_patch_list_random(num):
    patch_list = []
    for i in range(num):
        patch_list.append(Patch(random.randint(0, 3), random.uniform(0, 25), random.uniform(0, 25), random.uniform(0, 5)))
        patch_list[i].set_probability(random.uniform(0, 1))
    return patch_list

