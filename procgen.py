from __future__ import annotations

import random
from categories.biomes import biomes
import config
from typing import Dict, Tuple, TYPE_CHECKING

import numpy as np
from PIL import Image

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
    seed: int,  # Adicionando heatmaps
    noise_scale: float = 100.0,  # Escala para o Perlin noise (não será mais usado)
) -> "GameMap":
    from game_map import GameMap  # Importação atrasada para evitar dependência circular
    """Gerar um novo mapa do mundo."""
    player = engine.player
    overworld = GameMap(engine, map_width, map_height, entities=[player])

    heightmap = generate_perlin_grid(config.WORLD_SIZE_X, config.WORLD_SIZE_Y, 200.0)
    humidity_map = generate_perlin_grid(config.WORLD_SIZE_X, config.WORLD_SIZE_Y, 200.0)
    temperature_map = generate_perlin_grid(config.WORLD_SIZE_X, config.WORLD_SIZE_Y, 200.0)
    
    # Preencher o mapa com base nos biomas
    for x in range(map_width):
        for y in range(map_height):
            biome = determine_biome(heightmap[x, y], humidity_map[x, y], temperature_map[x, y])
            overworld.tiles[x, y] = biome

    # Colocar o jogador no centro do mapa
    player_x, player_y = map_width // 2, map_height // 2
    player.place(player_x, player_y, overworld)

    return overworld