# **Documentation for `setup_game.py`**

## **Overview**

This script handles the initialization and management of game sessions in "DIESEL." It provides tools for creating new games, loading saved games, and rendering the main menu. The script includes three main components:

1. **Game Initialization**: Creates new game sessions.
2. **Game Loading**: Loads saved game states.
3. **Main Menu**: Handles the game's main menu rendering and input.

---

## **Requirements**

### **Dependencies**

- **`tcod`**: Library for roguelike game development.
- **Custom Modules**:
    - **`color`**: Manages game color schemes.
    - **`engine`**: Core game logic, including the `Engine` class.
    - **`entity_factories`**: Provides pre-defined game entities like the player character.
    - **`game_map`**: Handles the game world, including map generation.
    - **`input_handlers`**: Manages player input and event handling.
- **Standard Libraries**:
    - `copy`: For deep copying objects.
    - `lzma`: For file compression and decompression.
    - `pickle`: For serializing and deserializing Python objects.
    - `traceback`: For debugging errors.

---

## **Key Components**

### **1. Game Initialization**

#### `new_game() -> Engine`

- **Purpose**: Initializes a new game session and returns an `Engine` instance.
- **Key Steps**:
    1. **Define Map Parameters**:
        - `map_width` and `map_height` set the dimensions of the game map.
        - Room generation parameters:
            - `room_max_size`, `room_min_size`: Control the size of individual rooms.
            - `max_rooms`: Sets the maximum number of rooms in the game.
        - `max_monsters_per_room`, `max_items_per_room`: Determine the density of monsters and items.
    2. **Create Player**:
        - A deep copy of the player entity is created using `entity_factories.player`.
    3. **Initialize Engine**:
        - Creates an `Engine` instance with the player entity.
        - Configures the game world using `GameWorld`.
        - Generates the game map and updates the field of view (FOV).
    4. **Message Log**:
        - Adds a welcome message to the message log.
- **Returns**: An initialized `Engine` instance ready to run the game.
- **Example Usage**:
    - Called when the player starts a new game from the main menu.

---

### **2. Game Loading**

#### `load_game(filename: str) -> Engine`

- **Purpose**: Loads a previously saved game session.
- **Key Steps**:
    1. Opens the specified file (`filename`) in binary read mode.
    2. Reads and decompresses the file's contents using `lzma`.
    3. Deserializes the data into an `Engine` instance using `pickle`.
    4. Validates that the deserialized object is an instance of `Engine`.
- **Parameters**:
    - `filename`: The name of the save file (e.g., `savegame.sav`).
- **Returns**: An `Engine` instance representing the saved game state.
- **Example Usage**:
    - Called when the player chooses to continue from a save file in the main menu.

---

### **3. Main Menu**

#### `class MainMenu(input_handlers.BaseEventHandler)`

- **Purpose**: Manages the main menu's rendering and input handling.
- **Methods**:
    - **`on_render(console: tcod.Console) -> None`**:
        - Renders the main menu with a background image.
        - Displays the game title and menu options:
            - `[N] Novo Jogo`: Start a new game.
            - `[C] Continuar`: Continue from the last save.
            - `[Q] Quitar`: Quit the game.
        - Uses `tcod`'s semigraphics for displaying the background.
    - **`ev_keydown(event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]`**:
        - Handles key press events in the main menu:
            - **Quit (`Q` or `ESC`)**: Exits the game.
            - **Continue (`C`)**: Loads the last saved game if available.
            - **New Game (`N`)**: Starts a new game session.
        - Handles errors gracefully, providing feedback for failed game loads.

---

## **Modules**

### **1. `color`**

- **Purpose**: Defines colors for the game's user interface.
- **Key Variables**:
    - `color.menu_title`: Color for the main menu title.
    - `color.menu_text`: Color for the menu options.
    - `color.welcome_text`: Welcome message color.

### **2. `engine`**

- **Purpose**: Implements the core game logic.
- **Key Class**:
    - `Engine`: Manages the player, game world, and overall game state.

### **3. `entity_factories`**

- **Purpose**: Provides templates for game entities.
- **Key Entity**:
    - `player`: The player's character.

### **4. `game_map`**

- **Purpose**: Handles map generation and game world logic.
- **Key Class**:
    - `GameWorld`: Represents the procedurally generated game world.

### **5. `input_handlers`**

- **Purpose**: Manages input and event handling for different game states.
- **Key Classes**:
    - `BaseEventHandler`: Base class for handling events.
    - `MainGameEventHandler`: Handles in-game events.
    - `PopupMessage`: Displays messages to the player.

---

## **File Structure**

```
setup_game.py           # Handles game initialization and main menu.
engine.py               # Core game logic and engine implementation.
entity_factories.py     # Game entity templates.
game_map.py             # Map and world generation logic.
color.py                # Color scheme definitions.
images/menu_background.png  # Background image for the main menu.
```

---

## **Usage**

1. **Main Menu Navigation**:
    
    - **`N`**: Starts a new game.
    - **`C`**: Continues from the last save.
    - **`Q`** or **`ESC`**: Exits the game.
2. **Save File Management**:
    
    - Save files are stored as compressed `.sav` files.
    - Ensure `savegame.sav` exists in the root directory to continue a game.
3. **Debugging**:
    
    - Errors during save file loading are logged to `stderr`.

---

## **Code Walkthrough**

### **1. Background Image**

- Loaded using `tcod.image.load` and stripped of its alpha channel for compatibility with the console.

### **2. Game Initialization**

- `new_game` creates a complete `Engine` instance with procedural map generation.

### **3. Save File Loading**

- `load_game` validates the integrity of the save file before returning an `Engine` instance.

### **4. Main Menu**

- Renders an interactive menu with options to start a new game, continue, or quit.

---

## **Future Improvements**

1. **Dynamic Menu Options**:
    - Add settings or customizable keybindings to the main menu.
2. **Save Management**:
    - Allow multiple save slots for more flexibility.
3. **Enhanced Error Handling**:
    - Provide detailed error messages and potential fixes for failed game loads.

---

This documentation ensures clarity for newcomers and provides a strong foundation for further development.