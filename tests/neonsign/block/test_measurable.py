from typing import Optional
from unittest import TestCase

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
        self.assertEqual(
            Size.zero(),
            ZeroWidthMeasurable().measure()
        )

        class ZeroHeightMeasurable(Measurable):
            def _measure(
                    self,
                    width_constraint: Optional[int] = None,
                    height_constraint: Optional[int] = None
            ) -> Size:
                return Size(width=0, height=1)
        self.assertEqual(
            Size.zero(),
            ZeroHeightMeasurable().measure()
        )
