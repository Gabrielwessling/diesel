# **Documentation for `engine.py`**

## **Overview**

The `engine.py` module is the core of the "DIESEL" game logic. It contains the `Engine` class, which manages the game's main systems, including:

1. **Player Management**: Handles the player's interactions and visibility.
2. **Game Map**: Manages the rendering and exploration of the map.
3. **Message Log**: Displays messages to the player.
4. **Save and Load**: Provides functionality for saving the game state.

---

## **Requirements**

### **Dependencies**

- **Third-Party Libraries**:
    - `tcod`: For rendering the console and calculating field of view (FOV).
- **Custom Modules**:
    - **`exceptions`**: Custom exceptions for handling specific in-game errors.
    - **`game_map`**: Defines the game world and tile-based map logic.
    - **`message_log`**: Manages the log of messages displayed to the player.
    - **`render_functions`**: Contains utilities for rendering game elements (e.g., health bars, names, and dungeon level).
- **Standard Libraries**:
    - `lzma`: For compressing save files.
    - `pickle`: For serializing and deserializing the game state.
    - `typing`: For type hints, specifically `TYPE_CHECKING` for avoiding circular imports.

---

## **Key Components**

### **1. Engine Class**

#### **Attributes**

- **`win_condition`** (`bool`): Tracks whether the win condition has been met (default: `False`).
- **`game_map`** (`GameMap`): Represents the current game map.
- **`game_world`** (`GameWorld`): Contains details about the game world, including floors and level transitions.
- **`heal_turn`** (`int`): Tracks the turn when healing occurs (default: `0`).
- **`message_log`** (`MessageLog`): Stores messages for player communication.
- **`mouse_location`** (`tuple[int, int]`): Tracks the mouse cursor's position on the map.
- **`player`** (`Actor`): Reference to the player character.

---

### **2. Methods**

#### **`__init__(self, player: Actor)`**

- **Purpose**: Initializes the `Engine` instance with a player character.
- **Parameters**:
    - `player`: The player character, an instance of `Actor`.
- **Key Operations**:
    - Initializes the `message_log` for storing player messages.
    - Sets the default mouse location to `(0, 0)`.

---

#### **`handle_enemy_turns(self) -> None`**

- **Purpose**: Processes turns for all enemies on the map.
- **Key Operations**:
    1. Iterates through all `Actor` entities on the map, excluding the player.
    2. If an enemy has AI, attempts to execute its behavior.
    3. Ignores `Impossible` exceptions, which indicate invalid actions.

---

#### **`update_fov(self) -> None`**

- **Purpose**: Updates the player's field of view (FOV) based on their position.
- **Key Operations**:
    1. Computes the visible area using the player's location and a visibility radius (`8` tiles).
    2. Updates the `game_map.visible` array to reflect the computed FOV.
    3. Marks tiles as "explored" if they become visible for the first time.

---

#### **`render(self, console: Console) -> None`**

- **Purpose**: Renders the game state to the console.
- **Parameters**:
    - `console`: The `tcod.Console` instance used for rendering.
- **Key Operations**:
    1. Renders the game map using `game_map.render`.
    2. Displays the `message_log` at a fixed position (`x=17, y=31`).
    3. Renders the player's health bar using `render_functions.render_bar`.
    4. Shows the names of entities under the mouse cursor with `render_functions.render_names_at_mouse_location`.
    5. Displays the current dungeon level with `render_functions.render_dungeon_level_indicator`.

---

#### **`save_as(self, filename: str) -> None`**

- **Purpose**: Saves the current game state to a compressed file.
- **Parameters**:
    - `filename`: The name of the save file (e.g., `savegame.sav`).
- **Key Operations**:
    1. Serializes the `Engine` instance using `pickle`.
    2. Compresses the serialized data with `lzma`.
    3. Writes the compressed data to the specified file in binary mode.

---

## **Modules**

### **1. `exceptions`**

- Handles custom exceptions specific to the game's logic.

### **2. `game_map`**

- Manages map tiles, visibility, and exploration.

### **3. `message_log`**

- Displays important messages to the player, such as combat results or status updates.

### **4. `render_functions`**

- Provides utility functions for rendering UI elements like health bars, entity names, and the dungeon level.

---

## **File Structure**

```
engine.py              # Core game logic and systems.
game_map.py            # Map and tile handling.
message_log.py         # Message logging system.
render_functions.py    # Rendering utilities.
exceptions.py          # Custom exception handling.
```

---

## **Usage**

1. **Initialization**:
    
    - An instance of `Engine` is created by passing a player character (`Actor`).
    - Example:
        
        ```python
        engine = Engine(player=player_character)
        ```
        
2. **Game Loop**:
    
    - Call `update_fov` whenever the player moves to update visibility.
    - Render the game state using `render`:
        
        ```python
        engine.update_fov()
        engine.render(console)
        ```
        
3. **Saving**:
    
    - Save the game state to a file:
        
        ```python
        engine.save_as("savegame.sav")
        ```
        
4. **Enemy Turns**:
    
    - Call `handle_enemy_turns` to process enemy behavior:
        
        ```python
        engine.handle_enemy_turns()
        ```
        

---

## **Future Improvements**

1. **Dynamic FOV Radius**:
    - Allow the FOV radius to change based on player attributes or items.
2. **Modular AI**:
    - Expand enemy AI to support more complex behaviors and interactions.
3. **Custom Save Locations**:
    - Add support for specifying save file directories and names dynamically.

---

This documentation provides a comprehensive understanding of the `Engine` class and its role in the game.