#!/usr/bin/env python3
import traceback

import tcod

import categories.color as color
import exceptions
import input_handlers
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main() -> None:
    screen_width = 90
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet("tilesets/urizen12.png", 30, 40, tcod.tileset.CHARMAP)
    
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
    
    with tcod.context.new(
        width=90,
        height=50,
        columns=90,
        rows=50,
        sdl_window_flags=tcod.context.SDL_WINDOW_FULLSCREEN_DESKTOP,
        renderer=tcod.context.RENDERER_OPENGL2,
        tileset=tileset,
        title="DIESEL 0.0",
        vsync=True,
    ) as context:
        root_console: tcod.console
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise
    
if __name__ == "__main__":
    main()