from src.yzero.errors import YZeroCharacterError


class AbstractValue:
    """ Abstract class for all year zero engine values."""
    def __init__(self, value, lower_limit, upper_limit):
        self.value = None
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.set_value(value)

    def set_value(self, value):
        """ Sets attribute value between lower limit and upper limit. """
        if self.lower_limit > value > self.upper_limit:
            raise YZeroCharacterError("Value must be between %d and %d but was: %d" % (self.lower_limit, self.upper_limit, value))
        self.value = value

    def adjust(self, value):
        """ Adjusts attribute value by adding or subtracting value. """
        self.set_value(self.value + value)

    def set_starting_value(self, value, primary_attribute=False, allow_one=False):
        raise YZeroCharacterError("Method not implemented in super class")

