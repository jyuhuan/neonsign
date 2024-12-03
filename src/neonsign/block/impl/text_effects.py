from __future__ import annotations

from typing import Callable, Optional, Tuple, final

from neonsign.block.canvas import (
    Canvas, Pixel, PixelSource,
    StyledStringPixel
)
from neonsign.block.block import Block, LayoutBlock
from neonsign.core.colors import Color
from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size
from neonsign.string.styled_string import StyledString


class MappedBlock(LayoutBlock):

    def __init__(
            self,
            original: Block,
            f: Callable[[StyledString], StyledString]
    ):
        self.original = original
        self.f = f

    @property
    def subblocks(self) -> Tuple[Block, ...]:
        return (self.original,)

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        return self.original.measure(
            width_constraint=width_constraint,
            height_constraint=height_constraint
        )

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        return (
            Rect(
                top_left=Point.origin(),
                size=self.measure(
                    width_constraint=granted_size.width,
                    height_constraint=granted_size.height
                )
            ),
        )

    def _render(self, granted_size: Size) -> Canvas:
        original_render: Canvas = self.original.render(granted_size)
        def f(pixel: Pixel) -> PixelSource:
            if isinstance(pixel, StyledStringPixel):
                return self.f(pixel.styled_string)
            else:
                return pixel
        return original_render.map(f)


@final
class ForegroundColoredBlock(MappedBlock):
    def __init__(self, original: Block, color: Color):
        super().__init__(original, lambda _: _.foreground(color))


@final
class BackgroundColoredBlock(MappedBlock):
    def __init__(self, original: Block, color: Color):
        super().__init__(original, lambda _: _.background(color))


@final
class BoldBlock(MappedBlock):
    def __init__(self, original: Block):
        super().__init__(original, lambda _: _.bold())


@final
class ItalicBlock(MappedBlock):
    def __init__(self, original: Block):
        super().__init__(original, lambda _: _.italic())


@final
class UnderlinedBlock(MappedBlock):
    def __init__(self, original: Block):
        super().__init__(original, lambda _: _.underlined())


@final
class BlinkingBlock(MappedBlock):
    def __init__(self, original: Block):
        super().__init__(original, lambda _: _.blinking())
