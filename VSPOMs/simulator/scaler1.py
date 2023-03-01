from parser import parse_csv

a,b,c = parse_csv("demo.csv")

for d in a.keys():
    # print(d)
    # print(a[d])
    min_x = min(a["x_coords"])
    min_y = min(a["y_coords"])
    # print(min_x,min_y)

for index, current_x_coord in enumerate(a["x_coords"]):
    a["x_coords"][index] = current_x_coord - min_x

for index, current_y_coord in enumerate(a["y_coords"]):
    a["y_coords"][index] = current_y_coord - min_y

# print(a["x_coords"])
for x in a["x_coords"]:
    print(x)

print("\n\n\n---------------\n\n\n")
for y in a["y_coords"]:
    print(y)

