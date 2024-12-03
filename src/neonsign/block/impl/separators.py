from dataclasses import dataclass
from typing import Optional, final

from neonsign.block.canvas import Canvas
from neonsign.block.block import LeafBlock
from neonsign.core.size import Size


@final
@dataclass
class HorizontalSeparator(LeafBlock):
    """A horizontal line that separates contents in a :class:`Column`."""

    DEFAULT_WIDTH = 3

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        if width_constraint is None and height_constraint is None:
            return Size(width=self.DEFAULT_WIDTH, height=1)
        elif width_constraint is not None and height_constraint is None:
            if width_constraint == 0:
                return Size.zero()
            return Size(width=width_constraint, height=1)
        elif width_constraint is None and height_constraint is not None:
            if height_constraint == 0:
                return Size.zero()
            return Size(width=self.DEFAULT_WIDTH, height=1)
        else:
            if width_constraint == 0 or height_constraint == 0:
                return Size.zero()
            return Size(width=width_constraint, height=1)

    def _render(self, granted_size: Size) -> Canvas:
        return Canvas.of(granted_size, lambda x, y: '─')


@final
@dataclass
class VerticalSeparator(LeafBlock):
    """A vertical line that separates contents in a :class:`Row`."""

    DEFAULT_HEIGHT = 3

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        if width_constraint is None and height_constraint is None:
            return Size(width=1, height=self.DEFAULT_HEIGHT)
        elif width_constraint is not None and height_constraint is None:
            if width_constraint == 0:
                return Size.zero()
            return Size(width=1, height=self.DEFAULT_HEIGHT)
        elif width_constraint is None and height_constraint is not None:
            if height_constraint == 0:
                return Size.zero()
            return Size(width=1, height=height_constraint)
        else:
            if width_constraint == 0 or height_constraint == 0:
                return Size.zero()
            return Size(width=1, height=height_constraint)

    def _render(self, granted_size: Size) -> Canvas:
        return Canvas.of(granted_size, lambda x, y: '│')
