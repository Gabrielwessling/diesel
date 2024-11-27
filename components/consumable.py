from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import components.ai
import color
from components.base_component import BaseComponent
import components.inventory
from exceptions import Impossible
from input_handlers import (
    ActionOrHandler,
    SquareAreaRangedAttackHandler,
    CircleAreaRangedAttackHandler,
    SingleRangedAttackHandler,
)

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()
    
    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)

class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("Você não tá vendo esse tile.")
        if not target:
            raise Impossible("Você deve selecionar um inimigo.")
        if target is consumer:
            raise Impossible("Você não pode se confundir!")

        self.engine.message_log.add_message(
            f"Os olhos de {target.name} estão distantes, e ele comeca a trupicar!",
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
        )
        self.consume()

class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"Voce consome {self.parent.name} e recupera {amount_recovered} HP!",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"Vida ja esta cheia.")

class FireballDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> CircleAreaRangedAttackHandler:
        self.engine.message_log.add_message(
            "Selecione um local alvo.", color.needs_target
        )
        return CircleAreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("Voce nao esta vendo a area.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"{actor.name} grita de dor enquanto ve sua pele queimar e derreter, levando {self.damage} de dano!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("Sem alvos no local.")
        self.consume()

class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"Uma corrente de eletricidade atinge {target.name} com um som de mil morcegos, dando {self.damage} de dano!"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("Não existe alvo próximo.")