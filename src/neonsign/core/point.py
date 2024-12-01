from __future__ import annotations

from dataclasses import dataclass
from typing import final


@final
@dataclass
class Point:
    x: int
    y: int

    def moved_by(self, x_delta: int = 0, y_delta: int = 0) -> Point:
        if x_delta == 0 and y_delta == 0:
            return self
        return Point(x=self.x + x_delta, y=self.y + y_delta)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    @classmethod
    def origin(cls) -> Point:
        return Point(x=0, y=0)
