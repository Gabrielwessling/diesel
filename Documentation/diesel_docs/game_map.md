# **Documentation for `game_map.py`**

## **Overview**

The `game_map.py` module defines the `GameMap` and `GameWorld` classes, which handle the representation, logic, and generation of the game world. It manages the placement and rendering of tiles and entities, tracks exploration and visibility, and generates new levels.

---

## **Requirements**

### **Dependencies**

- **Third-Party Libraries**:
    - `numpy`: For managing map tiles and computational efficiency.
    - `tcod`: Used for console rendering.
- **Custom Modules**:
    - **`tile_types`**: Defines tile types (e.g., walls, floors, shrouded areas).
    - **`entity`**: Contains the definitions for entities like `Actor` and `Item`.
- **Standard Libraries**:
    - `typing`: Provides type hints for iterables, optional values, and circular dependencies.

---

## **Key Components**

### **1. GameMap Class**

The `GameMap` class handles the core map functionality, including tile storage, entity management, and rendering.

#### **Attributes**

- **`engine`** (`Engine`): Reference to the game engine.
- **`width, height`** (`int`): Dimensions of the map.
- **`entities`** (`set[Entity]`): Set of all entities present on the map.
- **`tiles`** (`numpy.ndarray`): 2D array storing tile data for the map.
- **`visible`** (`numpy.ndarray`): Boolean array indicating tiles the player can currently see.
- **`explored`** (`numpy.ndarray`): Boolean array indicating tiles the player has seen.
- **`downstairs_location`** (`tuple[int, int]`): Coordinates of the stairs to the next floor.

---

#### **Properties**

- **`gamemap`**: Returns `self` for compatibility with `Entity`'s `gamemap` attribute.
- **`actors`**: Iterator over all living actors on the map.
- **`items`**: Iterator over all items on the map.

---

#### **Methods**

##### **`__init__`**

- **Purpose**: Initializes a new game map.
- **Parameters**:
    - `engine`: The game engine instance.
    - `width, height`: Dimensions of the map.
    - `entities`: Optional iterable of initial entities.

---

##### **`get_blocking_entity_at_location`**

- **Purpose**: Returns the blocking entity at a specific location, if any.
- **Parameters**:
    - `location_x, location_y`: Coordinates to check.
- **Returns**: The blocking entity or `None`.

---

##### **`in_bounds`**

- **Purpose**: Checks if a coordinate is within the map bounds.
- **Parameters**:
    - `x, y`: Coordinates to check.
- **Returns**: `True` if within bounds; otherwise `False`.

---

##### **`render`**

- **Purpose**: Renders the map and visible entities on the console.
- **Parameters**:
    - `console`: The `tcod.Console` instance for rendering.
- **Key Features**:
    - Visible tiles are drawn with "light" colors.
    - Explored but non-visible tiles are drawn with "dark" colors.
    - Non-explored tiles use the `SHROUD` tile.
    - Entities are sorted by `render_order` to ensure correct layering.

---

##### **`get_actor_at_location`**

- **Purpose**: Retrieves the actor at a specific location, if any.
- **Parameters**:
    - `x, y`: Coordinates to check.
- **Returns**: The `Actor` instance or `None`.

---

##### **`get_locations_of_tile`**

- **Purpose**: Finds all map coordinates with a specific tile type.
- **Parameters**:
    - `tile_type`: The tile type to search for (e.g., `tile_types.floor_grass`).
- **Returns**: A list of `(x, y)` tuples for matching tile locations.

---

### **2. GameWorld Class**

The `GameWorld` class holds settings for the game world and is responsible for generating new levels.

#### **Attributes**

- **`engine`** (`Engine`): Reference to the game engine.
- **`map_width, map_height`** (`int`): Dimensions of generated maps.
- **`max_rooms`** (`int`): Maximum number of rooms per map.
- **`room_min_size, room_max_size`** (`int`): Size constraints for generated rooms.
- **`max_monsters_per_room`** (`int`): Maximum number of monsters per room.
- **`max_items_per_room`** (`int`): Maximum number of items per room.
- **`current_floor`** (`int`): Tracks the current dungeon floor level.

---

#### **Methods**

##### **`__init__`**

- **Purpose**: Initializes the `GameWorld` instance with game settings.
- **Parameters**:
    - `engine`: The game engine instance.
    - `map_width, map_height`: Dimensions of the generated maps.
    - `max_rooms`: Maximum number of rooms per level.
    - `room_min_size, room_max_size`: Constraints for room sizes.
    - `max_monsters_per_room, max_items_per_room`: Limits for entities in rooms.
    - `current_floor`: Initial dungeon floor (default: `0`).

---

##### **`generate_floor`**

- **Purpose**: Generates a new dungeon floor and increments the floor counter.
- **Key Operations**:
    - Imports the dungeon generation function from `procgen`.
    - Calls `generate_dungeon` with the current game settings.
    - Updates the `engine`'s `game_map` with the new map.

---

## **File Structure**

```
game_map.py           # Defines GameMap and GameWorld classes.
tile_types.py         # Tile definitions (walls, floors, etc.).
entity.py             # Entity base class, Actor, and Item classes.
procgen.py            # Procedural dungeon generation logic.
```

---

## **Usage Example**

### **Initialization**

1. Create an instance of `GameWorld`:
    
    ```python
    game_world = GameWorld(
        engine=engine,
        map_width=80,
        map_height=45,
        max_rooms=30,
        room_min_size=6,
        room_max_size=10,
        max_monsters_per_room=3,
        max_items_per_room=2,
    )
    ```
    
2. Generate the first floor:
    
    ```python
    game_world.generate_floor()
    ```
    

### **Rendering**

- Call the `render` method to draw the map and entities:
    
    ```python
    game_map.render(console)
    ```
    

### **Tile and Entity Queries**

- Get all locations of grass tiles:
    
    ```python
    grass_locations = game_map.get_locations_of_tile(tile_types.floor_grass)
    ```
    
- Check for a blocking entity:
    
    ```python
    blocker = game_map.get_blocking_entity_at_location(10, 5)
    if blocker:
        print(f"Blocking entity: {blocker.name}")
    ```
    

---

## **Future Improvements**

1. **Dynamic Tile Types**:
    - Allow dynamic changes to tile types during gameplay (e.g., traps, secret doors).
2. **Advanced Pathfinding**:
    - Integrate a more robust pathfinding system for both player and AI.
3. **Map Features**:
    - Add environmental effects (e.g., water, lava) to enhance gameplay mechanics.

This documentation provides a detailed breakdown of the `GameMap` and `GameWorld` classes and their integration into the game's core logic.