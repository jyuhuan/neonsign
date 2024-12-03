from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from neonsign.block.canvas import Canvas
from neonsign.block.frame_styles import FrameStyle
from neonsign.block.measurable import Measurable
from neonsign.block.renderable import Renderable
from neonsign.core.colors import Color
from neonsign.core.rect import Rect
from neonsign.core.size import Size


class Block(Measurable, Renderable, ABC):

    def rendered(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Canvas:
        return self.render(
            granted_size=self.measure(
                width_constraint=width_constraint,
                height_constraint=height_constraint
            )
        )

    def __str__(self) -> str:
        return str(self.rendered())

    def foreground(self, color: Color) -> Block:
        from neonsign.block.impl.text_effects import ForegroundColoredBlock
        return ForegroundColoredBlock(self, color)

    def background(self, color: Color) -> Block:
        from neonsign.block.impl.text_effects import BackgroundColoredBlock
        return BackgroundColoredBlock(self, color)

    def bold(self) -> Block:
        from neonsign.block.impl.text_effects import BoldBlock
        return BoldBlock(self)

    def italic(self) -> Block:
        from neonsign.block.impl.text_effects import ItalicBlock
        return ItalicBlock(self)

    def underlined(self) -> Block:
        from neonsign.block.impl.text_effects import UnderlinedBlock
        return UnderlinedBlock(self)

    def blinking(self) -> Block:
        from neonsign.block.impl.text_effects import BlinkingBlock
        return BlinkingBlock(self)

    def framed(
            self,
            style: FrameStyle = FrameStyle.REGULAR,
            title: Optional[Block] = None,
            color: Optional[Color] = None,
    ) -> Block:
        from neonsign.block.impl.framed import FramedBlock
        return FramedBlock(self, style=style, title=title, color=color)

    def resized(
            self,
            width: Optional[int] = None,
            height: Optional[int] = None
    ) -> Block:
        from neonsign.block.impl.fixed import (
            FixedWidthBlock, FixedHeightBlock, FixedSizeBlock
        )
        if width is None and height is None:
            return self
        elif width is not None and height is None:
            return FixedWidthBlock(self, fixed_width=width)
        elif width is None and height is not None:
            return FixedHeightBlock(self, fixed_height=height)
        else:
            return FixedSizeBlock(self, fixed_width=width, fixed_height=height)

    def padded(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_top=num_spaces,
            padding_right=num_spaces,
            padding_bottom=num_spaces,
            padding_left=num_spaces,
        )

    def padded_horizontally(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_left=num_spaces,
            padding_right=num_spaces
        )

    def padded_vertically(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_top=num_spaces,
            padding_bottom=num_spaces
        )

    def padded_top(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_top=num_spaces,
        )

    def padded_right(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_right=num_spaces,
        )

    def padded_bottom(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_bottom=num_spaces,
        )

    def padded_left(self, num_spaces: int = 1) -> Block:
        from neonsign.block.impl.padded import PaddedBlock
        return PaddedBlock(
            original=self,
            padding_left=num_spaces,
        )


class LeafBlock(Block, ABC):
    pass


class LayoutBlock(Block, ABC):

    @property
    @abstractmethod
    def subblocks(self) -> Tuple[Block, ...]:
        pass

    @abstractmethod
    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        pass

    def get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        return self._get_rects(granted_size=granted_size)

    def _render(self, granted_size: Size) -> Canvas:
        rects: Tuple[Rect, ...] = self.get_rects(granted_size=granted_size)
        renders: Tuple[Canvas, ...] = tuple(
            block.render(granted_size=rect.size)
            for block, rect in zip(self.subblocks, rects)
        )
        canvas: Canvas = Canvas.of(size=granted_size, pixel_factory=lambda x, y: ' ')
        for rect, render in zip(rects, renders):
            canvas = canvas.replace(rect.top_left, rect.size, render)
        return canvas
