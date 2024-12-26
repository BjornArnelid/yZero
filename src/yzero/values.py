from src.yzero.errors import YZeroCharacterError


class AbstractValue:
    """ Abstract class for all year zero engine values."""

    def __init__(self, value, low_limit, high_limit):
        self.value = None
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.set_value(value)

    def set_value(self, value):
        """ Sets attribute value between lower limit and upper limit. """
        if not (self.low_limit <= value <= self.high_limit):
            raise YZeroCharacterError(
                "Value must be between %d and %d but was: %d" % (self.low_limit, self.high_limit, value))
        self.value = value

    def adjust(self, value):
        """ Adjusts attribute value by adding or subtracting value. """
        self.set_value(self.value + value)
