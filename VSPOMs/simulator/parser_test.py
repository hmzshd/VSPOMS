from parser import parse_csv
# from simulator import Simulator
# from simulator_testing import generate_patch_list_random
patch_list, settings = parse_csv("demo.csv")

print(patch_list)
print(settings)

# print(patch_list)
# print(settings)

# sim = Simulator(patches=generate_patch_list_random(15), steps=50, replicates=5,
#                           dispersal_alpha=settings["dispersal_alpha"],
#                           area_exponent_b=settings["area_exponent_b"],
#                           species_specific_constant_y=settings["species_specific_constant_y"],
#                           species_specific_constant_u=settings["species_specific_constant_u"],
#                           patch_area_effect_x=settings["patch_area_effect_x"])
#
# sim.simulate(debug=True)
#
# @ property
# also initialise list as list()
