from __future__ import annotations

import random
from categories.biomes import biomes
import config
from typing import Dict, Tuple, TYPE_CHECKING

import numpy as np
from PIL import Image
import threading
import time
import tcod

import categories.tile_types as tile_types

if TYPE_CHECKING:
    from engine import Engine

def generate_perlin_grid(width: int, height: int, scale: float) -> np.ndarray:
    """Generate a 2D Perlin noise grid."""
    from perlin_noise import perlin_noise
    seed=random.randint(1, 9999999)
    perlin = perlin_noise.PerlinNoise(octaves=8, seed=seed)
    grid = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            grid[x, y] = perlin((x/scale, y/scale))

    # Avoid division by zero during normalization
    grid_min, grid_max = np.min(grid), np.max(grid)
    if grid_max != grid_min:
        grid = (grid - grid_min) / (grid_max - grid_min)  # Normalize to [0, 1]
    else:
        grid = np.zeros_like(grid)  # If all values are the same, return a grid of zeros

    return grid


def determine_biome(elevation: float, humidity: float, temperature: float):
    """Determine the biome based on elevation, humidity, and temperature."""
    for biome in biomes:
        if biome.matches(elevation, humidity, temperature):
            return biome.tile_type
    # Default to grass if no biome matches
    print (f"Error made with height:{elevation.__format__("0.00")} temp:{temperature.__format__("0.00")} humid:{humidity.__format__("0.00")}")
    return tile_types.floor_error


def generate_overworld(
    map_width: int,
    map_height: int,
    engine: Engine,
    seed: int,
    noise_scale: float = 100.0,
) -> "GameMap":  # type: ignore
    from game_map import GameMap  # Importação atrasada para evitar dependência circular

    player = engine.player
    overworld = GameMap(engine, map_width, map_height, entities=[player])

    # Gerar mapas de Perlin noise
    heightmap = generate_perlin_grid(config.WORLD_SIZE_X, config.WORLD_SIZE_Y, 500.0)
    humidity_map = generate_perlin_grid(config.WORLD_SIZE_X, config.WORLD_SIZE_Y, 500.0)
    temperature_map = generate_perlin_grid(config.WORLD_SIZE_X, config.WORLD_SIZE_Y, 500.0)

    def draw_loading_screen(console: tcod.console.Console, progress: int) -> None:
        """Desenha a tela de carregamento com uma barra de progresso."""
        console.clear()
        console.print(x=1, y=1, string="Generating Overworld...", fg=(255, 255, 255))
        bar_width = int((progress / 100) * (console.width - 2))
        console.draw_rect(x=1, y=3, width=console.width - 2, height=1, ch=ord(" "), bg=(100, 100, 100))
        console.draw_rect(x=1, y=3, width=bar_width, height=1, ch=ord(" "), bg=(0, 200, 50))
        console.print(x=console.width // 2 - 5, y=5, string=f"{progress}%", fg=(255, 255, 255))

    for x in range(map_width):
        for y in range(map_height):
            biome = determine_biome(heightmap[x, y], humidity_map[x, y], temperature_map[x, y])
            overworld.tiles[x, y] = biome
            draw_loading_screen(tcod.console.Console, (x * map_height + y) / (map_width * map_height) * 100)

    # Colocar o jogador no centro do mapa
    player_x, player_y = map_width // 2, map_height // 2
    player.place(player_x, player_y, overworld)

    return overworld