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
        self.attributes[archetype.key_attribute] = DicePoolAttributeValue(2, archetype.key_attribute_soft_limits[0],
                                                                          archetype.key_attribute_soft_limits[1])
        for archetype_skill in archetype.associated_skills:
            self.skills[archetype_skill] = DicePoolSkillValue(0, archetype_skill.attribute,
                                                              archetype.associated_skills_soft_limits[0],
                                                              archetype.associated_skills_soft_limits[1])

    def count_attributes(self):
        return sum(attribute.value for attribute in self.attributes.values())

    def count_skills(self):
        return sum(skill.value for skill in self.skills.values())

    def set_attribute(self, attribute, value, apply_soft_limits=False):
        if attribute not in self.attributes:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        self.attributes[attribute].set_value(value, apply_soft_limits)

    def adjust_attribute(self, attribute, value, apply_soft_limits=False):
        self.attributes[attribute].adjust(value, apply_soft_limits)

    def set_skill(self, skill, value, apply_soft_limits=False):
        if skill not in self.skills:
            raise YZeroCharacterError("Skill %s does not exist" % skill.name)
        self.skills[skill].set_value(value, apply_soft_limits)

    def adjust_skill(self, skill, value, apply_soft_limits=False):
        self.skills[skill].adjust(value, apply_soft_limits)

    def print_attributes(self):
        for key, value in self.attributes.items():
            print(get_string(key.name) + ": " + str(value))

    def print_skills(self):
        for key, value in self.skills.items():
            if value.value > 0:
                print(get_string(key.name) + ": " + str(value))


def from_template(attribute, value, low_limit, high_limit):
    """ Creates a DicePoolSkillValue from a SkillTemplate and a value."""
    return DicePoolSkillValue(attribute, value, low_limit, high_limit)


class DicePoolArchetype(Archetype):
    def __init__(self, name, key_attribute, associated_skills=None, key_attribute_soft_limits=None,
                 associated_skills_soft_limits=None, ):
        super().__init__(name, key_attribute, associated_skills)
        if key_attribute_soft_limits is None:
            self.key_attribute_soft_limits = [2, 5]
        if associated_skills_soft_limits is None:
            self.associated_skills_soft_limits = [0, 3]


class DicePoolAttributeValue(AbstractValue):
    """ Dice pool value for attributes with a value between 1 and 5.
        Only key attributes can have a value of 5."""

    def __init__(self, value, low_limit=1, high_limit=4):
        """ Sets the starting value for the attribute or skill. """
        super().__init__(value, [low_limit, high_limit], [1, 5])

    def roll(self):
        """ Rolls for attribute success based on value.
        Return number of successes."""
        return roll_dice_pool_success(self.value, 6)

    def __str__(self):
        result_string = ""
        if self.value == 1:
            result_string =  get_string("attribute_feeble")
        elif self.value == 2:
            result_string =  get_string("attribute_below")
        elif self.value == 3:
            result_string =  get_string("attribute_average")
        elif self.value == 4:
            result_string =  get_string("attribute_capable")
        elif self.value == 5:
            result_string =  get_string("attribute_extraordinary")
        return result_string + " (" + str(self.value) + ")"


class DicePoolSkillValue(AbstractValue):
    """ Dice pool value for skills with a value between 0 and 5."""

    def __init__(self, value, attribute, low_limit=0, high_limit=5):
        """ Sets the starting value for the attribute or skill. """
        super().__init__(value, [low_limit, high_limit], [0, 5])
        self.attribute = attribute

    def roll(self):
        return roll_dice_pool_success(self.value + self.attribute.value, 6)

    def __str__(self):
        result_string = ""
        if self.value == 0:
            result_string =  get_string("skill_none")
        elif self.value == 1:
            result_string =  get_string("skill_novice")
        elif self.value == 2:
            result_string =  get_string("skill_trained")
        elif self.value == 3:
            result_string =  get_string("skill_experienced")
        elif self.value == 4:
            result_string =  get_string("skill_veteran")
        elif self.value == 5:
            result_string =  get_string("skill_elite")
        return result_string + " (" + str(self.value) + ")"
