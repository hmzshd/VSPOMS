import csv
from patch import Patch
from math import sqrt, pi

with open("demo.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    patch_list = []
    for row in reader:
        if line_count == 0 or line_count == 4:
            pass
        elif line_count == 2:
            settings = [float(item) for item in row]
        # using bitwise operator to check if even
        # as this is faster than modulo!
        # the way this works is we take the 'bitwise &'
        # of the line counter with 1
        # as any ODD digit in binary will always end in 1
        # this will only return 1 when a number is odd
        # as such we need to invent this
        # so basically we're doing something like
        # NOT (binary represantation of line count) & 0001
        elif ~line_count & 1:
            x_coord = float(row[0])
            y_coord = float(row[1])
            radius = sqrt(float(row[2]) / pi)
            if int(row[3]) == 0:
                status = False
            else:
                status = True
            patch_list.append(Patch(status, x_coord, y_coord, radius))
        line_count = line_count + 1

print(patch_list)
for patch in patch_list:
    print(patch)
print(settings)