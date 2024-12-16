from __future__ import annotations

import random
from typing import Optional, Tuple, TYPE_CHECKING

import categories.color as color
import exceptions
from entity import Chest
from categories.skills import WEAPON_SKILL_MAP, EquipmentType

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Chest

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()
    
class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it and it doesn't exceed the weight capacity."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                # Check if the item can fit in terms of capacity
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("You can't shove the item in your inventory.")

                # Check if the item can fit in terms of weight
                total_weight = sum(i.weight for i in inventory.items)
                if total_weight + item.weight > inventory.max_weight:
                    raise exceptions.Impossible("You're too weak to carry more.")

                # Add the item to the inventory
                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory

                inventory.items.append(item)

                self.engine.message_log.add_message(f"You get {item.name}")
                return

        raise exceptions.Impossible("You can't get the air.")
    
class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity)
        if item is None:
            raise ValueError("Item can't be None")
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)

class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)
        self.entity.inventory.drop(self.item)

class WaitAction(Action):
    def perform(self) -> None:
        pass

class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You descend the stairs.", color.descend
            )
        else:
            raise exceptions.Impossible("You can't descend into matter.")

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
    
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        
        #setting color
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
            
        if not target:
            raise exceptions.Impossible("You can't attack the air.")

        chance_to_hit = 70 + 2 * (self.entity.fighter.dexterity - target.fighter.dexterity)
        
        dice = random.randint(1, 100)
        
        if dice > chance_to_hit:
            self.engine.message_log.add_message(
                f"You miss.", attack_color
            )
            return
        
        damage = self.entity.fighter.power - target.fighter.defense
        
        extra_damage = int((random.randint(-self.entity.fighter.power, self.entity.fighter.power)) / 2)

        damage += extra_damage

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        

        if damage > 0:
            if self.entity is self.engine.player:
                self.engine.player.skill_list.skills["Martial Arts"].add_xp(15)
            if target is self.engine.player:
                self.engine.player.skill_list.skills["Pain Mastering"].add_xp(15)
            for skill_name, weapon_class in WEAPON_SKILL_MAP.items():
                item_seguro: Item = self.engine.player.equipment.slots[EquipmentType.HANDS]
                if item_seguro and item_seguro.equippable.equipment_type is weapon_class:
                    self.engine.player.skill_list.skills[skill_name].add_xp(15)
            extra_damage_message = ""
            if dice == 1:
                damage = damage*2
                extra_damage_message = " Critical!"
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} damage.{extra_damage_message}", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} for no damage.", attack_color
            )

class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("You try to walk outside boundaries. Do you think I'm stupid?")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("You try to walk into a wall, so I won't count it as a turn, dumbass.")
        blocking_entity = self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if blocking_entity:
            if isinstance(blocking_entity, Chest):
                if blocking_entity.breakable:
                    # Aqui você pode acessar métodos ou atributos da classe Chest
                    for item in blocking_entity.break_chest(self.engine.player):
                        item.spawn(self.engine.game_map, dest_x, dest_y)
                        item.parent = self.engine.game_map
                    self.engine.message_log.add_message("You broke the container!")
                    return  # Finaliza a ação após interagir com o baú
                else:
                    for item in blocking_entity.open(self.engine.player):
                        item.spawn(self.engine.game_map, dest_x, dest_y)
                        item.parent = self.engine.game_map
                    self.engine.message_log.add_message("You opened the container!")
                    return  # Finaliza a ação após interagir com o baú
            raise exceptions.Impossible("Blocked by an entity. Spooky!")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()