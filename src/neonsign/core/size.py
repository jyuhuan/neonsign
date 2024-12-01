from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class Size:
    width: int
    height: int

    def __post_init__(self):
        if self.width < 0:
            raise ValueError(
                f'The width of a size must be non-negative, '
                f'and not {self.width}!'
            )
        if self.height < 0:
            raise ValueError(
                f'The height of a size must be non-negative, '
                f'and not {self.height}!'
            )

    @property
    def area(self) -> int:
        return self.width * self.height

    def can_fit_within(self, other: Size) -> bool:
        return self.width <= other.width and self.height <= other.height

    def with_updated_width(self, new_width: int) -> Size:
        return Size(width=new_width, height=self.height)

    def with_updated_height(self, new_height: int) -> Size:
        return Size(width=self.width, height=new_height)

    def increased_by(self, width_delta: int = 0, height_delta: int = 0) -> Size:
        return Size(width=self.width + width_delta, height=self.height + height_delta)

    def __gt__(self, other: Size) -> bool:
        return self.width > other.width and self.height > other.height

    def __ge__(self, other: Size) -> bool:
        return self.width >= other.width and self.height >= other.height

    def __lt__(self, other: Size) -> bool:
        return self.width < other.width and self.height < other.height

    def __le__(self, other: Size) -> bool:
        return self.width <= other.width and self.height <= other.height

    def __str__(self) -> str:
        return f'{self.width}x{self.height}'

    @classmethod
    def zero(cls) -> Size:
        return Size(width=0, height=0)

    @classmethod
    def max(cls) -> Size:
        return Size(width=sys.maxsize, height=sys.maxsize)

    @classmethod
    def square(cls, length: int) -> Size:
        return Size(width=length, height=length)
