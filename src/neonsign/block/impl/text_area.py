import math
from typing import Optional

from neonsign.block.block import LeafBlock
from neonsign.block.canvas import Canvas, PixelSource
from neonsign.core.size import Size


class TextArea(LeafBlock):

    DEFAULT_WIDTH = 4

    def __init__(
            self,
            content: str,
            max_number_of_lines: Optional[int] = None,
    ):
        self.content = content

        if max_number_of_lines is not None and max_number_of_lines <= 0:
            raise ValueError(
                f'max_number_of_lines must be a positive integer '
                f'and not {max_number_of_lines}!'
            )
        self.max_number_of_lines = max_number_of_lines

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:

        if self.max_number_of_lines is not None:
            if height_constraint is not None:
                height_constraint = min(height_constraint, self.max_number_of_lines)
            else:
                height_constraint = self.max_number_of_lines

        if width_constraint is None and height_constraint is None:
            if len(self.content) == 0:
                return Size(width=self.DEFAULT_WIDTH, height=1)
            return Size(width=len(self.content), height=1)

        elif width_constraint is not None and height_constraint is None:
            if width_constraint == 0:
                return Size.zero()
            if len(self.content) == 0:
                return Size(width=width_constraint, height=1)
            num_lines = int(math.ceil(len(self.content) / width_constraint))
            return Size(width=width_constraint, height=num_lines)

        elif width_constraint is None and height_constraint is not None:
            if height_constraint == 0:
                return Size.zero()
            if len(self.content) == 0:
                return Size(width=self.DEFAULT_WIDTH, height=1)
            if height_constraint == 0:
                return Size.zero()
            return Size(width=len(self.content), height=1)

        else:
            if width_constraint == 0 or height_constraint == 0:
                return Size.zero()
            if len(self.content) == 0:
                return Size(width=width_constraint, height=1)
            else:
                num_lines = int(math.ceil(len(self.content) / width_constraint))
                return Size(
                    width=width_constraint,
                    height=min(num_lines, height_constraint)
                )

    def _render(self, granted_size: Size) -> Canvas:
        if granted_size.area >= len(self.content):
            content = self.content
        else:
            content = self.content[:granted_size.area - 1] + '…'

        def pixel_factory(x: int, y: int) -> PixelSource:
            i = x + y * granted_size.width
            return content[i] if i < len(content) else ' '
        return Canvas.of(granted_size, pixel_factory)
