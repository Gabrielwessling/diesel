from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class SpawnCurve(BaseComponent):
    parent: Actor

    def __init__(self, min_prob: float = 0.0, peak_prob: float = 1.0, start_floor: int = 1, 
                 peak_floor: int = 5, end_floor: int = 10):
        self.min_prob = min_prob
        self.peak_prob = peak_prob
        self.start_floor = start_floor
        self.peak_floor = peak_floor
        self.end_floor = end_floor

    def __repr__(self) -> str:
        return f"EnemyStats(min_prob={self.min_prob}, peak_prob={self.peak_prob}, " \
               f"start_floor={self.start_floor}, peak_floor={self.peak_floor}, end_floor={self.end_floor})"
