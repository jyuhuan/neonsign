from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple, final

from neonsign.block.block import LayoutBlock, Block
from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size


@final
@dataclass
class PaddedBlock(LayoutBlock):
    original: Block
    padding_top: int = field(default_factory=lambda: 0)
    padding_right: int = field(default_factory=lambda: 0)
    padding_bottom: int = field(default_factory=lambda: 0)
    padding_left: int = field(default_factory=lambda: 0)

    @property
    def subblocks(self) -> Tuple[Block, ...]:
        return (self.original,)

    @property
    def padding_horizontal(self) -> int:
        return self.padding_left + self.padding_right

    @property
    def padding_vertical(self) -> int:
        return self.padding_top + self.padding_bottom

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:

        if width_constraint is None and height_constraint is None:
            return self.original.unconstrained_size.increased_by(
                width_delta=self.padding_horizontal,
                height_delta=self.padding_vertical
            )

        elif width_constraint is not None and height_constraint is None:
            if width_constraint == 0:
                return Size.zero()
            if width_constraint <= self.padding_horizontal:
                return Size(
                    width=width_constraint,
                    height=self.padding_vertical
                )
            return (
                self.original.measure(
                    width_constraint=width_constraint - self.padding_horizontal
                )
                .increased_by(
                    width_delta=self.padding_horizontal,
                    height_delta=self.padding_vertical
                )
            )

        elif width_constraint is None and height_constraint is not None:
            if height_constraint == 0:
                return Size.zero()
            if height_constraint <= self.padding_vertical:
                return Size(
                    width=self.padding_horizontal,
                    height=height_constraint
                )
            return (
                self.original.measure(
                    height_constraint=height_constraint - self.padding_vertical
                )
                .increased_by(
                    width_delta=self.padding_horizontal,
                    height_delta=self.padding_vertical
                )
            )

        else:
            if width_constraint == 0 or height_constraint == 0:
                return Size.zero()

            has_enough_width = width_constraint >= self.padding_horizontal
            has_enough_height = height_constraint >= self.padding_vertical

            if not has_enough_width and has_enough_height:
                return Size(
                    width=width_constraint,
                    height=self.padding_vertical
                )
            elif has_enough_width and not has_enough_height:
                return Size(
                    width=self.padding_horizontal,
                    height=height_constraint
                )
            elif not has_enough_width and not has_enough_height:
                return Size(
                    width=width_constraint,
                    height=height_constraint
                )
            else:
                original_size: Size = self.original.measure(
                    width_constraint=width_constraint - self.padding_horizontal,
                    height_constraint=height_constraint - self.padding_vertical
                )
                return original_size.increased_by(
                    width_delta=self.padding_horizontal,
                    height_delta=self.padding_vertical
                )

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        num_horizontal_spaces_needed = self.padding_left + self.padding_right
        num_vertical_spaces_needed = self.padding_top + self.padding_bottom

        if (
            num_horizontal_spaces_needed > granted_size.width or
            num_vertical_spaces_needed > granted_size.height
        ):
            return (Rect.zero(),)

        available_size_for_content: Size = granted_size.increased_by(
            width_delta=-num_horizontal_spaces_needed,
            height_delta=-num_vertical_spaces_needed
        )

        original_size: Size = self.original.measure(
            width_constraint=available_size_for_content.width,
            height_constraint=available_size_for_content.height
        )

        return (
            Rect(
                top_left=Point(x=self.padding_left, y=self.padding_top),
                size=original_size,
            ),
        )
