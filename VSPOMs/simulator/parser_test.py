from parser import parse_csv

patch_list, settings = parse_csv("../static/data/demo.csv")


print(patch_list)
# @ property
# also initialise list as list()
