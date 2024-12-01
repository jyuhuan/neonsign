from __future__ import annotations

from dataclasses import dataclass

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

    @classmethod
    def zero(cls) -> Rect:
        return Rect(top_left=Point.origin(), size=Size.zero())
