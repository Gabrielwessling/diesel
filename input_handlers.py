from __future__ import annotations
import os

from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union

import tcod.event
import math

import actions
from actions import (
    Action,
    BumpAction,
    PickupAction,
    WaitAction
)
import categories.color as color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

KEY_BINDINGS = {
    "inventory": tcod.event.KeySym.i,
    "drop_item": tcod.event.KeySym.o,
    "look_around": tcod.event.KeySym.x,
    "skills": tcod.event.KeySym.TAB,
    "pickup": tcod.event.KeySym.g,
    "history": tcod.event.KeySym.h,
    "quit": tcod.event.KeySym.ESCAPE,
}

MOVE_KEYS = {
    # WASDQEZC keys
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.d: (1, 0),
    tcod.event.KeySym.q: (-1, -1),
    tcod.event.KeySym.e: (1, -1),
    tcod.event.KeySym.z: (-1, 1),
    tcod.event.KeySym.c: (1, 1),

    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
    tcod.event.KeySym.SPACE
}

CONFIRM_KEYS = {
    tcod.event.KeySym.RETURN,
    tcod.event.KeySym.KP_ENTER,
}

EXIT_KEYS = {
    tcod.event.KeySym.ESCAPE,
    tcod.event.KeySym.BACKSPACE,
    tcod.event.MouseButton.RIGHT,
}

ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[ActionOrHandler]:
        raise SystemExit()

class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action: Optional[ActionOrHandler]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if not hasattr(self.engine, "game_map"):
            return
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y
    
    def on_render(self, console: tcod.console.Console) -> None:
        self.engine.render(console)

class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.Console) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg=color.white,
            bg=color.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent

class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        if event.sym in {  # Ignore modifier keys.
            tcod.event.KeySym.LSHIFT,
            tcod.event.KeySym.RSHIFT,
            tcod.event.KeySym.LCTRL,
            tcod.event.KeySym.RCTRL,
            tcod.event.KeySym.LALT,
            tcod.event.KeySym.RALT,
        }:
            return None
        return self.on_exit()

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameEventHandler(self.engine)

class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item with the mouse or keyboard."""

    TITLE = "<missing title>"

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.grouped_items = self.group_inventory_items()
        self.current_index = 0  # Index of the currently highlighted item

    def group_inventory_items(self) -> list[tuple[str, Item, int]]:
        """Group inventory items by name, preserving their order and count."""
        grouped = {}
        for item in self.engine.player.inventory.items:
            key = f"[E] {item.name}" if self.engine.player.equipment.item_is_equipped(item) else item.name
            if key in grouped:
                grouped[key]["count"] += 1
            else:
                grouped[key] = {"item": item, "count": 1}
        return [(name, data["item"], data["count"]) for name, data in grouped.items()]

    def on_render(self, console: tcod.Console) -> None:
        """Render the inventory menu."""
        super().on_render(console)

        height = len(self.grouped_items) + 3
        height = max(height, 3)
        inventory = self.engine.player.inventory
        total_weight = sum(item.weight for item in inventory.items)
        max_weight = inventory.max_weight

        x = 40 if self.engine.player.x <= 30 else 0
        y = 0
        width = max(len(self.TITLE), 30) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(
            x + 1,
            y + 1,
            f"Load: {total_weight}/{max_weight}kg and {len(inventory.items)}/{inventory.capacity}",
        )

        if self.grouped_items:
            for i, (item_name, _, count) in enumerate(self.grouped_items):
                highlight = (i == self.current_index)
                fg = (255, 255, 0) if highlight else (255, 255, 255)
                console.print(x + 1, y + i + 2, f"{item_name} x{count}", fg=fg)
        else:
            console.print(x + 1, y + 2, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Handle keyboard input for navigation and selection."""
        key = event.sym

        if key in {tcod.event.K_UP, tcod.event.K_w}:
            self.current_index = (self.current_index - 1) % len(self.grouped_items)
        elif key in {tcod.event.K_DOWN, tcod.event.K_s}:
            self.current_index = (self.current_index + 1) % len(self.grouped_items)
        elif key in {tcod.event.K_RETURN, tcod.event.K_KP_ENTER}:
            _, selected_item, _ = self.grouped_items[self.current_index]
            return self.on_item_selected(selected_item)
        elif key in EXIT_KEYS:
            return MainGameEventHandler(self.engine)
        return None

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        """Highlight items as the mouse hovers over them."""
        x, y = event.tile
        if x >= 1 and y >= 2 and y < len(self.grouped_items) + 2:
            self.current_index = y - 2

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """Select an item with a left mouse click."""
        if event.button == 1:  # Left mouse button
            if 0 <= self.current_index < len(self.grouped_items):
                _, selected_item, _ = self.grouped_items[self.current_index]
                return self.on_item_selected(selected_item)
        if event.button == 2:  # Left mouse button
            if 0 <= self.current_index < len(self.grouped_items):
                _, selected_item, _ = self.grouped_items[self.current_index]
                return actions.DropItem(self.engine.player, selected_item)
        return None

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Override this in subclasses for specific behavior."""
        raise NotImplementedError()

class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an Item to use"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Return the action for the selected item."""
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Drop Item"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        return actions.DropItem(self.engine.player, item)

class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y
        self.offset_x = 0
        self.offset_y = 0

    def on_render(self, console: tcod.console.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        
        # Destaca o tile sob o cursor
        x, y = self.engine.mouse_location
                
        console.rgb["bg"][x, y] = color.white
        console.rgb["fg"][x, y] = color.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        return MainGameEventHandler(self.engine)

class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(
        self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[ActionOrHandler]]
    ):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        return self.callback((x, y))

class SquareAreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[ActionOrHandler]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        return self.callback((x, y))

class CircleAreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[ActionOrHandler]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a circle around the targeted area, so the player can see the affected tiles.
        for dx in range(-self.radius, self.radius + 1):
            for dy in range(-self.radius, self.radius + 1):
                # Check if the current tile (dx, dy) lies within the circle
                if math.sqrt(dx ** 2 + dy ** 2) <= self.radius:
                    # Print a character at the position (x + dx, y + dy)
                    console.print(x + dx, y + dy, 'X', fg=color.red)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        return self.callback((x, y))

class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        action: Optional[ActionOrHandler] = None

        key = event.sym
        modifier = event.mod

        player = self.engine.player


        if key == tcod.event.KeySym.PERIOD and modifier & (
            tcod.event.KeySym.LSHIFT | tcod.event.KeySym.RSHIFT
        ):
            return actions.TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key == KEY_BINDINGS["skills"]:
            return SkillsViewer(self.engine)
        elif key in WAIT_KEYS:
            action = WaitAction(player)
        elif key == KEY_BINDINGS["history"]:
            return HistoryViewer(self.engine)
        elif key == KEY_BINDINGS["pickup"]:
            action = PickupAction(player)
        elif key == KEY_BINDINGS["inventory"]:
            return InventoryActivateHandler(self.engine)
        elif key == KEY_BINDINGS["drop_item"]:
            return InventoryDropHandler(self.engine)
        elif key == KEY_BINDINGS["look_around"]:
            return LookHandler(self.engine)
        elif key == KEY_BINDINGS["quit"]:
            raise SystemExit

        # No valid key was pressed
        return action
    
class GameOverEventHandler(EventHandler):
    def on_quit(self) -> None:
        """Handle exiting out of a finished game."""
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")  # Deletes the active save file.
        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.KeySym.ESCAPE:
            self.on_quit()

CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
    tcod.event.KeySym.PAGEUP: -10,
    tcod.event.KeySym.PAGEDOWN: 10,
}

class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.console.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤History Browser├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            return MainGameEventHandler(self.engine)
        return None
    
class SkillsViewer(EventHandler):
    """Exibe as habilidades do jogador, nível atual, XP e XP restante.""" 
    
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.player = engine.player

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Desenha o estado principal como fundo.

        # Desenhando o console de habilidades
        skills_console = tcod.Console(console.width - 6, console.height - 6)
        skills_console.draw_frame(0, 0, skills_console.width, skills_console.height)
        skills_console.print_box(
            0, 0, skills_console.width, 1, "┤ Status ├", alignment=tcod.CENTER
        )

        # Validando se `skill_list` existe
        if not hasattr(self.player, "skill_list") or self.player.skill_list is None:
            skills_console.print(1, 5, "No skill found.")
            skills_console.blit(console, 3, 3)
            return

        # Listando habilidades do jogador
        y_offset = 2
        for i, skill in enumerate(self.player.skill_list.skills):  # Itera pelas habilidades
            skill_line = (
                f"{self.player.skill_list.skills[skill].name}: Level {self.player.skill_list.skills[skill].current_level} - {self.player.skill_list.skills[skill].remaining_xp} xp to next level"
            )
            skills_console.print(1, y_offset + i * 2, skill_line)

        skills_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Pressionar qualquer tecla retorna ao estado do jogo principal."""
        return MainGameEventHandler(self.engine)