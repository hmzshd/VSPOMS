from simulator import Simulator
from parser import parse_csv
from patch import Patch
from patch_generator import generate_patch_list_random
a,b,c = parse_csv("demo.csv")

# for patch in c:
#     print(patch)
d = c[:5]
# for p in d:
#     print(p)
simulation = Simulator(d,
                       dispersal_alpha=float(b["dispersal_alpha"]),
                       area_exponent_b=float(b["area_exponent_b"]),
                       species_specific_constant_y=float(b["species_specific_constant_y"]),
                       species_specific_constant_u=float(b["species_specific_constant_u"]),
                       patch_area_effect_x=float(b["patch_area_effect_x"]),
                       steps=100, replicates=1, debug=True)

simulation.simulate()
