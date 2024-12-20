from src.yzero import defaults
from src.yzero.character import AbstractCharacter, Archetype
from src.yzero.dice import roll_dice_pool_success
from src.yzero.errors import YZeroCharacterError
from src.yzero.translation import get_string
from src.yzero.values import AbstractValue


class DicePoolCharacter(AbstractCharacter):
    def __init__(self, archetype=None, attributes=None, skills=None, specialities=None, items=None, traits=None,
                 gear=None, name=None):
        super().__init__(archetype, specialities, items, traits, gear, name)
        if attributes is None:
            attributes = {attribute: DicePoolAttributeValue(2, 2, 4) for attribute in defaults.ATTRIBUTES}
        self.attributes = attributes
        if skills is None:
            skills = {skill: DicePoolSkillValue(0, skill.attribute, 0, 2) for skill in defaults.SKILLS}
        self.skills = skills

    def set_archetype(self, archetype):
        self.archetype = archetype
        self.attributes[archetype.key_attribute] = DicePoolAttributeValue(2, archetype.attribute_low,
                                                                          archetype.attribute_high)
        for archetype_skill in archetype.associated_skills:
            self.skills[archetype_skill] = DicePoolSkillValue(0, archetype_skill.attribute, archetype.skill_low,
                                                                   archetype.skill_high)

    def count_attributes(self):
        return sum(attribute.value for attribute in self.attributes.values())

    def count_skills(self):
        return sum(skill.value for skill in self.skills.values())

    def set_attribute(self, attribute, value):
        if attribute not in self.attributes:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        self.attributes[attribute].set_value(value)

    def adjust_attribute(self, attribute, value):
        self.attributes[attribute].adjust(value)

    def set_skill(self, skill, value):
        if skill not in self.skills:
            raise YZeroCharacterError("Skill %s does not exist" % skill.name)
        self.skills[skill].set_value(value)

    def adjust_skill(self, skill, value):
        self.skills[skill].adjust(value)

    def print_attributes(self):
        for key, value in self.attributes.items():
            print(get_string(key.name) + ": " + str(value))

    def print_skills(self):
        for key, value in self.skills.items():
            print(get_string(key.name) + ": " + str(value))


def from_template(attribute, value, low_limit, high_limit):
    """ Creates a DicePoolSkillValue from a SkillTemplate and a value."""
    return DicePoolSkillValue(attribute, value, low_limit, high_limit)


class DicePoolArchetype(Archetype):
    def __init__(self, name, key_attribute, associated_skills=None, attribute_low=2, attribute_high=5, skill_low=0,
                 skill_high=3):
        super().__init__(name, key_attribute, associated_skills)
        self.attribute_low = attribute_low
        self.attribute_high = attribute_high
        self.skill_low = skill_low
        self.skill_high = skill_high


class DicePoolAttributeValue(AbstractValue):
    """ Dice pool value for attributes with a value between 1 and 5.
        Only key attributes can have a value of 5."""

    def __init__(self, value, low_limit=1, high_limit=5):
        """ Sets the starting value for the attribute or skill. """
        super().__init__(value, low_limit, high_limit)

    def roll(self):
        """ Rolls for attribute success based on value.
        Return number of successes."""
        return roll_dice_pool_success(self.value, 6)

    def __str__(self):
        if self.value == 1:
            return get_string("attribute_feeble")
        elif self.value == 2:
            return get_string("attribute_below")
        elif self.value == 3:
            return get_string("attribute_average")
        elif self.value == 4:
            return get_string("attribute_capable")
        elif self.value == 5:
            return get_string("attribute_extraordinary")


class DicePoolSkillValue(AbstractValue):
    """ Dice pool value for skills with a value between 0 and 5."""

    def __init__(self, value, attribute, low_limit=0, high_limit=5):
        """ Sets the starting value for the attribute or skill. """
        super().__init__(value, low_limit, high_limit)
        self.attribute = attribute

    def roll(self):
        return roll_dice_pool_success(self.value + self.attribute.value, 6)

    def __str__(self):
        if self.value == 0:
            return get_string("skill_none")
        elif self.value == 1:
            return get_string("skill_novice")
        elif self.value == 2:
            return get_string("skill_trained")
        elif self.value == 3:
            return get_string("skill_experienced")
        elif self.value == 4:
            return get_string("skill_veteran")
        elif self.value == 5:
            return get_string("skill_elite")
