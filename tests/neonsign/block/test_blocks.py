from unittest import TestCase

from neonsign import (
    Color, Column, FixedHeightBlock, FixedSizeBlock, FixedWidthBlock,
    FlexibleSpace, FrameStyle, HorizontalSeparator, Label, PaddedBlock, Row,
    VerticalSeparator, s
)
from neonsign.block.canvas import Canvas, px
from neonsign.block.impl.framed import _Frame
from neonsign.block.impl.text_effects import MappedBlock
from neonsign.core.size import Size
from tests.neonsign.block.utilities import MAX, run_size_and_render_tests


class TestBlocks(TestCase):

    def test_label(self):

        run_size_and_render_tests(
            self,
            Label(''),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda _: Size.zero(),
            expected_size_given_height_constraint_only=lambda _: Size.zero(),
            expected_size_given_both_constraints=lambda _1, _2: Size.zero(),
            expected_canvas=lambda _: Canvas.empty()
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
            return Size(width=5, height=1)

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
            return Size(width=5, height=1)

        def expected_canvas(size: Size) -> Canvas:
            return {
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
                ])

            }[size]()

        run_size_and_render_tests(
            self,
            Label('12345'),
            expected_unconstrained_size=Size(width=5, height=1),
            expected_size_given_width_constraint_only=expected_size_given_width_constraint_only,
            expected_size_given_height_constraint_only=expected_size_given_height_constraint_only,
            expected_size_given_both_constraints=expected_size_given_both_constraints,
            expected_canvas=expected_canvas
        )

    def test_flexible_space(self):

        def expected_size_given_width_constraint_only(w: int) -> Size:
            if w == 0:
                return Size.zero()
            return Size(width=w, height=1)

        def expected_size_given_height_constraint_only(h: int) -> Size:
            if h == 0:
                return Size.zero()
            return Size(width=1, height=h)

        def expected_size_given_both_constraints(w: int, h: int) -> Size:
            if w == 0:
                return Size.zero()
            if h == 0:
                return Size.zero()
            return Size(width=w, height=h)

        def expected_canvas(size: Size) -> Canvas:
            if size == Size.zero():
                return Canvas.empty()
            if size > Size.zero():
                return Canvas.of(size, pixel_factory=lambda x, y: ' ')

        run_size_and_render_tests(
            self,
            FlexibleSpace(),
            expected_unconstrained_size=Size(width=1, height=1),
            expected_size_given_width_constraint_only=expected_size_given_width_constraint_only,
            expected_size_given_height_constraint_only=expected_size_given_height_constraint_only,
            expected_size_given_both_constraints=expected_size_given_both_constraints,
            expected_canvas=expected_canvas
        )

    def test_padded_block(self):

        def expected_size_given_width_constraint_only(w: int) -> Size:
            if w < 5:
                return {
                    0: lambda: Size.zero(),
                    1: lambda: Size(width=1, height=2),
                    2: lambda: Size(width=2, height=2),
                    3: lambda: Size(width=3, height=5),
                    4: lambda: Size(width=4, height=4),
                }[w]()
            else:
                return Size(width=5, height=3)

        def expected_size_given_height_constraint_only(h: int) -> Size:
            if h < 3:
                return {
                    0: lambda: Size.zero(),
                    1: lambda: Size(width=2, height=1),
                    2: lambda: Size(width=2, height=2),
                }[h]()
            else:
                return Size(width=5, height=3)

        def expected_size_given_both_constraints(w: int, h: int) -> Size:
            if w == 0 or h == 0:
                return Size.zero()
            if w <= 2 or h <= 2:
                return Size(width=min(w, 2), height=min(h, 2))
            if w == 3:
                return Size(width=3, height=min(5, h))
            if w == 4:
                return Size(width=4, height=min(4, h))
            return Size(width=5, height=3)

        def expected_canvas(size: Size) -> Canvas:
            return {
                Size.zero(): lambda: Canvas.empty(),

                Size(width=1, height=1): lambda: Canvas.from_pixels([
                    [px(' ')],
                ]),
                Size(width=1, height=2): lambda: Canvas.from_pixels([
                    [px(' ')],
                    [px(' ')],
                ]),
                Size(width=1, height=3): lambda: Canvas.from_pixels([
                    [px(' ')],
                    [px(' ')],
                    [px(' ')],
                ]),

                Size(width=2, height=1): lambda: Canvas.from_pixels([
                    [px(' '), px(' ')],
                ]),
                Size(width=2, height=2): lambda: Canvas.from_pixels([
                    [px(' '), px(' ')],
                    [px(' '), px(' ')],
                ]),
                Size(width=2, height=3): lambda: Canvas.from_pixels([
                    [px(' '), px(' ')],
                    [px(' '), px(' ')],
                    [px(' '), px(' ')],
                ]),

                Size(width=3, height=1): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' ')],
                ]),
                Size(width=3, height=2): lambda: Canvas.from_pixels([
                    [px(' '), px(' ')],
                    [px(' '), px(' ')],
                ]),
                Size(width=3, height=3): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' ')],
                    [px(' '), px('…'), px(' ')],
                    [px(' '), px(' '), px(' ')],
                ]),
                Size(width=3, height=4): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' ')],
                    [px(' '), px('1'), px(' ')],
                    [px(' '), px('…'), px(' ')],
                    [px(' '), px(' '), px(' ')],
                ]),
                Size(width=3, height=5): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' ')],
                    [px(' '), px('1'), px(' ')],
                    [px(' '), px('2'), px(' ')],
                    [px(' '), px('3'), px(' ')],
                    [px(' '), px(' '), px(' ')],
                ]),

                Size(width=4, height=1): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' '), px(' ')],
                ]),
                Size(width=4, height=2): lambda: Canvas.from_pixels([
                    [px(' '), px(' ')],
                    [px(' '), px(' ')],
                ]),
                Size(width=4, height=3): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px('1'), px('…'), px(' ')],
                    [px(' '), px(' '), px(' '), px(' ')],
                ]),
                Size(width=4, height=4): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px('1'), px('2'), px(' ')],
                    [px(' '), px('3'), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' ')],
                ]),

                Size(width=5, height=1): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                ]),
                Size(width=5, height=2): lambda: Canvas.from_pixels([
                    [px(' '), px(' ')],
                    [px(' '), px(' ')],
                ]),
                Size(width=5, height=3): lambda: Canvas.from_pixels([
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px('1'), px('2'), px('3'), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                ]),
            }[size]()

        run_size_and_render_tests(
            self,
            PaddedBlock(
                original=Label('123'),
                padding_top=1,
                padding_right=1,
                padding_bottom=1,
                padding_left=1,
            ),
            expected_unconstrained_size=Size(width=5, height=3),
            expected_size_given_height_constraint_only=expected_size_given_height_constraint_only,
            expected_size_given_width_constraint_only=expected_size_given_width_constraint_only,
            expected_size_given_both_constraints=expected_size_given_both_constraints,
            expected_canvas=expected_canvas,
            width_constraints_to_test=list(range(0, 10)) + [MAX],
            height_constraints_to_test=list(range(0, 10)) + [MAX],
        )

        self.assertEqual(
            (Label('1'),),
            Label('1').padded().subblocks
        )

    def test_framed_block(self):

        def expected_size_given_width_constraint_only(w: int) -> Size:
            if w < 6:
                return {
                    0: lambda: Size.zero(),
                    1: lambda: Size.zero(),
                    2: lambda: Size(width=2, height=2),
                    3: lambda: Size(width=3, height=6),
                    4: lambda: Size(width=4, height=4),
                    5: lambda: Size(width=5, height=4)
                }[w]()
            else:
                return Size(width=6, height=3)

        def expected_size_given_height_constraint_only(h: int) -> Size:
            if h < 3:
                return {
                    0: lambda: Size.zero(),
                    1: lambda: Size.zero(),
                    2: lambda: Size.square(2),
                }[h]()
            return Size(width=6, height=3)

        def expected_size_given_both_constraints(w: int, h: int) -> Size:
            if w < 2 or h < 2:
                return Size.zero()
            if w == 2 or h == 2:
                return Size.square(2)
            if w == 3:
                return Size(width=3, height=min(6, h))
            if w == 4:
                return Size(width=4, height=min(4, h))
            if w == 5:
                return Size(width=5, height=min(4, h))
            return Size(width=6, height=3)

        def expected_canvas(size: Size) -> Canvas:
            return {
                Size.zero(): lambda: Canvas.empty(),
                Size(width=2, height=2): lambda: Canvas.from_pixels([
                    [px('┌'), px('┐')],
                    [px('└'), px('┘')],
                ]),
                Size(width=3, height=3): lambda: Canvas.from_pixels([
                    [px('┌'), px('─'), px('┐')],
                    [px('│'), px('…'), px('│')],
                    [px('└'), px('─'), px('┘')],
                ]),
                Size(width=3, height=4): lambda: Canvas.from_pixels([
                    [px('┌'), px('─'), px('┐')],
                    [px('│'), px('1'), px('│')],
                    [px('│'), px('…'), px('│')],
                    [px('└'), px('─'), px('┘')],
                ]),
                Size(width=3, height=5): lambda: Canvas.from_pixels([
                    [px('┌'), px('─'), px('┐')],
                    [px('│'), px('1'), px('│')],
                    [px('│'), px('2'), px('│')],
                    [px('│'), px('…'), px('│')],
                    [px('└'), px('─'), px('┘')],
                ]),
                Size(width=3, height=6): lambda: Canvas.from_pixels([
                    [px('┌'), px('─'), px('┐')],
                    [px('│'), px('1'), px('│')],
                    [px('│'), px('2'), px('│')],
                    [px('│'), px('3'), px('│')],
                    [px('│'), px('4'), px('│')],
                    [px('└'), px('─'), px('┘')],
                ]),
                Size(width=4, height=3): lambda: Canvas.from_pixels(
                    [
                        [px('┌'), px('─'), px('─'), px('┐')],
                        [px('│'), px('1'), px('…'), px('│')],
                        [px('└'), px('─'), px('─'), px('┘')],
                    ]
                ),
                Size(width=4, height=4): lambda: Canvas.from_pixels(
                    [
                        [px('┌'), px('─'), px('─'), px('┐')],
                        [px('│'), px('1'), px('2'), px('│')],
                        [px('│'), px('3'), px('4'), px('│')],
                        [px('└'), px('─'), px('─'), px('┘')],
                    ]
                ),
                Size(width=5, height=3): lambda: Canvas.from_pixels(
                    [
                        [px('┌'), px(' '), px('…'), px(' '), px('┐')],
                        [px('│'), px('1'), px('2'), px('…'), px('│')],
                        [px('└'), px('─'), px('─'), px('─'), px('┘')],
                    ]
                ),
                Size(width=5, height=4): lambda: Canvas.from_pixels(
                    [
                        [px('┌'), px(' '), px('…'), px(' '), px('┐')],
                        [px('│'), px('1'), px('2'), px('3'), px('│')],
                        [px('│'), px('4'), px(' '), px(' '), px('│')],
                        [px('└'), px('─'), px('─'), px('─'), px('┘')],
                    ]
                ),
                Size(width=6, height=3): lambda: Canvas.from_pixels(
                    [
                        [px('┌'), px(' '), px('a'), px('b'), px(' '), px('┐')],
                        [px('│'), px('1'), px('2'), px('3'), px('4'), px('│')],
                        [px('└'), px('─'), px('─'), px('─'), px('─'), px('┘')],
                    ]
                ),

            }[size]()

        run_size_and_render_tests(
            self,
            Label('1234').framed(title=Label('ab')),
            expected_unconstrained_size=Size(width=6, height=3),
            expected_size_given_width_constraint_only=expected_size_given_width_constraint_only,
            expected_size_given_height_constraint_only=expected_size_given_height_constraint_only,
            expected_size_given_both_constraints=expected_size_given_both_constraints,
            expected_canvas=expected_canvas
        )

        # Test colored frame:
        self.assertEqual(
            Canvas.from_pixels([
                [px(s('┌').foreground(Color.GREEN)), px(s('─').foreground(Color.GREEN)), px(s('─').foreground(Color.GREEN)), px(s('─').foreground(Color.GREEN)), px(s('┐').foreground(Color.GREEN))],
                [px(s('│').foreground(Color.GREEN)), px('1'), px('2'), px('3'),px(s('│').foreground(Color.GREEN))],
                [px(s('└').foreground(Color.GREEN)), px(s('─').foreground(Color.GREEN)), px(s('─').foreground(Color.GREEN)), px(s('─').foreground(Color.GREEN)), px(s('┘').foreground(Color.GREEN))],
            ]),
            Label('123').framed(color=Color.GREEN).rendered()
        )

        self.assertEqual(
            (
                Label('1').padded(1),
                _Frame(style=FrameStyle.REGULAR)
            ),
            Label('1').framed().subblocks
        )
        self.assertEqual(
            (
                Label('1').padded(1),
                _Frame(style=FrameStyle.REGULAR),
                Label('a').padded_horizontally(1)
            ),
            Label('1').framed(title=Label('a')).subblocks
        )

    def test_column(self):
        # Case 1: An empty column:
        run_size_and_render_tests(
            self,
            Column(),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 2: A column containing a flexible block
        run_size_and_render_tests(
            self,
            Column(FlexibleSpace()),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 3: A column containing only an inflexible block
        label_1 = Label('123')
        run_size_and_render_tests(
            self,
            Column(label_1),
            expected_unconstrained_size=label_1.unconstrained_size,
            expected_size_given_width_constraint_only=lambda w: label_1.measure(width_constraint=w),
            expected_size_given_height_constraint_only=lambda h: label_1.measure(height_constraint=h),
            expected_size_given_both_constraints=lambda w, h: label_1.measure(width_constraint=w, height_constraint=h),
            expected_canvas=lambda size: label_1.render(granted_size=size)
        )

        # Case 4: A mix of flexible and inflexible blocks
        label_2 = Label('abcde')
        run_size_and_render_tests(
            self,
            Column(label_1, FlexibleSpace(), label_2),
            expected_unconstrained_size=Size(width=5, height=2),
            expected_size_given_width_constraint_only=lambda w: Size(
                width=max([
                    label_1.measure(width_constraint=w).width,
                    label_2.measure(width_constraint=w).width
                ]),
                height=sum([
                    label_1.measure(width_constraint=w).height,
                    label_2.measure(width_constraint=w).height
                ])
            ),
            expected_size_given_height_constraint_only=lambda h: Size(
                width=max([
                    label_1.measure(height_constraint=h).width,
                    label_2.measure(height_constraint=h).width
                ]),
                height=h
            ),
            expected_size_given_both_constraints=lambda w, h: Size(
                width=min(5, w),
                height=h
            ) if w != 0 and h != 0 else Size.zero(),
            expected_canvas=lambda size: {
                Size.zero(): lambda: Canvas.empty(),
                Size(width=2, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                ]),
                Size(width=2, height=4): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                    [px('a'), px('b')],
                    [px('c'), px('…')],
                ]),
                Size(width=2, height=5): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                    [px('a'), px('b')],
                    [px('c'), px('d')],
                    [px('e'), px(' ')],
                ]),
                Size(width=2, height=6): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                    [px(' '), px(' ')],
                    [px('a'), px('b')],
                    [px('c'), px('d')],
                    [px('e'), px(' ')],
                ]),
                Size(width=4, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' ')],
                    [px('a'), px('b'), px('c'), px('…')],
                ]),
                Size(width=4, height=3): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' ')],
                    [px('a'), px('b'), px('c'), px('d')],
                    [px('e'), px(' '), px(' '), px(' ')],
                ]),
                Size(width=4, height=4): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' ')],
                    [px(' '), px(' '), px(' '), px(' ')],
                    [px('a'), px('b'), px('c'), px('d')],
                    [px('e'), px(' '), px(' '), px(' ')],
                ]),
                Size(width=4, height=6): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' ')],
                    [px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' ')],
                    [px('a'), px('b'), px('c'), px('d')],
                    [px('e'), px(' '), px(' '), px(' ')],
                ]),
                Size(width=5, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' '), px(' ')],
                    [px('a'), px('b'), px('c'), px('d'), px('e')],
                ]),
                Size(width=5, height=4): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px('a'), px('b'), px('c'), px('d'), px('e')],
                ]),
                Size(width=5, height=6): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' '), px(' '), px(' ')],
                    [px('a'), px('b'), px('c'), px('d'), px('e')],
                ]),
            }[size](),
            width_constraints_to_test=[0, 2, 4, 6],
            height_constraints_to_test=[0, 2, 4, 6]
        )

        self.assertEqual(
            (
                Label('1'),
                FlexibleSpace(),
                Label('2'),
            ),
            Column(
                Label('1'),
                FlexibleSpace(),
                Label('2'),
            ).subblocks
        )

    def test_row(self):
        # Case 1: An empty row:
        run_size_and_render_tests(
            self,
            Row(),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 2: A row containing a flexible block
        run_size_and_render_tests(
            self,
            Row(FlexibleSpace()),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 3: A row containing only an inflexible block
        label_1 = Label('123')
        run_size_and_render_tests(
            self,
            Row(label_1),
            expected_unconstrained_size=label_1.unconstrained_size,
            expected_size_given_width_constraint_only=lambda w: label_1.measure(width_constraint=w),
            expected_size_given_height_constraint_only=lambda h: label_1.measure(height_constraint=h),
            expected_size_given_both_constraints=lambda w, h: label_1.measure(width_constraint=w, height_constraint=h),
            expected_canvas=lambda size: label_1.render(granted_size=size)
        )

        # Case 4: A mix of flexible and inflexible blocks
        label_2 = Label('abcde')
        run_size_and_render_tests(
            self,
            Row(label_1, FlexibleSpace(), label_2),
            expected_unconstrained_size=Size(width=8, height=1),
            expected_size_given_width_constraint_only=lambda w: {
                0: lambda: Size.zero(),
                1: lambda: Size(width=1, height=3),
                2: lambda: Size(width=2, height=2),
                3: lambda: Size(width=3, height=1),
                4: lambda: Size(width=4, height=5),
                5: lambda: Size(width=5, height=3),
                6: lambda: Size(width=6, height=2),
                7: lambda: Size(width=7, height=2),
            }[w](),
            expected_size_given_height_constraint_only=lambda h: Size(
                width=8,
                height=1
            ) if h != 0 else Size.zero(),
            expected_size_given_both_constraints=lambda w, h: {
                Size(width=1, height=1): lambda: Size(width=1, height=1),
                Size(width=2, height=2): lambda: Size(width=2, height=2),
                Size(width=2, height=4): lambda: Size(width=2, height=2),
                Size(width=2, height=6): lambda: Size(width=2, height=2),
                Size(width=4, height=2): lambda: Size(width=4, height=2),
                Size(width=4, height=4): lambda: Size(width=4, height=4),
                Size(width=4, height=6): lambda: Size(width=4, height=5),
                Size(width=6, height=2): lambda: Size(width=6, height=2),
                Size(width=6, height=4): lambda: Size(width=6, height=2),
                Size(width=6, height=6): lambda: Size(width=6, height=2),
            }[Size(width=w, height=h)]() if w != 0 and h != 0 else Size.zero(),
            expected_canvas=lambda size: {
                Size.zero(): lambda: Canvas.empty(),
                Size(width=2, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                ]),
                Size(width=4, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('a')],
                    [px(' '), px(' '), px(' '), px('…')],
                ]),
                Size(width=4, height=4): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('a')],
                    [px(' '), px(' '), px(' '), px('b')],
                    [px(' '), px(' '), px(' '), px('c')],
                    [px(' '), px(' '), px(' '), px('…')],
                ]),
                Size(width=4, height=5): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('a')],
                    [px(' '), px(' '), px(' '), px('b')],
                    [px(' '), px(' '), px(' '), px('c')],
                    [px(' '), px(' '), px(' '), px('d')],
                    [px(' '), px(' '), px(' '), px('e')],
                ]),
                Size(width=6, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('a'), px('b'), px('c')],
                    [px(' '), px(' '), px(' '), px('d'), px('e'), px(' ')],
                ]),
                Size(width=8, height=1): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3'), px('a'), px('b'), px('c'), px('d'), px('e')],
                ]),
            }[size](),
            width_constraints_to_test=[0, 2, 4, 6],
            height_constraints_to_test=[0, 2, 4, 6]
        )

        self.assertEqual(
            (
                Label('1'),
                FlexibleSpace(),
                Label('2'),
            ),
            Row(
                Label('1'),
                FlexibleSpace(),
                Label('2'),
            ).subblocks
        )

    def test_horizontal_separator(self):
        run_size_and_render_tests(
            self,
            HorizontalSeparator(),
            expected_unconstrained_size=Size(width=3, height=1),
            expected_size_given_width_constraint_only=lambda w: Size(width=w, height=1) if w != 0 else Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size(width=3, height=1) if h != 0 else Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size(width=w, height=1) if w != 0 and h != 0 else Size.zero(),
            expected_canvas=lambda size: Canvas.from_pixels([[px('─')] * size.width]) if size.area != 0 else Canvas.empty()
        )

    def test_vertical_separator(self):
        run_size_and_render_tests(
            self,
            VerticalSeparator(),
            expected_unconstrained_size=Size(width=1, height=3),
            expected_size_given_width_constraint_only=lambda w: Size(width=1, height=3) if w != 0 else Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size(width=1, height=h) if h != 0 else Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size(width=1, height=h) if w != 0 and h != 0 else Size.zero(),
            expected_canvas=lambda size: Canvas.from_pixels([[px('│')]] * size.height) if size.area != 0 else Canvas.empty()
        )

    def test_mapped_blocks(self):
        label = Label('123')
        self.assertEqual(
            label.rendered(),
            MappedBlock(label, lambda _: _).rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.foreground(Color.GREEN)),
            label.foreground(Color.GREEN).rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.background(Color.GREEN)),
            label.background(Color.GREEN).rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.inverted()),
            label.inverted().rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.bold()),
            label.bold().rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.italic()),
            label.italic().rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.underlined()),
            label.underlined().rendered(),
        )
        self.assertEqual(
            label.rendered().map(lambda _: _.styled_string.blinking()),
            label.blinking().rendered(),
        )

        self.assertEqual(
            (label,),
            MappedBlock(label, lambda _: _).subblocks
        )

    def test_fixed_width_block(self):
        label = Label('123')
        block = label.resized(width=2)
        self.assertIsInstance(block, FixedWidthBlock)
        self.assertEqual((label,), block.subblocks)
        run_size_and_render_tests(
            self,
            block,
            expected_unconstrained_size=Size(width=2, height=2),
            expected_size_given_width_constraint_only=lambda w: Size(width=2, height=2),
            expected_size_given_height_constraint_only=lambda h: Size(width=2, height=min(h, 2)) if h != 0 else Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size(width=2, height=min(h, 2)) if h != 0 else Size.zero(),
            expected_canvas=lambda size: {
                Size.zero(): lambda: Canvas.empty(),
                Size(width=2, height=2): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                ]),
            }[size](),
            width_constraints_to_test=[0, 2, 4],
            height_constraints_to_test=[0, 2, 4],
        )

    def test_fixed_height_block(self):
        label = Label('123')
        block = label.resized(height=3)
        self.assertIsInstance(block, FixedHeightBlock)
        self.assertEqual((label,), block.subblocks)
        run_size_and_render_tests(
            self,
            block,
            expected_unconstrained_size=Size(width=3, height=3),
            expected_size_given_width_constraint_only=lambda w: Size(width=min(w, 3), height=3) if w != 0 else Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size(width=3, height=3),
            expected_size_given_both_constraints=lambda w, h: Size(width=min(w, 3), height=3) if w != 0 else Size.zero(),
            expected_canvas=lambda size: {
                Size.zero(): lambda: Canvas.empty(),
                Size(width=2, height=3): lambda: Canvas.from_pixels([
                    [px('1'), px('2')],
                    [px('3'), px(' ')],
                    [px(' '), px(' ')],
                ]),
                Size(width=3, height=3): lambda: Canvas.from_pixels([
                    [px('1'), px('2'), px('3')],
                    [px(' '), px(' '), px(' ')],
                    [px(' '), px(' '), px(' ')],
                ]),
            }[size](),
            width_constraints_to_test=[0, 2, 4],
            height_constraints_to_test=[0, 2, 4],
        )

    def test_fixed_size_block(self):
        label = Label('123')
        block = label.resized(width=2, height=3)
        self.assertIsInstance(block, FixedSizeBlock)
        self.assertEqual((label,), block.subblocks)
        run_size_and_render_tests(
            self,
            block,
            expected_unconstrained_size=Size(width=2, height=3),
            expected_size_given_width_constraint_only=lambda w: Size(width=2, height=3),
            expected_size_given_height_constraint_only=lambda h: Size(width=2, height=3),
            expected_size_given_both_constraints=lambda w, h: Size(width=2, height=3),
            expected_canvas=lambda size: Canvas.from_pixels([
                [px('1'), px('2')],
                [px('3'), px(' ')],
                [px(' '), px(' ')],
            ]),
            width_constraints_to_test=[0, 2, 4],
            height_constraints_to_test=[0, 2, 4],
        )

    def test_padding_methods(self):
        label = Label('123')

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=1,
                padding_right=1,
                padding_bottom=1,
                padding_left=1,
            ),
            label.padded()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=2,
                padding_right=2,
                padding_bottom=2,
                padding_left=2,
            ),
            label.padded(2)
        )

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=1,
                padding_bottom=0,
                padding_left=1,
            ),
            label.padded_horizontally()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=2,
                padding_bottom=0,
                padding_left=2,
            ),
            label.padded_horizontally(2)
        )

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=1,
                padding_right=0,
                padding_bottom=1,
                padding_left=0,
            ),
            label.padded_vertically()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=2,
                padding_right=0,
                padding_bottom=2,
                padding_left=0,
            ),
            label.padded_vertically(2)
        )

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=1,
                padding_right=0,
                padding_bottom=0,
                padding_left=0,
            ),
            label.padded_top()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=2,
                padding_right=0,
                padding_bottom=0,
                padding_left=0,
            ),
            label.padded_top(2)
        )

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=1,
                padding_bottom=0,
                padding_left=0,
            ),
            label.padded_right()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=2,
                padding_bottom=0,
                padding_left=0,
            ),
            label.padded_right(2)
        )

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=0,
                padding_bottom=1,
                padding_left=0,
            ),
            label.padded_bottom()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=0,
                padding_bottom=2,
                padding_left=0,
            ),
            label.padded_bottom(2)
        )

        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=0,
                padding_bottom=0,
                padding_left=1,
            ),
            label.padded_left()
        )
        self.assertEqual(
            PaddedBlock(
                original=label,
                padding_top=0,
                padding_right=0,
                padding_bottom=0,
                padding_left=2,
            ),
            label.padded_left(2)
        )

    def test_resized_method(self):
        block: Label = Label('123')

        # Case 1: No new width or height specified:
        self.assertIsInstance(block.resized(), Label)
        self.assertEqual(block, block.resized())

        # Case 2: Only width specified:
        self.assertIsInstance(block.resized(width=2), FixedWidthBlock)

        # Case 3: Only height specified:
        self.assertIsInstance(block.resized(height=3), FixedHeightBlock)

        # Case 4: Both width and height specified:
        self.assertIsInstance(block.resized(width=2, height=3), FixedSizeBlock)

    def test_string_representation(self):
        self.assertEqual(
            '┌───┐\n'
            '│123│\n'
            '└───┘',
            str(Label('123').framed())
        )
