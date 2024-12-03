from __future__ import annotations

from typing import Optional, Tuple

from neonsign.block.block import LayoutBlock, Block
from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size


class FixedWidthBlock(LayoutBlock):

    def __init__(self, original: Block, fixed_width: int):
        self.original = original
        self.fixed_width = fixed_width

    @property
    def subblocks(self) -> Tuple[Block, ...]:
        return (self.original,)

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        return self.original.measure(
            width_constraint=self.fixed_width,
            height_constraint=height_constraint
        ).with_updated_width(self.fixed_width)

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        return (
            Rect(
                top_left=Point.origin(),
                size= self.original.measure(
                    width_constraint=granted_size.width,
                    height_constraint=granted_size.height
                )
            ),
        )


class FixedHeightBlock(LayoutBlock):

    def __init__(self, original: Block, fixed_height: int):
        self.original = original
        self.fixed_height = fixed_height

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
            height_constraint=self.fixed_height
        ).with_updated_height(self.fixed_height)

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        return (
            Rect(
                top_left=Point.origin(),
                size= self.original.measure(
                    width_constraint=granted_size.width,
                    height_constraint=granted_size.height
                )
            ),
        )


class FixedSizeBlock(LayoutBlock):

    def __init__(
            self,
            original: Block,
            fixed_width: int,
            fixed_height: int
    ):
        self.original = original
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

    @property
    def subblocks(self) -> Tuple[Block, ...]:
        return (self.original,)

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        return (
            self.original.measure(
                width_constraint=self.fixed_width,
                height_constraint=self.fixed_height
            )
            .with_updated_width(self.fixed_width)
            .with_updated_height(self.fixed_height)
        )

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        return (
            Rect(
                top_left=Point.origin(),
                size= self.original.measure(
                    width_constraint=granted_size.width,
                    height_constraint=granted_size.height
                )
            ),
        )
