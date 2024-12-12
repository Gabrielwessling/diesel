from typing import Tuple

import tcod
import numpy as np
import tcod.tcod  # type: ignore

base_codepoint = 0xE000

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((0, (0, 0, 0), (0, 0, 0)), dtype=graphic_dt)

floor_grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(1202, (220, 220, 220), (0, 0, 0)),
    light=(1202, (255, 255, 255), (0, 0, 0)),
)
floor_sand = new_tile(
    walkable=True,
    transparent=True,
    dark=(1201, (220, 220, 220), (0, 0, 0)),
    light=(1201, (255, 255, 255), (0, 0, 0)),
)
floor_water = new_tile(
    walkable=False,
    transparent=True,
    dark=(1200, (220, 220, 220), (0, 0, 0)),
    light=(1200, (255, 255, 255), (0, 0, 0)),
)
floor_stone = new_tile(
    walkable=True,
    transparent=True,
    dark=(1203, (220, 220, 220), (0, 0, 0)),
    light=(1203, (255, 255, 255), (0, 0, 0)),
)
floor_snow = new_tile(
    walkable=True,
    transparent=True,
    dark=(1204, (220, 220, 220), (0, 0, 0)),
    light=(1204, (255, 255, 255), (0, 0, 0)),
)
floor_dirt = new_tile(
    walkable=True,
    transparent=True,
    dark=(1205, (220, 220, 220), (0, 0, 0)),
    light=(1205, (255, 255, 255), (0, 0, 0)),
)
floor_error = new_tile(
    walkable=True,
    transparent=True,
    dark=(1135, (220, 220, 220), (200, 100, 0)),
    light=(1135, (255, 255, 255), (200, 100, 0)),
)

wall_stone = new_tile(
    walkable=False,
    transparent=False,
    dark=(301, (220, 220, 220), (0, 0, 0)),
    light=(301, (255, 255, 255), (0, 0, 0)),
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(304, (220, 220, 220), (0, 0, 0)),
    light=(304, (255, 255, 255), (0, 0, 0)),
)