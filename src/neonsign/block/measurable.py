import sys
from abc import ABC, abstractmethod
from typing import Optional

from neonsign.core.size import Size


class Measurable(ABC):
    """An object whose size can be measured."""

    @abstractmethod
    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        """Calculates the size that satisfies the specified height and width
        constraints.

        Args:

            width_constraint: The maximum width that the text block can have.
                When this is set to None, the text block's width is
                unconstrained, and it can take as much horizontal space as it
                needs.

            height_constraint: The maximum height that the text block can have.
                When this is set to None, the text block's height is
                unconstrained, and it can take as much horizontal space as it
                needs.

        Returns:
            The size satisfying the constraints.

        This is the method any class implementing ``Measurable`` should
        implement. When using a ``Measurable``, the :func:`Measurable.measure`
        method should be called.

        You should handle all 4 combinations of the constraints as follows in
        your implementation::

            if width_constraint is None and height_constraint is None:
                # Case 1: No constraints.
                #   Return the size that allows all contents to be visible.
                #   Use as much width and height as needed to present all
                #   contents without text wrapping, truncation, clipping, or
                #   scaling, etc.

            elif width_constraint is not None and height_constraint is None:
                # Case 2: Only constrained horizontally.
                #   Return the size that allows all contents to be visible
                #   without exceeding the given maximum width constraint.
                #   Because the height is unconstrained, you should use as much
                #   vertical space as needed so all contents are visible.

            elif width_constraint is None and height_constraint is not None:
                # Case 3: Only constrained vertically.
                #   Return the size that allows all contents to be visible
                #   without exceeding the given maximum height constraint.
                #   Because the width is unconstrained, you should use as much
                #   horizontal space as needed so all contents are visible.

            else:
                # Case 4: Constrained in both axes.
                #   Return the size that is the same size or smaller than the
                #   constraints. Because both the width and height are
                #   constrained, there may not be space for all contents to be
                #   visible. When there isn't enough space, you should reduce
                #   your contents elegantly, by using text wrapping, truncation,
                #   clipping, or scaling, etc.

        """
        pass

    def measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        """Calculates the size that satisfies the specified height and width
        constraints.

        Args:

            width_constraint: The maximum width that the text block can have.
                When this is set to None, the text block's width is
                unconstrained, and it can take as much horizontal space as it
                needs.

            height_constraint: The maximum height that the text block can have.
                When this is set to None, the text block's height is
                unconstrained, and it can take as much horizontal space as it
                needs.

        Returns:
            The size satisfying the constraints.
        """
        size = self._measure(
            width_constraint=width_constraint,
            height_constraint=height_constraint
        )
        if size.width == 0 or size.height == 0:
            return Size.zero()
        else:
            return size

    @property
    def unconstrained_size(self) -> Size:
        return self.measure(width_constraint=None, height_constraint=None)

    def is_flexible_in_x_axis(
            self,
            height_constraint: Optional[int] = None
    ) -> bool:
        min_width: int = self.measure(
            width_constraint=0,
            height_constraint=height_constraint
        ).width
        max_width: int = self.measure(
            width_constraint=sys.maxsize,
            height_constraint=height_constraint
        ).width
        return min_width == 0 and max_width >= sys.maxsize

    def is_flexible_in_y_axis(
            self,
            width_constraint: Optional[int] = None
    ) -> bool:
        min_height: int = self.measure(
            width_constraint=width_constraint,
            height_constraint=0
        ).height
        max_height: int = self.measure(
            width_constraint=width_constraint,
            height_constraint=sys.maxsize
        ).height
        return min_height == 0 and max_height >= sys.maxsize


class FlexibleMeasurable(Measurable):

    @property
    def default_size(self) -> Size:
        return Size(width=1, height=1)

    def _measure(
            self,
            width_constraint: Optional[int] = None,
            height_constraint: Optional[int] = None
    ) -> Size:
        if width_constraint is None and height_constraint is None:
            return self.default_size
        elif width_constraint is not None and height_constraint is None:
            if width_constraint == 0:
                return Size.zero()
            return Size(
                width=width_constraint,
                height=self.default_size.height
            )
        elif width_constraint is None and height_constraint is not None:
            if height_constraint == 0:
                return Size.zero()
            return Size(
                width=self.default_size.width,
                height=height_constraint
            )
        else:
            if width_constraint == 0 or height_constraint == 0:
                return Size.zero()
            return Size(
                width=width_constraint,
                height=height_constraint
            )
