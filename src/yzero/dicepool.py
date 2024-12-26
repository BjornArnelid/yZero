from src.yzero import defaults
from src.yzero.character import Character, Archetype
from src.yzero.dice import roll_dice_pool_success
from src.yzero.errors import YZeroCharacterError
from src.yzero.translation import get_string
from src.yzero.values import AbstractValue


class DicePoolCharacter(Character):
    def __init__(self, archetype=None, attributes=None, skills=None, specialities=None, items=None, traits=None,
                 gear=None, name=None):
        super().__init__(archetype, specialities, items, traits, gear, name)
        if attributes is None:
            attributes = {attribute: DicePoolAttributeValue(2, 2, 4) for attribute in defaults.ATTRIBUTES}
        self.attributes = attributes
        if skills is None:
            skills = {skill: DicePoolSkillValue(0, skill.attribute, 0, 2) for skill in defaults.SKILLS}
        self.skills = skills


    def count_attributes(self):
        return sum(attribute.value for attribute in self.attributes.values())

    def count_skills(self):
        return sum(skill.value for skill in self.skills.values())

    def set_attribute(self, attribute, value):
        if attribute not in self.attributes:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        if self.archetype:
            self.attributes[attribute] = self.archetype.to_attribute(attribute, value)
        else:
            self.attributes[attribute] = DicePoolAttributeValue(value)

    def set_skill(self, skill, value):
        if skill not in self.skills:
            raise YZeroCharacterError("Skill %s does not exist" % skill.name)
        if self.archetype:
            self.skills[skill] = self.archetype.to_skill(skill, value)
        else:
            self.skills[skill] = DicePoolSkillValue(value, skill.attribute)




class DicePoolArchetype(Archetype):
    def __init__(self, name, key_attribute, associated_skills=None):
        super().__init__(name, key_attribute, associated_skills)

    def to_attribute(self, attribute, value):
        if not (2 <= value <= 5):
            raise YZeroCharacterError("Value must be between 2 and 5 but was: %d" % value)
        if attribute != self.key_attribute:
            if value == 5:
                raise YZeroCharacterError("Only key attributes can have a value of 5")
        return DicePoolAttributeValue(value)

    def to_skill(self, skill, value):
        if not (0 <= value <= 3):
            raise YZeroCharacterError("Value must be between 0 and 3 but was: %d" % value)
        if skill not in self.associated_skills:
            if value == 3:
                raise YZeroCharacterError("Only associated skills can have a value of 3")
        return DicePoolSkillValue(value, skill.attribute)


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
        result_string = ""
        if self.value == 1:
            result_string = get_string("attribute_feeble")
        elif self.value == 2:
            result_string = get_string("attribute_below")
        elif self.value == 3:
            result_string = get_string("attribute_average")
        elif self.value == 4:
            result_string = get_string("attribute_capable")
        elif self.value == 5:
            result_string = get_string("attribute_extraordinary")
        return result_string + " (" + str(self.value) + ")"


class DicePoolSkillValue(AbstractValue):
    """ Dice pool value for skills with a value between 0 and 5."""

    def __init__(self, value, attribute, low_limit=0, high_limit=5):
        """ Sets the starting value for the attribute or skill. """
        super().__init__(value, low_limit, high_limit)
        self.attribute = attribute

    def roll(self):
        return roll_dice_pool_success(self.value + self.attribute.value, 6)

    def __str__(self):
        result_string = ""
        if self.value == 0:
            result_string = get_string("skill_none")
        elif self.value == 1:
            result_string = get_string("skill_novice")
        elif self.value == 2:
            result_string = get_string("skill_trained")
        elif self.value == 3:
            result_string = get_string("skill_experienced")
        elif self.value == 4:
            result_string = get_string("skill_veteran")
        elif self.value == 5:
            result_string = get_string("skill_elite")
        return result_string + " (" + str(self.value) + ")"
