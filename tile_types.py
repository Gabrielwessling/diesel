from typing import Tuple

import numpy as np  # type: ignore

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
SHROUD = np.array((ord(" "), (255, 255, 255), (100, 90, 60)), dtype=graphic_dt)

floor_grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (123, 154, 133), (154, 192, 166)),
    light=(ord(" "), (60, 220, 110), (100, 250, 150)),
)
floor_grass_alt = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("w"), (123, 154, 133), (154, 192, 166)),
    light=(ord("w"), (60, 220, 110), (100, 250, 150)),
)

wall_stone = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (179, 163, 143), (95, 85, 76)),
    light=(ord("#"), (200, 150, 90), (110, 80, 60)),
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)