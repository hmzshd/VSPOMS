"""
Parser.

The parser for the sim, parse_csv, which takes in a csv file,
validates it, throws an error if need be using row_error_investigator to find the
invalid data and raise_value_error to raise the correct error.
If no errors, it returns the setting for the simulation,
and a dictionary corresponding to the patches
"""

# pylint: disable=line-too-long

from math import sqrt, pi
import csv

# necessary to wrap this in try except due to the location of manage.py
try:
    from simulator.float_checker import is_float
    from simulator.patch import Patch
except ModuleNotFoundError:
    from float_checker import is_float
    from patch import Patch


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
        # we need to create an empty bytes object as a UnicodeDecodeError
        # requires this
        empty_bytes_object = b''
        raise UnicodeDecodeError("file does not end with .csv", empty_bytes_object, 0, 1, "file does not end with .csv")

    with open(filename, encoding="utf-8") as csvfile:

        reader = csv.reader(csvfile, delimiter=',')
        x_coords = []
        y_coords = []
        statuses = []
        radiuses = []
        settings = dict()
        first_column_headings = set(('a', 'x',))
        valid_status_set = set((0, 1))
        settings_read = False

        # the following vars are needed to check if we need to
        # scale the values when sending to frontend - if we have
        # radius < 6 we do - as bokeh cannot display this
        min_radius = 6.0
        scaling_factor = 1.0
        # we set the smallest radius to be min_radius  -
        # using float to ensure it's the same value not the same reference.
        # we could also set it to none - but then we'd be performing
        # two checks each time - if it's != none and then
        # if it's less than the min. this way we just have to check once
        # and if it never gets smaller than 6 that's fine - we don't have to
        # do anything!
        smallest_radius_seen = float(min_radius)

        for line_number, row in enumerate(reader):
            # incrementing line number, as it's not 0 indexed
            line_number = line_number + 1
            # skipping 'empty' rows if there are any
            if len(row) == 0:
                continue
            # checking if all vals are empty str
            # skipping if so
            elif row[0] == '':
                # all performs a check on all rows
                if all(item in row == '' for item in row):
                    continue

            # checking if the first item is a number
            # if it's not we then check if it's an acceptable first column heading
            # if it is, we can safely skip, if not a heading
            # we have to raise a valueerror, this is incase we have some case where
            # the first item is 1.03x or some other typo.
            elif is_float(row[0]):
                # checking if settings read - done first for efficiency,
                # most of the lines will pass this test, so we want it to be first.
                if settings_read:

                    # try except in case one of the elements is
                    # not a float - in which case we pass the row
                    # to the error detection
                    try:
                        x_coord = float(row[0])
                        y_coord = float(row[1])
                        area = float(row[2])
                        radius = sqrt(area / pi)

                        if radius < smallest_radius_seen:
                            smallest_radius_seen = radius
                            scaling_factor = min_radius / smallest_radius_seen

                        status_int = int(row[3])
                        # validating patch status
                        if status_int not in valid_status_set:
                            raise_value_error(4, row, line_number, row[3], 3)

                        # converting to bool
                        if status_int == 0:
                            status = False
                        else:
                            status = True

                        x_coords.append(x_coord)
                        y_coords.append(y_coord)
                        statuses.append(status)
                        radiuses.append(radius)

                    except ValueError:
                        # we only want the 0-3rd items as their may be blank lines
                        # which we simply don't care about
                        row_error_investigator(row[0:4], line_number)

                # path to take if settings unread
                else:
                    try:
                        settings["dispersal_alpha"] = float(row[0])
                        settings["area_exponent_b"] = float(row[1])
                        settings["species_specific_constant_y"] = float(row[2])
                        settings["species_specific_constant_u"] = float(row[3])
                        settings["patch_area_effect_x"] = float(row[4])
                        settings_read = True
                    except ValueError:
                        # similar to above - we only care about the 0-4th els
                        # in case of any blank items
                        row_error_investigator(row[0:5], line_number)


            # big if else here -
            # this is the case if the 0th item of the row isn't a float
            # in which case we check if it's a valid column heading
            # if it is cool - if not we raise an error
            else:
                # converting item to lower and stripping whitespace
                item = row[0].lower().strip()
                if item not in first_column_headings:
                    raise_value_error(1, row, line_number, row[0], 0)

    # if scaling factor is 1 - it's not been changed, therefore
    # we do not need to scale up the radiuses to send to frontend.
    # print(scaling_factor)
    if scaling_factor != 1.0:
        radiuses_scaled = [radius * scaling_factor for radius in radiuses]
        patch_dict = {"x_coords": x_coords, "y_coords": y_coords,
                      "radiuses": radiuses_scaled, "statuses": statuses}

    else:
        patch_dict = {"x_coords": x_coords, "y_coords": y_coords,
                      "radiuses": radiuses, "statuses": statuses}

    return patch_dict, settings, scaling_factor


def row_error_investigator(row, line_number):
    """
    Function to find the unconvertible item in a list.

    Finds which element of a list in not convertible to a float
    and then calls raise_value_error, with the appropriate case
    and any values it needs

    Parameters
        ---
            row: list
                the row to be checked
            line_number: int
                the line number, only used to call raise_value_error
    """

    unconvertible_items = []

    for index, element in enumerate(row):
        if not is_float(element):
            unconvertible_items.append((index, element))

    if len(unconvertible_items) == 1:
        item = unconvertible_items[0][0]
        column = unconvertible_items[0][1]
        raise_value_error(2, row, line_number, item, column)
    else:
        items = [item[1] for item in unconvertible_items]
        raise_value_error(3, row, line_number, items, 0)


def raise_value_error(case_value, row, line_number, item, column):
    """
    Function to raise a ValueError

    Mostly just a switch case thing, that formats the string to be raised with
    the ValueError

    Parameters
        ---
            case_value : int
                what 'case' the error is
                    if 1 - error is on the 0th element of a row - and likely a headings issue
                    if 2 - error is not on 0th element - needed as we check for headings -
                        as these can be safely skipped, but something like 10.4x for an x_coord can't
                    if 3 - error is on multiple elements in row
                    if 4 - error is that what it's expecting to be a status isn't 1 or 0
            row: list
                the row containing the error
            line_number: int
                the line number
            item: unknown
                the offending item
            column: int
                the column number of the offending item.
    """
    error_string = "unknown error - try a different CSV - or contact devs for help"
    match case_value:
        case 1:
            error_string = f"Error parsing CSV - may be " \
                           f"an issue with column headings, first heading must be " \
                           f"'a' or 'x' - case and space insensitive. \nError Details:\nItem: {item} Column " \
                           f"Number: {column}, " \
                           f"Line Number: {line_number}\nRow: {row}"

        case 2:
            error_string = f"Error parsing CSV, one item is invalid\nError Details:\nItem: {item}, " \
                           f"Column Number: {column}, Line Number: {line_number}\nRow: {row}"

        case 3:
            error_string = f"Error parsing CSV, multiple items are invalid\nError Details:\nItems: {item}\n" \
                           f"Line Number: {line_number}\nRow: {row}"

        case 4:
            error_string = f"""Error parsing CSV, patch status must be 0 or 1
                            Line Number: {line_number}, Given item: {row[3]}"""

    raise ValueError(error_string)

