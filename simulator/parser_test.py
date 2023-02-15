from parser import parse

patch_list, settings = parse("demo.csv")


print(patch_list)
for patch in patch_list:
    print(patch)
print(settings)
