from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from neonsign.core.point import Point
from neonsign.core.size import Size


@dataclass
class Rect:

    top_left: Point
    size: Size

    @property
    def top_right(self) -> Point:
        return Point(x=self.top_left.x + self.size.width, y=self.top_left.y)

    @property
    def bottom_left(self) -> Point:
        return Point(x=self.top_left.x, y=self.top_left.y + self.size.height)

    @property
    def bottom_right(self) -> Point:
        return Point(
            x=self.top_left.x + self.size.width,
            y=self.top_left.y + self.size.height
        )

    @property
    def left(self) -> int:
        return self.top_left.x

    @property
    def right(self) -> int:
        return self.top_right.x

    @property
    def top(self) -> int:
        return self.top_left.y

    @property
    def bottom(self) -> int:
        return self.bottom_left.y

    def moved_by(self, x_delta: int = 0, y_delta: int = 0) -> Rect:
        if x_delta == 0 and y_delta == 0:
            return self
        return Rect(
            size=self.size,
            top_left=self.top_left.moved_by(
                x_delta=x_delta,
                y_delta=y_delta
            )
        )

    def moved_to_origin(self) -> Rect:
        return Rect.from_origin(self.size)

    def intersect(self, other: Rect) -> Optional[Rect]:
        x1 = max(self.top_left.x, other.top_left.x)
        y1 = max(self.top_left.y, other.top_left.y)
        x2 = min(
            self.top_left.x + self.size.width,
            other.top_left.x + other.size.width
        )
        y2 = min(
            self.top_left.y + self.size.height,
            other.top_left.y + other.size.height
        )

        if x2 <= x1 or y2 <= y1:
            return None

        # Convert to self's coordinate system
        rel_x1 = x1 - self.top_left.x
        rel_y1 = y1 - self.top_left.y

        return Rect(
            top_left=Point(rel_x1, rel_y1),
            size=Size(width=x2 - x1, height=y2 - y1)
        )

    @classmethod
    def zero(cls) -> Rect:
        return Rect(top_left=Point.origin(), size=Size.zero())

    @classmethod
    def from_origin(cls, size: Size) -> Rect:
        return Rect(top_left=Point.origin(), size=size)
