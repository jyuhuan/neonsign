from __future__ import annotations

from typing import Dict, List, Optional, Tuple, final

from neonsign.block.alignment import Alignment
from neonsign.block.layout_calculation import ItemsDistributor
from neonsign.block.block import LayoutBlock, Block
from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size


@final
class Row(LayoutBlock):

    def __init__(
            self,
            *blocks: Block,
            alignment: Alignment = Alignment.START,
    ):
        self.blocks: Tuple[Block, ...] = blocks
        self.alignment: Alignment = alignment

    @property
    def subblocks(self) -> Tuple[Block, ...]:
        return self.blocks

    def _measure_each(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> List[Size]:
        if len(self.blocks) == 0:
            return []

        flexibility = [
            block.is_flexible_in_x_axis(height_constraint)
            for block in self.blocks
        ]

        inflexible_blocks: Dict[int, Block] = {
            i: block for i, block in enumerate(self.blocks)
            if not flexibility[i]
        }
        flexible_blocks: Dict[int, Block] = {
            i: block for i, block in enumerate(self.blocks)
            if flexibility[i]
        }

        if width_constraint is None and height_constraint is None:
            return [
                block.unconstrained_size
                for block in inflexible_blocks.values()
            ]

        elif width_constraint is None and height_constraint is not None:
            return [
                block.measure(height_constraint=height_constraint)
                for block in inflexible_blocks.values()
            ]

        else:
            sizes: List[Size] = [Size.zero() for _ in self.blocks]
            remaining_width = width_constraint
            for i, block in inflexible_blocks.items():
                if remaining_width <= 0:
                    break
                size: Size = block.measure(
                    width_constraint=min(remaining_width, width_constraint),
                    height_constraint=height_constraint
                )
                sizes[i] = size
                remaining_width -= size.width

            total_inflexible_size = Size(
                width=sum(_.width for _ in sizes),
                height=max(_.height for _ in sizes)
            )

            if remaining_width <= 0 or len(flexible_blocks) == 0:
                return sizes
            else:
                # Distribute the remaining width among flexible blocks:
                width_distributor = ItemsDistributor(
                    num_items=remaining_width,
                    num_recipients=len(flexible_blocks)
                )
                k = 0
                for i, block in flexible_blocks.items():
                    sizes[i] = Size(
                        width=width_distributor.num_items_for_recipient(k),
                        height=total_inflexible_size.height
                    )
                    k += 1
                return sizes

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        sizes = self._measure_each(
            width_constraint=width_constraint,
            height_constraint=height_constraint
        )
        return Size(
            width=sum(_.width for _ in sizes),
            height=max([_.height for _ in sizes], default=0)
        )

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        if len(self.blocks) == 0:
            return ()

        sizes: List[Size] = self._measure_each(
            width_constraint=granted_size.width,
            height_constraint=granted_size.height
        )
        max_height: int = max(_.height for _ in sizes)
        rects: List[Rect] = []
        last_x: int = 0
        for size in sizes:
            rect = Rect(
                top_left=Point(
                    x=last_x,
                    y={
                        Alignment.START: lambda: 0,
                        Alignment.CENTER: lambda: max_height // 2 - size.height // 2,
                        Alignment.END: lambda: max_height - size.height,
                    }[self.alignment]()
                ),
                size=size
            )
            rects.append(rect)
            last_x += size.width
        return tuple(rects)
