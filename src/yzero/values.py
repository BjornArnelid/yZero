from src.yzero.errors import YZeroCharacterError


class AbstractValue:
    """ Abstract class for all year zero engine values."""

    def __init__(self, value, soft_limits, hard_limits):
        self.value = None
        self.soft_limits = soft_limits
        self.hard_limits = hard_limits
        self.set_value(value)

    def set_value(self, value, apply_soft_limits=False):
        """ Sets attribute value between lower limit and upper limit. """
        if not (self.hard_limits[0] <= value <= self.hard_limits[1]):
            raise YZeroCharacterError(
                "Value must be between %d and %d but was: %d" % (self.hard_limits[0], self.hard_limits[1], value))
        if apply_soft_limits and not (self.soft_limits[0] <= value <= self.soft_limits[1]):
            raise YZeroCharacterError(
                "Value must be between soft limits %d and %d but was: %d" % (self.hard_limits[0], self.hard_limits[1], value))
        self.value = value

    def adjust(self, value, apply_soft_limits=False):
        """ Adjusts attribute value by adding or subtracting value. """
        self.set_value(self.value + value, apply_soft_limits)
