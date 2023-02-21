from parser import parse_csv
# from simulator import Simulator
# from simulator_testing import generate_patch_list_random
patch_list, settings = parse_csv("demo.csv")

print(len(patch_list['x_coords']))
print(settings)

# print(patch_list)
# print(settings)

# simulation = Simulator(patch_list,
#                        dispersal_alpha=float(settings["dispersal_kernel"]),
#                        area_exponent_b=float(settings["connectivity"]),
#                        species_specific_constant_y=float(settings["colonization_probability"]),
#                        species_specific_constant_u=float(settings["patch_extinction_probability_u"]),
#                        patch_area_effect_x=float(settings["patch_extinction_probability_x"]),
#                        steps=100, replicates=1)


# sim.simulate(debug=True)
#
# @ property
# also initialise list as list()
