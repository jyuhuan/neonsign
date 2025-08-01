from __future__ import annotations

from typing import Dict, List, Optional, Tuple, final

from neonsign.block.alignment import Alignment
from neonsign.block.layout_calculation import ItemsDistributor
from neonsign.block.block import LayoutBlock, Block
from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size


@final
class Column(LayoutBlock):

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
            block.is_flexible_in_y_axis(width_constraint)
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

        elif width_constraint is not None and height_constraint is None:
            return [
                block.measure(width_constraint=width_constraint)
                for block in inflexible_blocks.values()
            ]

        else:
            sizes: List[Size] = [Size.zero() for _ in self.blocks]
            remaining_height = height_constraint
            for i, block in inflexible_blocks.items():
                if remaining_height <= 0:
                    break
                size: Size = block.measure(
                    width_constraint=width_constraint,
                    height_constraint=min(remaining_height, height_constraint)
                )
                sizes[i] = size
                remaining_height -= size.height

            total_inflexible_size = Size(
                width=max(_.width for _ in sizes),
                height=sum(_.height for _ in sizes)
            )

            if remaining_height <= 0 or len(flexible_blocks) == 0:
                return sizes
            else:
                # Distribute the remaining height among flexible blocks:
                height_distributor = ItemsDistributor(
                    num_items=remaining_height,
                    num_recipients=len(flexible_blocks)
                )
                k = 0
                for i, block in flexible_blocks.items():
                    sizes[i] = Size(
                        width=total_inflexible_size.width,
                        height=height_distributor.num_items_for_recipient(k)
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
            width=max([_.width for _ in sizes], default=0),
            height=sum([_.height for _ in sizes])
        )

    def _get_rects(self, granted_size: Size) -> Tuple[Rect, ...]:
        if len(self.blocks) == 0:
            return ()

        sizes: List[Size] = self._measure_each(
            width_constraint=granted_size.width,
            height_constraint=granted_size.height
        )
        max_width: int = max(_.width for _ in sizes)
        rects: List[Rect] = []
        last_y: int = 0
        for size in sizes:
            rect = Rect(
                top_left=Point(
                    x={
                        Alignment.START: lambda: 0,
                        Alignment.CENTER: lambda: max_width // 2 - size.width // 2,
                        Alignment.END: lambda: max_width - size.width,
                    }[self.alignment](),
                    y=last_y
            ),
                size=size
            )
            rects.append(rect)
            last_y += size.height
        return tuple(rects)
