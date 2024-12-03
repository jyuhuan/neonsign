from dataclasses import dataclass
from typing import final

from neonsign.block.canvas import Canvas
from neonsign.block.measurable import FlexibleMeasurable
from neonsign.block.block import LeafBlock
from neonsign.core.size import Size


@final
@dataclass
class Rectangle(LeafBlock, FlexibleMeasurable):
    def _render(self, granted_size: Size) -> Canvas:
        return Canvas.of(size=granted_size, pixel_factory=lambda x, y: ' ')
