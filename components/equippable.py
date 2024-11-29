from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType
from damage_types import DamageType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        damage_type: DamageType,
        power_bonus: int = 0,
        range: int = 1,
        defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_type
        self.damage_type = damage_type
        self.range = range

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, damage_type=DamageType.PIERCING, power_bonus=2, range=1)

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, damage_type=DamageType.SLASHING, power_bonus=3, range=1)

class Spear(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, damage_type=DamageType.PIERCING, power_bonus=4, range=2)

class Hammer(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, damage_type=DamageType.BLUNT, power_bonus=2, range=1)

class Axe(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, damage_type=DamageType.SLASHING, power_bonus=3, range=1)

class Bow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, damage_type=DamageType.PIERCING, power_bonus=3, range=5)

class Pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, damage_type=DamageType.PIERCING, power_bonus=4, range=7)

class Rock(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.THROW_WEAPON, damage_type=DamageType.BLUNT, power_bonus=1, range=5)
