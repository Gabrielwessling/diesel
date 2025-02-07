from __future__ import annotations

from typing import TYPE_CHECKING

import lzma
import pickle
import aiofiles  # For asynchronous file handling
from tcod.console import Console
from tcod.map import compute_fov
import tcod

import exceptions
from game_map import GameMap
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from entity_factories import EntityFactories
    from game_map import GameMap, GameWorld

class Engine:
    win_condition: bool = False
    game_map: GameMap
    heal_turn: int = 0
    game_world: GameWorld
    message_log: MessageLog

    def __init__(self, player: Actor, entity_factories: EntityFactories):
        self.message_log = MessageLog
        self.mouse_location = (0, 0)
        self.player = player
        self.message_log = MessageLog()
        self.entity_factories = entity_factories

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        if hasattr(self, "game_map"):
            offset_x = self.player.x - console.width // 2
            offset_y = self.player.y - console.height // 2
            # Renderiza o mapa ajustando os offsets.
            self.game_map.render(console, offset_x, offset_y)

        self.message_log.render(
            console=console,
            x=17,
            y=console.height - 7,  # Position 7 rows from the bottom
            width=console.width - 34,
            height=7,  # Display up to 7 lines of messages
        )
        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=15,
        )

        render_functions.render_names_at_mouse_location(console=console, x=0, y=0, engine=self)
        render_functions.render_dungeon_level_indicator(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 1),
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)