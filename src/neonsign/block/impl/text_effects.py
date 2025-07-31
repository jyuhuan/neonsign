from __future__ import annotations

from typing import Callable, final

from neonsign.block.block import Block, WrapperBlock
from neonsign.block.canvas import (
    Canvas, Pixel, PixelSource,
    StyledStringPixel
)
from neonsign.core.colors import Color
from neonsign.core.size import Size
from neonsign.string.styled_string import StyledString


class MappedBlock(WrapperBlock):

    def __init__(
            self,
            original: Block,
            f: Callable[[StyledString], StyledString]
    ):
        super().__init__(original)
        self.f = f

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
        self.color = color


@final
class BackgroundColoredBlock(MappedBlock):
    def __init__(self, original: Block, color: Color):
        super().__init__(original, lambda _: _.background(color))
        self.color = color


@final
class ColorInvertedBlock(MappedBlock):
    def __init__(self, original: Block):
        super().__init__(original, lambda _: _.inverted())


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
