"""
Parser.

Simple module with one function parse, which parses a csv file.
And returns the setting for the simulation, and the patch objects
"""

from math import sqrt, pi
import csv
from patch import Patch


def parse(filename):
    """
    Function to parse a CSV file.

    Returns two lists, one containing the sim settings.
    And one containing patch objects, created from the data given in the CSV file.

    Parameters
        ---
            filename: string
                filename of csv file to parse
    """
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        patch_list = []
        settings = []
        for row in reader:

            # 0th and 4th row just contain headings
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
                patch_list.append(Patch(status, x_coord, y_coord, radius))
            line_count = line_count + 1

    return patch_list, settings
