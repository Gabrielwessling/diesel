from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int, max_weight: float):
        self.capacity = capacity
        self.max_weight = max_weight
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"Voce dropa {item.name}.")
        
    @property
    def key_items(self) -> dict[int, Item]:
        """
        Retorna um dicionário de itens no inventário que têm um key_id não nulo.
        A chave do dicionário é o key_id e o valor é o item.
        """
        return {item.key_id: item for item in self.items if item.key_id is not None}