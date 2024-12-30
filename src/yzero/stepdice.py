from src.yzero import defaults
from src.yzero.character import Character
from src.yzero.defaults import STRENGTH, AGILITY, WITS, EMPATHY
from src.yzero.dice import roll_dice
from src.yzero.errors import YZeroCharacterError
from src.yzero.translation import get_string
from src.yzero.values import AbstractValue, ResourcePool


class StepDiceCharacter(Character):
    """ Character with step dice values for attributes and skills."""

    def __init__(self, attributes, skills, archetype=None, specialities=None, items=None, traits=None,
                 gear=None, name=None):
        super().__init__(archetype, specialities, items, traits, gear, name)
        if attributes is None:
            attributes = {attribute: StepDiceAttributeValue(C) for attribute in defaults.ATTRIBUTES}
        self.attributes = attributes
        if skills is None:
            skills = {skill: StepDiceSkillValue(NONE, skill.attribute) for skill in defaults.SKILLS}
        self.skills = skills
        self.calculate_resource_pools()

    def set_attribute(self, attribute, value):
        super().set_attribute(attribute, value)
        self.calculate_resource_pools()

    def calculate_resource_pools(self):
        resource_value = int((self.attributes[STRENGTH].dice_size() + self.attributes[AGILITY].dice_size()) / 4 + 0.5)
        self.health_pool = ResourcePool(resource_value)
        resource_value = int((self.attributes[WITS].dice_size() + self.attributes[EMPATHY].dice_size()) / 4 + 0.5)
        self.resolve_pool = ResourcePool(resource_value)


def count_attributes(character, level):
    """ Counts the number of attributes with a specific level."""
    amount = 0
    for attribute in character.attributes.values():
        if attribute.value == level:
            amount += 1
    return amount


def count_skills(character, level):
    """ Counts the number of skills with a specific level."""
    amount = 0
    for skill in character.skills.values():
        if skill.value == level:
            amount += 1
    return amount


# Step dice values
NONE = 0
D = 1
C = 2
B = 3
A = 4


class StepDiceAttributeValue(AbstractValue):
    """ Step dice value for attributes with a value between A and D.
        Only Primary attributes can have a value of 5."""

    def __init__(self, value=C):
        super().__init__(value, 1, 4)

    def dice_size(self):
        return calculate_dice_size(self.value)

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

    def dice_size(self):
        return calculate_dice_size(self.value)

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
