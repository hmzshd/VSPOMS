"""
Parser.

Simple module with one function parse_csv, which parses a csv file.
And returns the setting for the simulation, and a dictionary corresponding to the patches
"""

from math import sqrt, pi
import csv

import InvalidRowError

# necessary to wrap this in try except due to the location of manage.py
try:
    from simulator.float_checker import is_float
    from simulator.patch import Patch
    from simulator import InvalidRowError
except ModuleNotFoundError:
    from float_checker import is_float
    from patch import Patch
    from InvalidRowError import InvalidRowError


def parse_csv(filename):
    """
    Function to parse a CSV file.

    Returns two dicts, one containing the sim settings.
    And one containing the data for patches, formatted in a slightly odd way
    as this is how the frontend takes it in.

    Parameters
        ---
            filename: string
                filename of csv file to parse_csv
    """

    # checking file ends with csv - if not we'll return an error
    # this doesn't check the file is a valid csv though, just that it ends with
    # csv. that will still raise a UnicodeDecodeError (or similar) which should be
    # handled by frontend - in addition to FileNotFound error.

    if not filename.lower().endswith("csv"):
        raise UnicodeDecodeError("unknown", filename, )

    with open(filename, encoding="utf-8") as csvfile:

        reader = csv.reader(csvfile, delimiter=',')
        x_coords = list()
        y_coords = list()
        statuses = list()
        radiuses = list()
        settings = dict()
        patch_list = list()
        first_column_headings = set(('a', 'A', 'x', 'X', 'a ', 'A ', 'x ', 'X '))
        settings_read = False

        for line_number, row in enumerate(reader):
            # skipping 'empty' rows if there are any
            if len(row) == 0:
                pass

            # checking if the first item is a number
            # if it's not we then check if it's an acceptable first column heading
            # if it is, we can safely skip, if not a heading
            # we have to raise a valueerror, this is incase we have some case where
            # the first item is 1.03x or some other typo.
            elif is_float(row[0]):
                # checking if settings read - done first for efficiency,
                # most of the lines will pass this test, so we want it to be first.
                if settings_read:
                    try:
                        x_coord = float(row[0])
                        y_coord = float(row[1])
                        area = float(row[2])
                        radius = sqrt(area / pi)
                        if int(row[3]) == 0:
                            status = False
                        else:
                            status = True
                        x_coords.append(x_coord)
                        y_coords.append(y_coord)
                        statuses.append(status)
                        radiuses.append(radius)
                        patch_list.append(Patch(status, x_coord, y_coord, area))
                    except:
                        pass
                # path to take if settings unread
                else:
                    settings["dispersal_alpha"] = float(row[0])
                    settings["area_exponent_b"] = float(row[1])
                    settings["species_specific_constant_y"] = float(row[2])
                    settings["species_specific_constant_u"] = float(row[3])
                    settings["patch_area_effect_x"] = float(row[4])
                    settings_read = True
            else:
                if row[0] not in first_column_headings:
                    item = row[0]
                    column = 0
                    line_number = line_number + 1
                    error_text = f"Item: {item} Column Number: {column}, Line Number: {line_number}\nRow: {row}"
                    raise ValueError(error_text)

    patch_dict = {"x_coords": x_coords, "y_coords": y_coords,
                  "radiuses": radiuses, "statuses": statuses}

    return patch_dict, settings, patch_list
