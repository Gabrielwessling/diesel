from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import tcod
import categories.color as color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def render_names_at_mouse_location(
    console: tcod.console.Console, x: int, y: int, engine: Engine
) -> None:
    if not hasattr(engine, "game_map"):
        return

    # Get mouse location
    mouse_x, mouse_y = engine.mouse_location

    # Calculate the size of each tile
    tile_width = console.width // engine.game_map.width or 1
    tile_height = console.height // engine.game_map.height or 1

    # Map mouse position to game map coordinates
    map_mouse_x = mouse_x // tile_width + (engine.player.x - console.width // 2)
    map_mouse_y = mouse_y // tile_height + (engine.player.y - console.height // 2)

    # Check if the calculated position is in bounds
    if not engine.game_map.in_bounds(map_mouse_x, map_mouse_y):
        return

    # Get the names at the adjusted position
    names_at_mouse_location = get_names_at_location(
        x=map_mouse_x, y=map_mouse_y, game_map=engine.game_map
    )

    # Print the names to the console
    if names_at_mouse_location:
        console.print(x=x, y=y, bg=color.black, string=names_at_mouse_location)
    
def render_bar(
    console: tcod.console.Console,
    current_value: int,
    maximum_value: int,
    total_width: int
) -> None:
    """
    Renders a health bar or similar status bar at the bottom of the screen.
    """
    # Calculate the width of the filled portion of the bar
    bar_width = int(float(current_value) / maximum_value * total_width)

    # Draw the empty bar
    console.draw_rect(x=1, y=console.height - 7, width=total_width, height=1, ch=0, bg=color.bar_empty)

    # Draw the filled portion of the bar
    if bar_width > 0:
        console.draw_rect(
            x=1, y=console.height - 7, width=bar_width, height=1, ch=0, bg=color.bar_filled
        )

    # Print the bar's text (e.g., HP: 20/30)
    console.print(
        x=1, y=console.height - 7, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )

def render_dungeon_level_indicator(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """
    Render the current dungeon level at the specified location.
    """
    x, y = location

    console.print(
        x=x, 
        y=y, 
        bg=color.black, 
        string=f"Floor: {(dungeon_level * -1) + 1}"
    )