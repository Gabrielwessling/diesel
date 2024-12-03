from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int = 1, base_defense: int = 0, base_power: int = 0, range: int = 0, dexterity: int = 0):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power
        self.base_range = range
        self.base_dexterity = dexterity

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value
        if amount_recovered >= 1:
            self.engine.player.skill_list.skills[3].add_xp(15)
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus
    
    @property
    def range(self) -> int:
        return self.base_range + self.range_bonus
    
    @property
    def dexterity(self) -> int:
        return self.base_dexterity + self.dexterity_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    @property
    def dexterity_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.dexterity_bonus
        else:
            return 0

    @property
    def range_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.range_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "Voce morreu!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} morreu!"
            death_message_color = color.enemy_die

        self.parent.char = "▲"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"restos de {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
        