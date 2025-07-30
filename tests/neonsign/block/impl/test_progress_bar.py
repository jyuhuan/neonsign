from unittest import TestCase

from neonsign import ProgressBar
from neonsign.block.canvas import Canvas, px
from neonsign.core.size import Size
from tests.neonsign.block.utilities import run_size_and_render_tests


class TestProgressBar(TestCase):

    def test(self):

        def expected_canvas(size: Size) -> Canvas:
            if size.width == 0 or size.height == 0:
                return Canvas.empty()
            pixels = {
                Size(width=2, height=1):  '▌ ',
                Size(width=4, height=1):  '█▏  ',
                Size(width=6, height=1):  '█▊    ',
                Size(width=8, height=1):  '██▍     ',
                Size(width=10, height=1): '███       ',
                Size(width=12, height=1): '███▌        ',
                Size(width=14, height=1): '████▏         ',
                Size(width=16, height=1): '████▊           ',
                Size(width=18, height=1): '█████▍            ',
                Size(width=20, height=1): '██████              ',
                Size(width=22, height=1): '██████▌               ',
                Size(width=24, height=1): '███████▏                ',
                Size(width=26, height=1): '███████▊                  ',
                Size(width=28, height=1): '████████▍                   ',
            }[size]
            return Canvas.from_pixels([[px(char) for char in pixels]])

        run_size_and_render_tests(
            self,
            ProgressBar(progress=0.3),
            expected_unconstrained_size=Size(width=ProgressBar.DEFAULT_WIDTH, height=1),
            expected_size_given_width_constraint_only=lambda w: Size(width=w, height=1) if w != 0 else Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size(width=ProgressBar.DEFAULT_WIDTH, height=1) if h != 0 else Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size(width=w, height=1) if w != 0 and h != 0 else Size.zero(),
            expected_canvas=expected_canvas
        )


    def test_instantiation(self):

        with self.assertRaises(ValueError) as e:
            ProgressBar(progress=-0.5)
        self.assertEqual(
            str(e.exception),
            'progress cannot be negative, but -0.5 was provided!'
        )

        with self.assertRaises(ValueError) as e:
            ProgressBar(progress=1.5)
        self.assertEqual(
            str(e.exception),
            'progress cannot be greater than 1, but 1.5 was provided!'
        )

