

from typing import Optional

from engine import Engine
from entity import Actor

import categories.color as color


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
    def remaining_xp(self) -> int:
        return (self.level_up_base + self.current_level * self.level_up_factor) - self.current_xp
    
    @property
    def requires_level_up(self) -> bool:
        """Check if current XP exceeds the required XP for the next level."""
        return self.current_xp >= self.experience_to_next_level

    def add_xp(self, amount: int) -> None:
        self.current_xp += amount
        if self.current_xp >= self.experience_to_next_level:
            self.level_up()

    def level_up(self) -> None:
        self.current_level += 1
        self.current_xp -= self.experience_to_next_level
        self.engine.message_log.add_message(
            f"{self.name} subiu para o nível {self.current_level}!", color.white
        )

    def increase_level(self) -> None:
        """Increase the skill level and adjust XP."""
        # Handle level-up by subtracting the XP needed for the current level
        while self.requires_level_up:  # Make sure multiple level-ups can happen at once
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1
            self.engine.message_log.add_message(f"Your {self.name} skill has leveled up!")
