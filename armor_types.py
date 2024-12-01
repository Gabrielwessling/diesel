from enum import auto, Enum


class ArmorType(Enum):
    CLOTHING = auto()    # Damage from stabbing or thrusting weapons (e.g., spears, arrows).
    LIGHT = auto()     # Damage from cutting weapons (e.g., swords, axes).
    MEDIUM = auto()        # Damage from blunt-force weapons (e.g., maces, hammers).
    HEAVY = auto()     # Damage from heavy, crushing force (e.g., boulders, falling objects).