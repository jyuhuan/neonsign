from typing import Optional
from unittest import TestCase

from neonsign.block.cache import LayoutContainer
from neonsign.block.measurable import Measurable
from neonsign.core.size import Size


class TestMeasurable(TestCase):

    def test_zero_size_normalization(self):

        class ZeroWidthMeasurable(Measurable):
            def _measure(
                    self,
                    width_constraint: Optional[int] = None,
                    height_constraint: Optional[int] = None
            ) -> Size:
                return Size(width=0, height=1)

        zero_width_measurable = ZeroWidthMeasurable()
        with LayoutContainer(root=zero_width_measurable):
            self.assertEqual(
                Size.zero(),
                zero_width_measurable.measure()
            )

        class ZeroHeightMeasurable(Measurable):
            def _measure(
                    self,
                    width_constraint: Optional[int] = None,
                    height_constraint: Optional[int] = None
            ) -> Size:
                return Size(width=0, height=1)

        zero_height_measurable = ZeroHeightMeasurable()
        with LayoutContainer(root=zero_height_measurable):
            self.assertEqual(
                Size.zero(),
                zero_height_measurable.measure()
            )
