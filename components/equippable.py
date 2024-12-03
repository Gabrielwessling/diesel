from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from components.base_component import BaseComponent
from equipment_types import EquipmentType
from damage_types import DamageType
from armor_types import ArmorType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    """Componente base para itens que podem ser equipados."""
    def __init__(self, equipment_type: EquipmentType, parent: Optional[Item] = None):
        self.equipment_type = equipment_type
        if parent:
            self.parent = parent

class Weapon(Equippable):
    """Componente para armas."""
    def __init__(self, damage_type: DamageType, power_bonus: int, dexterity_bonus: int, equipment_type: EquipmentType, parent: Item, range: int = 1):
        super().__init__(parent)
        self.equipment_type = equipment_type
        self.damage_type = damage_type
        self.power_bonus = power_bonus
        self.dexterity_bonus = dexterity_bonus
        self.range = range


class Armor(Equippable):
    """Componente para armaduras."""
    def __init__(self, armor_type: ArmorType, defense_bonus: int, dexterity_bonus: int, parent: Item, equipment_type: EquipmentType):
        super().__init__(parent)
        self.equipment_type = equipment_type
        self.armor_type = armor_type
        self.dexterity_bonus = dexterity_bonus
        self.defense_bonus = defense_bonus

#|____________________________________________________ WEAPONS ________________________________________________________|

class Dagger(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.PIERCING, power_bonus=2, dexterity_bonus=4, range=1)

class Sword(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.SLASHING, power_bonus=3, dexterity_bonus=2, range=1)

class Spear(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.PIERCING, power_bonus=4, dexterity_bonus=0, range=2)

class Hammer(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.BLUNT, power_bonus=2, dexterity_bonus=3, range=1)

class Axe(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.SLASHING, power_bonus=3, dexterity_bonus=1, range=1)

class Bow(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.PIERCING, power_bonus=3, dexterity_bonus=0, range=5)

class Pistol(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.PIERCING, power_bonus=2, dexterity_bonus=2, range=5)

class Rifle(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.PIERCING, power_bonus=6, dexterity_bonus=1, range=10)

class Launcher(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.CRUSHING, power_bonus=2, dexterity_bonus=5, range=7)

class Throwable(Weapon):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, parent=parent, damage_type=DamageType.BLUNT, power_bonus=1, dexterity_bonus=2, range=5)


#|____________________________________________________ CLOTHING AND ARMOR ________________________________________________________|

# Roupas (Clothing) para TORSO
class Shirt(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.TORSO, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para TORSO
class Light_Body_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.TORSO, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=2)

class Medium_Body_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.TORSO, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=4)

class Heavy_Body_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.TORSO, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=6)


# Roupas (Clothing) para BRAÇOS
class Arm_Band(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.ARMS, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para BRAÇOS
class Light_Arm_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.ARMS, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=1)

class Medium_Arm_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.ARMS, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=3)

class Heavy_Arm_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.ARMS, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=5)


# Roupas (Clothing) para PÉS
class Footwear(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.FEET, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para PÉS
class Light_Sabatons(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.FEET, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=1)

class Medium_Sabatons(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.FEET, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=2)

class Heavy_Sabatons(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.FEET, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=3)


# Roupas (Clothing) para LUVA
class Gloves(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.GLOVES, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para LUVA
class Light_Glove_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.GLOVES, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=1)

class Medium_Glove_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.GLOVES, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=2)

class Heavy_Glove_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.GLOVES, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=3)


# Roupas (Clothing) para PERNAS
class Leggings(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.LEGS, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para PERNAS
class Light_Leg_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.LEGS, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=2)

class Medium_Leg_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.LEGS, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=4)

class Heavy_Leg_Armor(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.LEGS, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=6)


# Roupas (Clothing) para CABEÇA
class Head_Clothing(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HEAD, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para CABEÇA
class Light_Helmet(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HEAD, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=1)

class Medium_Helmet(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HEAD, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=2)

class Heavy_Helmet(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.HEAD, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=3)


# Roupas (Clothing) para OMBREIRAS
class Shoulder_Clothing(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.SHOULDERS, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

# Armaduras leves, médias e pesadas para OMBREIRAS
class Light_Shoulder_Pads(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.SHOULDERS, parent=parent, armor_type=ArmorType.LIGHT, dexterity_bonus=1, defense_bonus=1)

class Medium_Shoulder_Pads(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.SHOULDERS, parent=parent, armor_type=ArmorType.MEDIUM, dexterity_bonus=0, defense_bonus=2)

class Heavy_Shoulder_Pads(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.SHOULDERS, parent=parent, armor_type=ArmorType.HEAVY, dexterity_bonus=-1, defense_bonus=4)

# Acessórios (Rings, Necklace, Tabard)
class Ring(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.RING, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

class Necklace(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.NECKLACE, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

class Tabard(Armor):
    def __init__(self, parent: Item) -> None:
        super().__init__(equipment_type=EquipmentType.TABARD, parent=parent, armor_type=ArmorType.CLOTHING, dexterity_bonus=2, defense_bonus=0)

