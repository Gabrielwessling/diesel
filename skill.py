

from typing import Optional

from engine import Engine
from entity import Actor


class Skill:
    def __init__(
        self,
        name: str = "noname",
        current_level: int = 1,
        current_xp: int = 0,
        level_up_base: int = 0,
        level_up_factor: int = 150,
        xp_given: int = 0,
        parent: Optional[Actor] = None,  # Assuming parent references an Actor that has a 'fighter' component
        engine: Optional[Engine] = None  # Assuming 'engine' is the game engine that handles messaging
    ):
        self.name = name
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given
        self.parent = parent  # Parent actor to access 'fighter' component
        self.engine = engine  # Engine for messaging system

    @property
    def experience_to_next_level(self) -> int:
        """Calculate XP required to reach the next level."""
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def requires_level_up(self) -> bool:
        """Check if current XP exceeds the required XP for the next level."""
        return self.current_xp >= self.experience_to_next_level

    def add_xp(self, xp: int) -> None:
        """Add experience points and level up if necessary."""
        if xp == 0 or self.level_up_base == 0:
            return

        self.current_xp += xp

        if self.requires_level_up:
            self.increase_level()

    def increase_level(self) -> None:
        """Increase the skill level and adjust XP."""
        # Handle level-up by subtracting the XP needed for the current level
        while self.requires_level_up:  # Make sure multiple level-ups can happen at once
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1
            self.engine.message_log.add_message(f"Your {self.name} skill has leveled up!")

    def increase_power(self, amount: int = 1) -> None:
        """Increase the character's power and base power."""
        if self.parent and hasattr(self.parent, "fighter"):
            self.parent.fighter.base_power += amount
            self.engine.message_log.add_message("You feel stronger!")
        else:
            raise ValueError("Parent does not have a 'fighter' attribute")

    def increase_defense(self, amount: int = 1) -> None:
        """Increase the character's defense and base defense."""
        if self.parent and hasattr(self.parent, "fighter"):
            self.parent.fighter.base_defense += amount
            self.engine.message_log.add_message("Your movements are getting swifter!")
        else:
            raise ValueError("Parent does not have a 'fighter' attribute")
