# **Documentation for `main.py`**

## **Overview**

This script is the entry point for the game "DIESEL 0.0". It initializes the game, handles the main event loop, manages input, and ensures the game state is saved in case of unexpected exits. The game uses the `tcod` library for rendering and input handling, along with custom modules for game-specific functionality.

---

## **Requirements**

### **Dependencies**

- **`tcod`**: Library for roguelike game development.
- **Custom Modules**:
    - **`color`**: Defines the color scheme used in the game.
    - **`exceptions`**: Handles game-specific exceptions.
    - **`input_handlers`**: Manages player input and events.
    - **`setup_game`**: Contains logic for initializing the game.

---

## **Key Components**

### **1. Game Saving**

#### `save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None`

- **Purpose**: Saves the game state to a file if the active event handler contains an `Engine` instance.
- **Parameters**:
    - `handler`: An event handler instance, which may include the game engine.
    - `filename`: The name of the file where the game state is saved.
- **Behavior**:
    - Checks if the `handler` is of type `EventHandler` (a subclass of `BaseEventHandler`).
    - Calls `save_as` on the handler's `Engine` instance.
    - Outputs "Game saved." to the console.
- **Example Usage**:
    - Automatically called during unexpected exits or when the player chooses to quit.

---

### **2. Main Game Loop**

#### `main() -> None`

- **Purpose**: Initializes the game and manages the primary event loop.
- **Key Steps**:
    1. **Screen Initialization**:
        - `screen_width` and `screen_height` define the terminal's size.
        - Loads a tileset (`dejavu10.png`) using `tcod.tileset.load_tilesheet`.
    2. **Game Initialization**:
        - The initial handler is set to `setup_game.MainMenu()`, which displays the main menu.
    3. **Game Context**:
        - Creates a `tcod.context` for managing the game window.
        - A `tcod.Console` instance is initialized to handle rendering.
    4. **Main Loop**:
        - Clears the console and renders the current game state via `handler.on_render`.
        - Processes user input using `tcod.event.wait` and updates the handler based on events.
    5. **Error Handling**:
        - **`QuitWithoutSaving`**: Allows the player to quit without saving.
        - **`SystemExit`**: Saves the game state and exits.
        - **Other Exceptions**: Saves the game state and re-raises the exception for debugging.

---

## **Error Handling**

### **Exceptions**

- **`exceptions.QuitWithoutSaving`**: Raised when the player quits the game without saving.
- **`SystemExit`**: Captures system-level exit calls to save the game before quitting.
- **`BaseException`**: Captures unexpected errors, saves the game state, and re-raises the exception.

---

## **Modules**

### **1. `color`**

- Used for consistent coloring in the game.
- Example: `color.error` specifies the color for error messages.

### **2. `exceptions`**

- Defines game-specific exceptions like `QuitWithoutSaving`.

### **3. `input_handlers`**

- Manages player input and events.
- Contains:
    - `BaseEventHandler`: A base class for handling events.
    - `EventHandler`: A subclass with an `engine` attribute for game logic.

### **4. `setup_game`**

- Contains the `MainMenu` class for initializing the game's main menu.

---

## **File Structure**

```
main.py                # Main script
color.py               # Defines color schemes
exceptions.py          # Custom exception definitions
input_handlers.py      # Handles player input
setup_game.py          # Game setup logic
tilesets/dejavu10.png  # Tileset image for rendering
```

---

## **Usage**

1. **Run the Game**:
    
    ```bash
    ./main.py
    ```
    
    Ensure that the `tilesets/dejavu10.png` file is in the correct directory.
    
2. **Save and Quit**:
    
    - The game saves automatically on `SystemExit` or unexpected errors.
3. **Debugging**:
    
    - Errors are printed to the console and logged in the game's message log (if active).

---

## **Code Walkthrough**

### **1. Script Header**

- `#!/usr/bin/env python3`: Indicates the script should be run with Python 3.
- Imports:
    - `traceback`: For error logging.
    - `tcod`: Provides tools for game rendering and input.
    - Custom modules (`color`, `exceptions`, `input_handlers`, `setup_game`).

### **2. Main Functionality**

- `save_game`: Saves the game state if an engine is active.
- `main`: Initializes the game, runs the main loop, and handles errors.

### **3. Entry Point**

- `if __name__ == "__main__":`: Ensures the `main` function runs when the script is executed directly.

---

## **Future Improvements**

1. **Refactor Error Handling**:
    - Add more specific exception types for better debugging.
2. **Dynamic Screen Dimensions**:
    - Allow customizable screen dimensions via a configuration file or arguments.
3. **Enhanced Saving**:
    - Notify the player of save file integrity and provide options for backups.

---

By organizing the documentation in this way, even new developers should have a clear understanding of the script's purpose and functionality.