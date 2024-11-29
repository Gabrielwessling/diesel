from enum import auto, Enum


class DamageType(Enum):
    PIERCING = auto()    # Damage from stabbing or thrusting weapons (e.g., spears, arrows).
    SLASHING = auto()     # Damage from cutting weapons (e.g., swords, axes).
    BLUNT = auto()        # Damage from blunt-force weapons (e.g., maces, hammers).
    CRUSHING = auto()     # Damage from heavy, crushing force (e.g., boulders, falling objects).