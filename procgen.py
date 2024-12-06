from __future__ import annotations

import random
import math
from typing import Iterator, List, Tuple, TYPE_CHECKING, Dict

import numpy as np
import tcod

from entity_factories import EntityFactories
from game_map import GameMap
import tile_types
from entity import Chest, Item, Actor


if TYPE_CHECKING:
    from engine import Engine

entity_factories: EntityFactories
entity_factories: Engine.entity_factories

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int, engine: Engine):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.engine = engine

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def place_entities(
    room: RectangularRoom, dungeon: GameMap, maximum_monsters: int, maximum_items: int, maximum_chests: int, entity_factories: EntityFactories, monsters_with_chance: Dict[Actor, float]
) -> None:
    number_of_monsters = random.randint(0, maximum_monsters)
    number_of_items = random.randint(0, maximum_items)
    number_of_chests = random.randint(0, maximum_chests)

    monster_list = list(monsters_with_chance.keys())
    weight_list = list(monsters_with_chance.values())
    chosen_monsters = random.choices(monster_list, weights=weight_list, k=number_of_monsters)

    # Debug: mostrar monstros escolhidos
    print(f"Chosen monsters: {[monster.name for monster in chosen_monsters]}")

    # Posicionar monstros no mapa
    for entity in chosen_monsters:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(existing_entity.x == x and existing_entity.y == y for existing_entity in dungeon.entities):
            entity.parent = dungeon
            entity.spawn(dungeon, x, y)

    # Place items on the map
    for i in range(number_of_items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            dice = random.randint(0, len(entity_factories.items) - 1)
            entity: Item = entity_factories.items[dice]
            entity.parent = dungeon
            entity.spawn(dungeon, x, y)

    # Place chests on the map
    for i in range(number_of_chests):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            dice = random.randint(0, 100)
            if dice >= 90:
                entity: Chest = entity_factories.chests[0]
                entity.parent = dungeon
                entity.spawn(dungeon, x, y)

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def modify_floor_tiles(dungeon: GameMap) -> None:
    """Modify all floor tiles of the dungeon with some chance of alternation."""
    chance_of_alt_tile = 0.02  # Adjust probability as needed

    # Create a random mask for the entire dungeon
    random_mask = np.random.rand(*dungeon.tiles.shape) < chance_of_alt_tile

    # Apply alternation only to tiles that are `floor_grass`
    floor_mask = dungeon.tiles == tile_types.floor_grass  # Identify all floor tiles
    alternation_mask = random_mask & floor_mask  # Combine the random mask with the floor mask

    # Apply alternate tiles where the mask is True
    dungeon.tiles[alternation_mask] = tile_types.floor_grass_alt

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    max_items_per_room: int,
    max_chests_per_room: int,
    engine: Engine,
    current_floor: int,  # Adicionado
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    entity_factories = engine.entity_factories
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)
    level_chest: Chest
    level_chest = entity_factories.chests[0].spawn(dungeon, center_of_last_room[0] + 2, center_of_last_room[1] + 2)

    # Gerar as salas e conectar com túneis
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height, engine)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # Esta sala intersecta, então tente novamente

        dungeon.tiles[new_room.inner] = tile_types.floor_grass

        for room in rooms:
            modify_floor_tiles(dungeon)

        center_of_last_room = new_room.center

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor_grass

        rooms.append(new_room)

    # Now that the dungeon is generated, we can generate the entities
    monsters_with_chance: Dict[Actor, float] = {}  # Now using a dictionary
 
    # define monsters as keys and their chances as values in a dictionary monsters_with_chance    
    for monster in entity_factories.monsters:
        monster: Actor

        SC = monster.spawn_curve
        
        if engine.game_world.current_floor < monster.spawn_curve.peak_floor:
            chance = get_spawn_probability(SC.min_prob, SC.peak_prob, SC.start_floor, SC.peak_floor, SC.end_floor, engine.game_world.current_floor, True)
        else:
            chance = get_spawn_probability(SC.min_prob, SC.peak_prob, SC.start_floor, SC.peak_floor, SC.end_floor, engine.game_world.current_floor, False)

        if chance < 0: chance = 0

        monsters_with_chance[monster] = chance
        
        print(f"{monster.name}: chance ajustada = {chance:.4f}")
        
    for room in rooms:
        place_entities(room, dungeon, max_monsters_per_room, max_items_per_room, max_chests_per_room, entity_factories, monsters_with_chance)

    dungeon.tiles[center_of_last_room] = tile_types.down_stairs
    dungeon.downstairs_location = center_of_last_room

    level_chest.x = center_of_last_room[0] + 2
    level_chest.y = center_of_last_room[1] + 2

    dice_locked = random.randint(1, 100)

    if dice_locked >= 80:
        level_chest.breakable = False
        level_chest.locked = True
        level_chest.chest_id = random.randint(1, 100)
        open_tiles = dungeon.get_locations_of_tile(tile_types.floor_grass)
        if open_tiles:
            chosen_location = random.choice(open_tiles)
            key_chest: Item = entity_factories.key_items[0].spawn(
                dungeon,
                x=chosen_location[0],
                y=chosen_location[1]
            )
            key_chest.key_id = level_chest.chest_id
    else:
        level_chest.locked = False
        level_chest.breakable = True

    if level_chest.locked: 
        number_of_items = random.randint(3, 6) 
    else:
        number_of_items = random.randint(1, 5)

    for _ in range(number_of_items):
        chosen_item = random.choice(entity_factories.items)
        level_chest.items.append(chosen_item)
    
    return dungeon

def get_spawn_probability(min: int, peak:int, startint_floor:int, peak_floor:int, ending_floor:int, current:int, rising: bool) -> float:
    if rising:
        probability = min + (peak-min) * (current - startint_floor) / (peak_floor - startint_floor)
    else:
        probability = peak - (peak-min) * (current - peak_floor) / (ending_floor - peak_floor)
    
    return probability