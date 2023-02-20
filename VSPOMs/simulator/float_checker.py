"""
    Float checker
    Very simple module to check if a number passed is a float or not.
    Needed as the built-in isdigit will return false for floats - e.g.
    "0.011".isdigit() would return false - as would isnumeric()
    seems dumb to me but that's python for you!

"""


def is_float(num):
    """
    Function to check if input can be converted to float

    Returns True if it can, False otherwise

    Parameters
        ---
            num: unknown value
                value we want to check to see if we can convert to float or not.
    """

    try:
        float(num)
    except ValueError:
        return False
    return True
