from src.yzero.character import AbstractCharacter, CHARACTER_ATTRIBUTES, CHARACTER_SKILLS
from src.yzero.dice import roll_dice
from src.yzero.errors import YZeroCharacterError
from src.yzero.translation import get_string
from src.yzero.values import AbstractValue


class StepDiceCharacter(AbstractCharacter):
    def __init__(self, archetype=None, attributes=None, skills=None, specialities=None, items=None, traits=None,
                 gear=None, name=None):
        super().__init__(archetype, specialities, items, traits, gear, name)
        if attributes is None:
            attributes = {}
        self.attributes = attributes
        if skills is None:
            skills = {}
        self.skills = skills

    def count_attributes(self, level):
        amount = 0
        for attribute in self.attributes.values():
            if attribute.level == level:
                amount += 1
        return amount

    def count_skills(self, level):
        amount = 0
        for skill in self.skills.values():
            if skill.level == level:
                amount += 1
        return amount

    def set_attribute(self, attribute, value, primary_attribute=False, allow_one=False):
        if attribute not in CHARACTER_ATTRIBUTES:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        self.attributes[attribute] = StepDiceAttributeValue(value)

    def adjust_attribute(self, attribute, value, primary_attribute=False, allow_one=False):
        self.attributes[attribute].adjust(value)

    def set_skill(self, skill_template, value, primary_attribute=False, allow_one=False):
        if skill_template not in CHARACTER_SKILLS:
            raise YZeroCharacterError("Skill %s does not exist" % skill_template.name)
        self.skills[skill_template.name] = from_template(skill_template, value)

    def adjust_skill(self, skill, value, primary_attribute=False, allow_one=False):
        self.skills[skill].adjust(value)

    def print_attributes(self):
        for key, value in self.attributes.items():
            print(key + ": " + str(value))

    def print_skills(self):
        for key, value in self.skills.items():
            print(key + ": " + str(value))


def from_template(template, value):
    """ Creates a StepDiceSkillValue from a SkillTemplate and a value."""
    return StepDiceSkillValue(template.attribute, value)


# Step dice values
D = 1
C = 2
B = 3
A = 4


def calculate_dice_size(value):
    if value == 0:
        return 0
    elif value == D:
        return 6
    elif value == C:
        return 8
    elif value == B:
        return 10
    elif value == A:
        return 12
    raise YZeroCharacterError("Invalid value for StepDiceAttribute")


def roll(dice_size):
    """ Rolls a step dice value and returns the result."""
    result = roll_dice(dice_size)
    if result >= 10:
        return 2
    elif result >= 6:
        return 1
    return 0


class StepDiceAttributeValue(AbstractValue):
    """ Step dice value for attributes with a value between A and D.
        Only Primary attributes can have a value of 5."""
    def __init__(self, value='C'):
        super().__init__(value, 1, 4)

    def set_starting_value(self, value, key_skill=False, allow_one=False):
        """ Sets the starting value for the attribute or skill. """
        self.set_value(value)

    def dice_size(self):
        calculate_dice_size(self.value)

    def roll(self):
        """ Rolls for attribute success based on value.
        Return number of successes."""
        return roll(self.dice_size())

    def __str__(self):
        if self.value == D:
            return get_string("attribute_feeble")
        elif self.value == C:
            return "attribute_average"
        elif self.value == B:
            return "attribute_capable"
        elif self.value == A:
            return "attribute_extraordinary"
        raise YZeroCharacterError("Invalid value for StepDiceAttribute")

class StepDiceSkillValue(AbstractValue):
    """ Dice pool value for skills with a value between 0 and 5."""
    def __init__(self, value, attribute):
        super().__init__(value, 0, A)
        self.attribute = attribute

    def set_starting_value(self, value, key_skill=False, allow_one=False):
        """ Sets the starting value for the attribute or skill. """
        if value == B and not key_skill:
            raise YZeroCharacterError("Only skills listed in archetype can have a value of B")
        elif value > B:
            raise YZeroCharacterError("Skill value can not be set to A during character creation")
        self.set_value(value)

    def dice_size(self):
        calculate_dice_size(self.value)

    def roll(self):
        return self.attribute.roll() + roll(self.dice_size())

    def __str__(self):
        if self.value == 0:
            return get_string("skill_none")
        elif self.value == D:
            return get_string("skill_novice")
        elif self.value == C:
            return get_string("skill_experienced")
        elif self.value == B:
            return get_string("skill_veteran")
        elif self.value == A:
            return get_string("skill_elite")
        raise YZeroCharacterError("Invalid value for StepDiceAttribute")