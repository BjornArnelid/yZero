from src.yzero import defaults
from src.yzero.errors import YZeroCharacterError


class AbstractCharacter:
    def __init__(self, archetype=None, specialities=None, items=None, traits=None, gear=None, name=None):
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

    def add_speciality(self, speciality):
        self.specialities.append(speciality)

    def add_trait(self, trait):
        self.traits.append(trait)

    def add_item(self, item):
        self.gear.append(item)

    def print_attributes(self):
        raise YZeroCharacterError("Method not implemented")

    def print_skills(self):
        raise YZeroCharacterError("Method not implemented")

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


class Archetype:
    def __init__(self, name, key_attribute, associated_skills):
        self.name = name
        self.key_attribute = key_attribute
        if associated_skills is None:
            associated_skills = []
        self.associated_skills = associated_skills
