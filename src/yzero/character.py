from src.yzero.errors import YZeroCharacterError
from src.yzero.values import AbstractValue


class Character:
    """
    Abstract class for all year zero engine characters.
    """
    def __init__(self, attributes, skills, archetype=None, specialities=None, items=None, traits=None,
                 gear=None, name=None):
        self.attributes = attributes
        self.skills = skills
        self.archetype = archetype
        if specialities is None:
            specialities = []
        self.specialities = specialities
        if items is None:
            items = []
        self.items = items
        if traits is None:
            traits = []
        self.traits = traits
        if gear is None:
            gear = []
        self.gear = gear
        self.name = name
        self.health_pool = None
        self.resolve_pool = None

    def set_attribute(self, attribute, value):
        """Replaces existing attribute value with new attribute."""
        if attribute not in self.attributes:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        if not isinstance(value, AbstractValue):
            raise YZeroCharacterError("Value must be an instance of AbstractValue")
        self.attributes[attribute] = value

    def update_attribute(self, attribute, value):
        """Replaces existing attribute value with new attribute value."""
        if attribute not in self.attributes:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        self.attributes[attribute].set_value(value)

    def adjust_attribute(self, attribute, value):
        """Adjust existing attribute value by adding or subtracting value."""
        if attribute not in self.attributes:
            raise YZeroCharacterError("Attribute %s does not exist" % attribute)
        self.attributes[attribute].adjust(value)

    def set_skill(self, skill_template, value):
        """Replaces existing skill value with new skill."""
        if skill_template not in self.skills:
            raise YZeroCharacterError("Skill %s does not exist" % skill_template.name)
        if not isinstance(value, AbstractValue):
            raise YZeroCharacterError("Value must be an instance of AbstractValue")
        self.skills[skill_template.name] = value

    def update_skill(self, skill, value):
        """Replaces existing skill value with new skill value."""
        if skill not in self.skills:
            raise YZeroCharacterError("Skill %s does not exist" % skill)
        self.skills[skill].set_value(value)

    def adjust_skill(self, skill, value):
        """Adjust existing skill value by adding or subtracting value."""
        self.skills[skill].adjust(value)

    def set_archetype(self, archetype):
        self.archetype = archetype

    def add_speciality(self, speciality):
        self.specialities.append(speciality)

    def add_trait(self, trait):
        self.traits.append(trait)

    def add_item(self, item):
        self.gear.append(item)

    def print_attributes(self):
        for key, value in self.attributes.items():
            print(str(key) + ": " + str(value))

    def print_skills(self):
        for key, value in self.skills.items():
            if value.value > 0:
                print(str(key) + ": " + str(value))

    def print(self):
        print("\n################")
        print("Name: " + self.name)
        print("Archetype: " + self.archetype.name)
        print("\nAttributes:")
        self.print_attributes()
        print("\nSkills:")
        self.print_skills()
        print("\nSpecialities:")
        for speciality in self.specialities:
            print(speciality)
        print("\ntraits:")
        for trait in self.traits:
            print(trait)
        print("\nGear:")
        for item in self.gear:
            print(str(item))
        print("Health pool: " + str(self.health_pool.current) + "/" + str(self.health_pool.limit))
        print("Resolve pool: " + str(self.resolve_pool.current) + "/" + str(self.resolve_pool.limit))


class Archetype:
    def __init__(self, name, key_attribute, associated_skills):
        self.name = name
        self.key_attribute = key_attribute
        if associated_skills is None:
            associated_skills = []
        self.associated_skills = associated_skills
