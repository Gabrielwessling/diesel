"""Handle the loading and initialization of game sessions."""
from __future__ import annotations
from tcod import libtcodpy

from typing import Optional

import copy
import tcod
import lzma
import pickle
import traceback

import categories.color as color
from engine import Engine
from entity_factories import EntityFactories
from game_map import GameWorld
import input_handlers

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("images/menu_background.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 40

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 1
    max_items_per_room = 3

    engine = Engine(player=None, entity_factories=EntityFactories(None, None))
    entity_factories = EntityFactories(engine=engine, gamemap=None)
    engine.entity_factories = entity_factories
    player = copy.deepcopy(entity_factories.player)
    engine.player = player

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
    )
    engine.game_world.generate_floor()
    engine.entity_factories.gamemap = engine.game_map
    engine.game_map.engine = engine
    engine.update_fov()

    engine.message_log.add_message(
        "Welcome to hell, where some claw their way for diesel and others bleed for credits. Will you thrive or will you be used as fuel for the engines of violence?", color.welcome_text
    )
    return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

def draw_fullscreen_image(console: tcod.console.Console, image: tcod.image.Image):
    """Desenha uma imagem ajustada ao tamanho do console."""
    image_width, image_height = image.width, image.height
    console_width, console_height = console.width, console.height

    # Calcula o fator de escala para preencher a tela
    scale_x = console_width / image_width
    scale_y = console_height / image_height

    # Aplica a escala mínima para preservar o aspecto
    scale = min(scale_x, scale_y)

    # Calcula as novas dimensões da imagem com base no fator de escala
    new_width = int(image_width * scale)
    new_height = int(image_height * scale)

    # Redimensiona a imagem
    image.scale(new_width, new_height)
    
    # Desenha a imagem redimensionada no console
    image.blit(console, 0, 0, bg_blend=1, scale_x=2.03, scale_y=2.06, angle=0)

class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        image = tcod.image.Image(75, 35).from_file("images\menu_background.png")
        draw_fullscreen_image(console, image)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "DIESEL",
            fg=color.menu_title,
            bg=color.black,
            alignment=libtcodpy.CENTER,
            bg_blend=libtcodpy.BKGND_ALPHA(64),
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "by Gabriel Wessling",
            fg=color.menu_title,
            bg=color.black,
            alignment=libtcodpy.CENTER,
            bg_blend=libtcodpy.BKGND_ALPHA(64),
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] New Game","[C] Continue" , "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return input_handlers.MainGameEventHandler(new_game())

        return None