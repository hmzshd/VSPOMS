import math

# SPOM quantity functions


def dispersal_kernel(a, patch_i, patch_j):
    # parameter a is the species-specific dispersal constant.

    return math.exp((-a) * distance(patch_i, patch_j))


def connectivity(patches, patch_i, a, b):
    # MUST CLARIFY EXPONENT ON AREA FACTOR
    # b is area factor exponent ??? clarify!

    connectivity_total = 0
    for patch in patches:
        if patch != patch_i:
            connectivity_total += patch.get_probability() * dispersal_kernel(a, patch_i, patch) * patch.get_area()

    return connectivity_total


def colonization(patches, patch_i, a, y, b):
    # y is species-specific constant
    # MUST CLARIFY WHETHER y=a

    return 1 - math.exp(-y * connectivity(patches, patch_i, a, b))


def extinction(u, patch, x):
    # clarify x - as patch area factor exponent

    e = u / (patch.get_area)**x
    if e > 1:
        return 1.0
    else:
        return e

def distance(patch_i, patch_j):
    i_coords = patch_i.get_coords()
    j_coords = patch_j.get_coords()

    return math.sqrt((i_coords[0]-j_coords[0])**2 + (i_coords[1]-j_coords[1])**2)
