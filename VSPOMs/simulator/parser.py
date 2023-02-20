"""
Parser.

Simple module with one function parse_csv, which parses a csv file.
And returns the setting for the simulation, and a dictionary corresponding to the patches
"""

from math import sqrt, pi
import csv
from float_checker import is_float


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
        x_coords = list()
        y_coords = list()
        statuses = list()
        radiuses = list()
        settings = dict()
        settings_read = False

        for row in reader:
            # skipping 'empty' rows if there are any
            if len(row) == 0:
                # change this!!!
                # print("passing on ", row)
                continue

            # checking if the first item is a number
            # if it's not it's simply the headings of the rows
            # which can be safely ignored.

            # make elif!
            print(row[0])
            if is_float(row[0]):
                print("A DIGIT!")
                # checking if settings read - once again done first for efficiency
                if settings_read:
                    # print("settings read, values are", row)
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

                # path to take if settings unread
                else:
                    # print("settings unread, values are", row)
                    settings["dispersal_alpha"] = float(row[0])
                    settings["area_exponent_b"] = float(row[1])
                    settings["species_specific_constant_y"] = float(row[2])
                    settings["species_specific_constant_u"] = float(row[3])
                    settings["patch_area_effect_x"] = float(row[4])
                    settings_read = True

    patch_dict = {"x_coords": x_coords, "y_coords": y_coords,
                  "radiuses": radiuses, "statuses": statuses}

    return patch_dict, settings
