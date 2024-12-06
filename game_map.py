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
        print (f"\n - Initializing GameMap...")
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
        yield from (entity for entity in self.entities if isinstance(entity, ENT.Actor) and entity.is_alive)

    @property
    def items(self) -> Iterator[ENT.Item]:
        """Iterate over items on this map."""
        yield from (entity for entity in self.entities if isinstance(entity, ENT.Item))

    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[Entity]:
        """Get a blocking entity at a location."""
        return next(
            (entity for entity in self.entities if entity.blocks_movement and entity.x == x and entity.y == y),
            None,
        )

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        """Get an actor at a specific location."""
        return next((actor for actor in self.actors if actor.x == x and actor.y == y), None)

    def get_locations_of_tile(self, tile_type) -> list[tuple[int, int]]:
        """
        Return a list of all locations in the map that have the specified tile type.
        """
        print (f" - Getting list of all locations in the map that have {tile_type} tiles...")
        LIST = [tuple(loc) for loc in np.argwhere(self.tiles == tile_type)]
        return LIST

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console, offset_x: int = 0, offset_y: int = 0) -> None:
        """
        Renderiza o mapa, preenchendo áreas fora das tiles com SHROUD.
        """
        # Preenche todo o console com SHROUD antes de renderizar
        console.rgb[:, :] = tile_types.SHROUD

        # Define os limites do console
        console_width, console_height = console.width, console.height

        # Itera sobre cada posição do console
        for x in range(console_width):
            for y in range(console_height):
                # Calcula a posição no mapa correspondente ao console (ajustada pelo offset)
                map_x = x + offset_x
                map_y = y + offset_y

                # Verifica se a posição está dentro dos limites do mapa
                if 0 <= map_x < self.width and 0 <= map_y < self.height:
                    if self.visible[map_x, map_y]:
                        tile = self.tiles["light"][map_x, map_y]
                    elif self.explored[map_x, map_y]:
                        tile = self.tiles["dark"][map_x, map_y]
                    else:
                        tile = tile_types.SHROUD

                    # Atualiza a posição do console com o tile correspondente
                    console.rgb[x, y] = tile

        # Ordena as entidades com base no render_order
        sorted_entities = sorted(self.entities, key=lambda entity: entity.render_order.value)

        # Renderiza as entidades ordenadas
        for entity in sorted_entities:
            # Verifica se a entidade está dentro dos limites do mapa e visível
            if 0 <= entity.x < self.width and 0 <= entity.y < self.height and self.visible[entity.x, entity.y]:
                draw_x = entity.x - offset_x
                draw_y = entity.y - offset_y

                # Renderiza apenas se a entidade estiver dentro do console
                if 0 <= draw_x < console.width and 0 <= draw_y < console.height:
                    console.print(
                        x=draw_x,
                        y=draw_y,
                        string=entity.char,
                        fg=entity.color,
                    )

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
            current_floor=self.current_floor,  # Passar o andar atual
        )