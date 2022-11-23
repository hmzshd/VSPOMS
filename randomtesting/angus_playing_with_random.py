import patch
from patch_generate import generate_patch_list_random
import patches_weighted_random
import  spom_quantities

# print(generate_patch_list_random(5))

patch_list = generate_patch_list_random(5)


# print([patches_weighted_random(patch_list) for i in range(5)])

test_list = []
for i in range(10000):
    test_list.append(patches_weighted_random(patch_list))

print(test_list)