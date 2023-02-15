from parser import parse_csv

patch_list, settings = parse_csv("demo.csv")


print(len(patch_list))
for patch in patch_list:
    print(patch)
print(settings)

# @ property
# also initialise list as list()
