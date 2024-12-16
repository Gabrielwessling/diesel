from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from components.base_component import BaseComponent
from categories.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, **slots: Optional[Item]):
        """
        Initialize an equipment object. Supports assigning items to specific slots like weapon, armor, head, etc.

        :param slots: Optional equipment items to be assigned to specific slots.
        """
        # Initialize all equipment slots as None
        self.slots = {slot: None for slot in EquipmentType}

        # Assign each passed item to the corresponding slot
        for slot, item in slots.items():
            if isinstance(slot, EquipmentType) and isinstance(item, Item):
                self.slots[slot] = item
            else:
                raise ValueError(f"Invalid equipment slot or item: {slot}, {item}")

    @property
    def defense_bonus(self) -> int:
        bonus = 0
        for slot, item in self.slots.items():
            if item and item.equippable and item.equippable.equipment_type is not EquipmentType.HANDS:
                bonus += item.equippable.defense_bonus
        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0
        for slot, item in self.slots.items():
            if item and item.equippable and item.equippable.equipment_type is EquipmentType.HANDS:
                bonus += item.equippable.power_bonus
        return bonus

    @property
    def range_bonus(self) -> int:
        bonus = 0
        for slot, item in self.slots.items():
            if item and item.equippable and item.equippable.equipment_type is EquipmentType.HANDS:
                bonus += item.equippable.range
        return bonus
    
    @property
    def dexterity_bonus(self) -> int:
        bonus = 0
        for slot, item in self.slots.items():
            if item and item.equippable:
                bonus += item.equippable.dexterity_bonus
        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        # Check if the item is equipped in any slot
        return any(item == equipped_item for equipped_item in self.slots.values())

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip {item_name}."
        )

    def equip_to_slot(self, slot: EquipmentType, item: Item, add_message: bool) -> None:
        current_item = self.slots[slot]

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        self.slots[slot] = item

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: EquipmentType, add_message: bool) -> None:
        current_item = self.slots[slot]

        if add_message and current_item:
            self.unequip_message(current_item.name)

        self.slots[slot] = None

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        print(f"Equippable item: {equippable_item}")
        print(f"Equippable: {equippable_item.equippable if equippable_item.equippable else 'None'}")
        if equippable_item.equippable:  # Ensure equippable_item has an equippable attribute
            equipment_type = equippable_item.equippable.equipment_type
            if self.slots[equipment_type] == equippable_item:
                self.unequip_from_slot(equipment_type, add_message)
            else:
                self.equip_to_slot(equipment_type, equippable_item, add_message)
        else:
            raise ValueError(f"{equippable_item.name} is not equippable.")