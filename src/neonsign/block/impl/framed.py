from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, final

from neonsign.block.block import Block, LayoutBlock, LeafBlock
from neonsign.block.canvas import Canvas, PixelSource, px
from neonsign.block.frame_styles import FrameStyle
from neonsign.block.measurable import FlexibleMeasurable
from neonsign.core.colors import Color
from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size


@final
class FramedBlock(LayoutBlock):

    def __init__(
            self,
            original: Block,
            style: FrameStyle = FrameStyle.REGULAR,
            title: Optional[Block] = None,
            color: Optional[Color] = None,
    ):
        self.original = original
        self.style = style
        self.title = title
        self.color = color

        self._padded_original = self.original.padded(1)

        self._frame = _Frame(style=self.style)
        if self.color is not None:
            self._frame = self._frame.foreground(self.color)

        if self.title is None:
            self._padded_title = None
        else:
            self._padded_title = title.padded_horizontally(1)

    @property
    def subblocks(self) -> Tuple[Block, ...]:
        return (
            self._padded_original,
            self._frame,
        ) + ((self._padded_title,) if self.title is not None else ())

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        if (
            (width_constraint is not None and width_constraint < 2) or
            (height_constraint is not None and height_constraint < 2)
        ):
            return Size.zero()
        return self.original.padded(num_spaces=1).measure(
            width_constraint=width_constraint,
            height_constraint=height_constraint
        )

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        frame_rect = Rect.from_origin(
            size=self._frame.measure(
                width_constraint=granted_size.width,
                height_constraint=granted_size.height
            )
        )

        padded_original_size: Size = self._padded_original.measure(
            width_constraint=granted_size.width,
            height_constraint=granted_size.height
        )

        padded_original_rect = Rect.from_origin(
            size=self.original.padded(1).measure(
                width_constraint=granted_size.width,
                height_constraint=granted_size.height
            )
        )

        rects = [padded_original_rect, frame_rect]

        if (
                self.title is not None and
                padded_original_size > Size(width=2, height=2)
        ):
            size_available_for_title: Size = Size(
                width=padded_original_size.width - 2,
                height=1
            )

            granted_size_for_title_block: Size = self._padded_title.measure(
                width_constraint=size_available_for_title.width,
                height_constraint=1
            )
            title_start_x: int = (
                frame_rect.size.width // 2 - granted_size_for_title_block.width // 2
            )

            title_rect = Rect(
                top_left=Point(x=title_start_x, y=0),
                size=granted_size_for_title_block
            )

            rects.append(title_rect)

        return tuple(rects)


@dataclass
class _Frame(LeafBlock, FlexibleMeasurable):
    style: FrameStyle

    def _render(self, granted_size: Size) -> Canvas:
        def pixel_factory(x: int, y: int) -> PixelSource:
            if x == 0 and y == 0:
                return self.style.top_left
            if x == granted_size.width - 1 and y == 0:
                return self.style.top_right
            if x == 0 and y == granted_size.height - 1:
                return self.style.bottom_left
            if (
                x == granted_size.width - 1 and
                y == granted_size.height - 1
            ):
                return self.style.bottom_right
            if (
                1 <= x <= granted_size.width - 1 and
                (y == 0 or y == granted_size.height - 1)
            ):
                return self.style.horizontal_line
            if (
                (x == 0 or x == granted_size.width - 1) and
                1 <= y <= granted_size.height - 1
            ):
                return self.style.vertical_line
            return px()
        return Canvas.of(size=granted_size, pixel_factory=pixel_factory)
