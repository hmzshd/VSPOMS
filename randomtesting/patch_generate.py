from patch import Patch
import random


def generate_patch_list_random(num):
    patch_list = []
    for i in range(num):
        patch_list.append(Patch(bool(random.randint(0, 1)), random.uniform(0, 25), random.uniform(0, 25), random.uniform(0, 5)))
    return patch_list

