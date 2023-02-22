from parser import parse_csv
from simulator import Simulator
from simulator_testing import generate_patch_list_random
patch_list, settings = parse_csv("demo.csv")

print(len(patch_list['x_coords']))
print(settings)

# print(patch_list)
# print(settings)
patch_list1 = generate_patch_list_random(75)
simulation = Simulator(patch_list1,
                       dispersal_alpha=float(settings["dispersal_alpha"]),
                       area_exponent_b=float(settings["area_exponent_b"]),
                       species_specific_constant_y=float(settings["species_specific_constant_y"]),
                       species_specific_constant_u=float(settings["species_specific_constant_u"]),
                       patch_area_effect_x=float(settings["patch_area_effect_x"]),
                       steps=100, replicates=1)


simulation.simulate(debug=True)
#
# @ property
# also initialise list as list()
