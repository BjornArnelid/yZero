# Attributes
from src.yzero.translation import get_string

class AttributeTemplate:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return get_string(self.name)


STRENGTH = AttributeTemplate('attribute_strength')
AGILITY = AttributeTemplate('attribute_agility')
WITS = AttributeTemplate('attribute_wits')
EMPATHY = AttributeTemplate('attribute_empathy')
ATTRIBUTES = [STRENGTH, AGILITY, WITS, EMPATHY]


class SkillTemplate:
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    def __str__(self):
        return get_string(self.name)

# Skills
FORCE = SkillTemplate("skill_force", STRENGTH)
MELEE = SkillTemplate("skill_melee", STRENGTH)
STAMINA = SkillTemplate("skill_stamina", STRENGTH)
MARKSMANSHIP = SkillTemplate("skill_marksmanship", AGILITY)
MOBILITY = SkillTemplate("skill_mobility", AGILITY)
STEALTH = SkillTemplate("skill_stealth", AGILITY)
CRAFTING = SkillTemplate("skill_crafting", WITS)
OBSERVATION = SkillTemplate("skill_observation", WITS)
SURVIVAL = SkillTemplate("skill_survival", WITS)
HEALING = SkillTemplate("skill_healing", EMPATHY)
INSIGHT = SkillTemplate("skill_insight", EMPATHY)
PERSUASION = SkillTemplate("skill_persuasion", EMPATHY)
SKILLS = [FORCE, MELEE, STAMINA, MARKSMANSHIP, MOBILITY, STEALTH, CRAFTING, OBSERVATION, SURVIVAL, HEALING, INSIGHT, PERSUASION]


# Specialities
BODYGUARD = 'Bodyguard'
COMPASSION = 'Compassion'
FAST_REFLEXES = 'Fast Reflexes'
FIELD_SURGEON = 'Field Surgeon'
FLYWEIGHT = 'Flyweight'
GUT_FEELING = 'Gut Feeling'
HARDENED = 'Hardened'
HARD_HITTER = 'Hard Hitter'
HEALER = 'Healer'
INQUISITIVE = 'Inquisitive'
KILLER = 'Killer'
LUCKY = 'Lucky'
MENACING = 'Menacing'
MERCILESS = 'Merciless'
MUSICIAN = 'Musician'
PACK_MULE = 'Pack Mule'
QUICK_DRAW = 'Quick Draw'
RECKLESS = 'Reckless'
SECOND_WIND = 'Second Wind'
SNIPER = 'Sniper'
TOUGH = 'Tough'
TRUE_GRIT = 'True Grit'
WEAPON_SPECIALIST = 'Weapon Specialist'