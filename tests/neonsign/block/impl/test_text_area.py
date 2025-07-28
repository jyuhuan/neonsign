from unittest import TestCase

from neonsign import TextArea
from neonsign.block.canvas import Canvas, px
from neonsign.core.size import Size
from tests.neonsign.block.utilities import run_size_and_render_tests


class TestTextArea(TestCase):

    def test(self):

        empty_cases = [
            TextArea(''),
            TextArea('', max_number_of_lines=1),
            TextArea('', max_number_of_lines=5)
        ]

        for case in empty_cases:
            run_size_and_render_tests(
                self,
                case,
                expected_unconstrained_size=Size(width=TextArea.DEFAULT_WIDTH, height=1),
                expected_size_given_width_constraint_only=lambda w: Size(width=w, height=1) if w != 0 else Size.zero(),
                expected_size_given_height_constraint_only=lambda h: Size(width=TextArea.DEFAULT_WIDTH, height=1) if h != 0 else Size.zero(),
                expected_size_given_both_constraints=lambda w, h: Size(width=w, height=1) if w != 0 and h != 0 else Size.zero(),
                expected_canvas=lambda size: Canvas.empty() if size.area == 0 else Canvas.of(size, lambda x, y: ' ')
            )

        def expected_size_given_width_constraint_only(w: int) -> Size:
            if w < 5:
                return {
                    0: lambda: Size.zero(),
                    1: lambda: Size(width=1, height=5),
                    2: lambda: Size(width=2, height=3),
                    3: lambda: Size(width=3, height=2),
                    4: lambda: Size(width=4, height=2),
                }[w]()
            return Size(width=w, height=1)

        def expected_size_given_height_constraint_only(h: int) -> Size:
            if h == 0:
                return Size.zero()
            return Size(width=5, height=1)

        def expected_size_given_both_constraints(w: int, h: int) -> Size:
            if w == 0 or h == 0:
                return Size.zero()
            if w == 1:
                return Size(width=1, height=min(h, 5))
            if w == 2:
                return Size(width=2, height=min(h, 3))
            if w == 3:
                return Size(width=3, height=min(h, 2))
            if w == 4:
                return Size(width=4, height=min(h, 2))
            return Size(width=w, height=1)

        def expected_canvas(size: Size) -> Canvas:
            size_to_canvas = {
                Size.zero(): lambda: Canvas.empty(),

                Size(width=1, height=1): lambda: Canvas.from_pixels([
                    [px('…')]
                ]),
                Size(width=1, height=2): lambda: Canvas.from_pixels([
                    [px('1')],
                    [px('…')],
                ]),
                Size(width=1, height=3): lambda: Canvas.from_pixels([
                    [px('1')],
                    [px('2')],
                    [px('…')],
                ]),
                Size(width=1, height=4): lambda: Canvas.from_pixels([
                    [px('1')],
                    [px('2')],
                    [px('3')],
                    [px('…')],
                ]),
                Size(width=1, height=5): lambda: Canvas.from_pixels([
                    [px('1')],
                    [px('2')],
                    [px('3')],
                    [px('4')],
                    [px('5')],
                ]),

                Size(width=2, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('…')]
                ]),
                Size(width=2, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px('…')],
                ]),
                Size(width=2, height=3): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px('4')],
                    [px('5'), px(' ')],
                ]),

                Size(width=3, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('…')]
                ]),
                Size(width=3, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3')],
                    [px('4'), px('5'), px(' ')],
                ]),

                Size(width=4, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('…')]
                ]),
                Size(width=4, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('4')],
                    [px('5'), px(' '), px(' '), px(' ')],
                ]),

                Size(width=5, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('4'), px('5')]
                ]),

                Size(width=12, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('4'), px('5')] + [px(' ') for _ in range(12 - 5)]
                ]),

                Size(width=18, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('4'), px('5')] + [px(' ') for _ in range(18 - 5)]
                ]),

                Size(width=26, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('4'), px('5')] + [px(' ') for _ in range(26 - 5)]
                ]),
                Size(width=28, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('4'), px('5')] + [px(' ') for _ in range(28 - 5)]
                ]),

            }

            if size in size_to_canvas:
                return size_to_canvas[size]()

            return Canvas.from_pixels([
                [px('1'), px('2'), px('3'), px('4'), px('5')] +
                [px(' ') for _ in range(size.width - 5)]
            ])

        run_size_and_render_tests(
            self,
            TextArea('12345'),
            expected_unconstrained_size=Size(width=5, height=1),
            expected_size_given_width_constraint_only=expected_size_given_width_constraint_only,
            expected_size_given_height_constraint_only=expected_size_given_height_constraint_only,
            expected_size_given_both_constraints=expected_size_given_both_constraints,
            expected_canvas=expected_canvas
        )

    def test_instantiation(self):
        with self.assertRaises(ValueError) as e:
            TextArea('', max_number_of_lines=0)
        self.assertEqual(
            str(e.exception),
            'max_number_of_lines must be a positive integer and not 0!'
        )

        with self.assertRaises(ValueError) as e:
            TextArea('', max_number_of_lines=-1)
        self.assertEqual(
            str(e.exception),
            'max_number_of_lines must be a positive integer and not -1!'
        )
