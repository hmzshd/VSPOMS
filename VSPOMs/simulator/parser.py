"""
Parser.

Simple module with one function parse_csv, which parses a csv file.
And returns the setting for the simulation, and a dictionary corresponding to the patches
"""

from math import sqrt, pi
import csv


def parse_csv(filename):
    """
    Function to parse a CSV file.

    Returns two lists, one containing the sim settings.
    And one containing patch objects, created from the data given in the CSV file.

    Parameters
        ---
            filename: string
                filename of csv file to parse_csv
    """
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        x_coords = list()
        y_coords = list()
        statuses = list()
        radiuses = list()
        settings = dict()
        heading_line_indexes_set = set((0,4))
        for row in reader:

            # 0th and 4th row just contain headings
            if line_count in heading_line_indexes_set:
                pass

            elif line_count == 2:
                settings["dispersal_alpha"] = float(row[0])
                settings["area_exponent_b"] = float(row[1])
                settings["species_specific_constant_y"] = float(row[2])
                settings["species_specific_constant_u"] = float(row[3])
                settings["patch_area_effect_x"] = float(row[4])

            # using bitwise operator to check if even
            # as this is faster than modulo!
            # the way this works is we take the 'bitwise &'
            # of the line counter with 1
            # as any ODD digit in binary will always end in 1
            # this will only return 1 when a number is odd
            # as such we need to invent this
            # basically we're doing something like
            # NOT (binary representation of line count) & 0001
            elif ~line_count & 1:
                x_coord = float(row[0])
                y_coord = float(row[1])
                radius = sqrt(float(row[2]) / pi)
                if int(row[3]) == 0:
                    status = False
                else:
                    status = True
                x_coords.append(x_coord)
                y_coords.append(y_coord)
                statuses.append(status)
                radiuses.append(radius)
            line_count = line_count + 1

    patch_dict = {"x_coords": x_coords, "y_coords": y_coords,
                  "radiuses": radiuses, "statuses": statuses}

    return patch_dict, settings
