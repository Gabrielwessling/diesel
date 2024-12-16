import categories.tile_types as tile_types

class Biome:
    def __init__(self, name: str, elevation_range: tuple, humidity_range: tuple, temperature_range: tuple, tile_type):
        self.name = name
        self.elevation_range = elevation_range
        self.humidity_range = humidity_range
        self.temperature_range = temperature_range
        self.tile_type = tile_type

    def matches(self, elevation: float, humidity: float, temperature: float) -> bool:
        return (self.elevation_range[0] <= elevation <= self.elevation_range[1] and
                self.humidity_range[0] <= humidity <= self.humidity_range[1] and
                self.temperature_range[0] <= temperature <= self.temperature_range[1])

# Define biomes with their ranges and associated tile type
biomes = [
    Biome("Water", (0, 0.3), (0, 1), (-10, 0), tile_types.floor_water),
    Biome("Stone", (0.3, 1), (0, 0.3), (0, 30), tile_types.floor_stone),
    Biome("Grass", (0.4, 1), (0.4, 1), (0, 30), tile_types.floor_grass),
    Biome("Sand", (0.3, 0.7), (0, 0.3), (20, 50), tile_types.floor_sand),
    Biome("Dirt", (0.3, 0.4), (0.3, 0.4), (0, 50), tile_types.floor_dirt),
    Biome("Snow", (0.3, 1), (0.6, 1), (-10, 10), tile_types.floor_snow),
    Biome("Swamp", (0.3, 0.6), (0.3, 0.6), (0.2, 0.5), tile_types.floor_swamp),
    Biome("Shrubland", (0.4, 0.7), (0.3, 0.4), (0.3, 0.6), tile_types.floor_shrubland),
    Biome("Marsh", (0.2, 0.4), (0.5, 0.7), (0.3, 0.5), tile_types.floor_marsh),
    Biome("Savanna", (0.5, 0.7), (0.3, 0.5), (0.4, 0.7), tile_types.floor_savanna)
]