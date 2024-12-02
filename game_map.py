from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import numpy as np  # type: ignore
from tcod.console import Console
import gc

import tile_types
import entity as ENT

if TYPE_CHECKING:
    from entity import Entity, Actor, Item
    from engine import Engine

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        print (f" - Initializing GameMap...")
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall_stone, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

        self.downstairs_location = (0, 0)
        print (f" - GameMap Initialized, {len(self.tiles)} tiles...")

    @property
    def actors(self) -> Iterator[ENT.Actor]:
        """Iterate over this map's living actors."""
        print (f" - Iterating over living ACTORS inside map...")
        yield from (entity for entity in self.entities if isinstance(entity, ENT.Actor) and entity.is_alive)

    @property
    def items(self) -> Iterator[ENT.Item]:
        """Iterate over items on this map."""
        print (f" - Iterating over ITEMS inside map...")
        yield from (entity for entity in self.entities if isinstance(entity, ENT.Item))

    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[Entity]:
        """Get a blocking entity at a location."""
        print (f" - Getting blocking ENTITY at location x:{x} y:{y}...")
        return next(
            (entity for entity in self.entities if entity.blocks_movement and entity.x == x and entity.y == y),
            None,
        )

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        """Get an actor at a specific location."""
        print (f" - Getting ACTOR at location x:{x} y:{y}...")
        return next((actor for actor in self.actors if actor.x == x and actor.y == y), None)

    def get_locations_of_tile(self, tile_type) -> list[tuple[int, int]]:
        """
        Return a list of all locations in the map that have the specified tile type.
        """
        print (f" - Getting list of all locations in the map that have {tile_type} tiles...")
        LIST = [tuple(loc) for loc in np.argwhere(self.tiles == tile_type)]
        for i in range(len(LIST)):
            print (f" - x:{LIST[i][0]} y:{LIST[i][1]} ...")
        return LIST

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            (entity for entity in self.entities if self.visible[entity.x, entity.y]),
            key=lambda x: x.render_order.value,
        )
        for entity in entities_sorted_for_rendering:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)


class GameWorld:
    """
    Holds the settings for the GameMap and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        max_monsters_per_room: int,
        max_items_per_room: int,
        current_floor: int = 0,
    ):
        self.engine = engine
        self.map_width = map_width
        self.map_height = map_height
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_monsters_per_room = max_monsters_per_room
        self.max_items_per_room = max_items_per_room
        self.current_floor = current_floor

    def generate_floor(self) -> None:
        """Generate a new floor, increasing the floor count."""
        from procgen import generate_dungeon

        self.current_floor += 1

        # Limpa o mapa anterior para evitar referências persistentes.
        if hasattr(self.engine, "game_map"):
            self.engine.game_map.entities.clear()
            del self.engine.game_map

        gc.collect()
        for obj in gc.garbage:
            print(obj)
            
        # Gera o novo mapa.
        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            max_monsters_per_room=self.max_monsters_per_room,
            max_items_per_room=self.max_items_per_room,
            max_chests_per_room=1,
            engine=self.engine,
        )