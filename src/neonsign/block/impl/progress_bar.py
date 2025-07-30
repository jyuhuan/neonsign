from typing import Optional

from neonsign.block.block import LeafBlock
from neonsign.block.canvas import Canvas, PixelSource
from neonsign.core.size import Size


BLOCK_CHARS = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']


class ProgressBar(LeafBlock):

    DEFAULT_WIDTH: int = 10

    def __init__(self, progress: float):
        if progress < 0.0:
            raise ValueError(
                f'progress cannot be negative, but {progress} was provided!'
            )
        if progress > 1.0:
            raise ValueError(
                f'progress cannot be greater than 1, but {progress} was provided!'
            )
        self.progress = progress

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
        num_units_in_full_block = len(BLOCK_CHARS)
        num_units_available = granted_size.width * num_units_in_full_block
        num_units_to_fill = int(self.progress * num_units_available)
        num_full_blocks = num_units_to_fill // num_units_in_full_block
        partial_block_index = (num_units_to_fill % num_units_in_full_block) - 1

        def factory(x: int, _: int) -> PixelSource:
            if x < num_full_blocks:
                return BLOCK_CHARS[-1]
            elif x == num_full_blocks and partial_block_index >= 0:
                return BLOCK_CHARS[partial_block_index]
            else:
                return ' '
        return Canvas.of(size=granted_size, pixel_factory=factory)
