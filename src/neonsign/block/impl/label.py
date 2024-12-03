import math
from dataclasses import dataclass
from typing import Optional, final

from neonsign.block.block import LeafBlock
from neonsign.block.canvas import Canvas, PixelSource
from neonsign.core.size import Size


@final
@dataclass
class Label(LeafBlock):
    content: str

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        if len(self.content) == 0:
            return Size.zero()

        if width_constraint is not None and width_constraint == 0:
            return Size.zero()
        if height_constraint is not None and height_constraint == 0:
            return Size.zero()

        # Is wrapping necessary?
        if width_constraint is None or width_constraint > len(self.content):
            return Size(
                width=len(self.content),
                height=1
            )
        else:
            # TODO: Implement better handling of space characters. For example,
            #  avoid starting a new line with a space.
            num_lines = int(math.ceil(len(self.content) / width_constraint))
            if height_constraint is not None:
                num_lines = min(num_lines, height_constraint)
            return Size(width=width_constraint, height=num_lines)

    def _render(self, granted_size: Size) -> Canvas:
        if granted_size.area >= len(self.content):
            content = self.content
        else:
            content = self.content[:granted_size.area - 1] + '…'

        def pixel_factory(x: int, y: int) -> PixelSource:
            i = x + y * granted_size.width
            return content[i] if i < len(content) else ' '
        return Canvas.of(granted_size, pixel_factory)
