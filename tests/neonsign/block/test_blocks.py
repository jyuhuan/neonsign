import sys
from typing import Callable, List, Optional, Set
from unittest import TestCase

from neonsign import (
    Block, Color, Column, FixedHeightBlock, FixedSizeBlock, FixedWidthBlock,
    FrameStyle, HorizontalSeparator, Label, PaddedBlock, Row, FlexibleSpace,
    VerticalSeparator, s
)
from neonsign.block.impl.framed import _Frame
from neonsign.block.canvas import Canvas, px
from neonsign.block.impl.text_effects import MappedBlock
from neonsign.core.size import Size

MAX = sys.maxsize
"""An alias for ``sys.maxsize`` to keep test code short."""


DEFAULT_TEST_CONSTRAINTS: List[int] = list(range(0, 30, 2)) + [MAX]


class TestBlocks(TestCase):

    def test_label(self):

        self.run_size_and_render_tests(
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

        self.run_size_and_render_tests(
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

        self.run_size_and_render_tests(
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

        self.run_size_and_render_tests(
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

        self.run_size_and_render_tests(
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
        self.run_size_and_render_tests(
            Column(),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 2: A column containing a flexible block
        self.run_size_and_render_tests(
            Column(FlexibleSpace()),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 3: A column containing only an inflexible block
        label_1 = Label('123')
        self.run_size_and_render_tests(
            Column(label_1),
            expected_unconstrained_size=label_1.unconstrained_size,
            expected_size_given_width_constraint_only=lambda w: label_1.measure(width_constraint=w),
            expected_size_given_height_constraint_only=lambda h: label_1.measure(height_constraint=h),
            expected_size_given_both_constraints=lambda w, h: label_1.measure(width_constraint=w, height_constraint=h),
            expected_canvas=lambda size: label_1.render(granted_size=size)
        )

        # Case 4: A mix of flexible and inflexible blocks
        label_2 = Label('abcde')
        self.run_size_and_render_tests(
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
        self.run_size_and_render_tests(
            Row(),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 2: A row containing a flexible block
        self.run_size_and_render_tests(
            Row(FlexibleSpace()),
            expected_unconstrained_size=Size.zero(),
            expected_size_given_width_constraint_only=lambda w: Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size.zero(),
            expected_canvas=lambda size: Canvas.empty()
        )

        # Case 3: A row containing only an inflexible block
        label_1 = Label('123')
        self.run_size_and_render_tests(
            Row(label_1),
            expected_unconstrained_size=label_1.unconstrained_size,
            expected_size_given_width_constraint_only=lambda w: label_1.measure(width_constraint=w),
            expected_size_given_height_constraint_only=lambda h: label_1.measure(height_constraint=h),
            expected_size_given_both_constraints=lambda w, h: label_1.measure(width_constraint=w, height_constraint=h),
            expected_canvas=lambda size: label_1.render(granted_size=size)
        )

        # Case 4: A mix of flexible and inflexible blocks
        label_2 = Label('abcde')
        self.run_size_and_render_tests(
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
        self.run_size_and_render_tests(
            HorizontalSeparator(),
            expected_unconstrained_size=Size(width=3, height=1),
            expected_size_given_width_constraint_only=lambda w: Size(width=w, height=1) if w != 0 else Size.zero(),
            expected_size_given_height_constraint_only=lambda h: Size(width=3, height=1) if h != 0 else Size.zero(),
            expected_size_given_both_constraints=lambda w, h: Size(width=w, height=1) if w != 0 and h != 0 else Size.zero(),
            expected_canvas=lambda size: Canvas.from_pixels([[px('─')] * size.width]) if size.area != 0 else Canvas.empty()
        )

    def test_vertical_separator(self):
        self.run_size_and_render_tests(
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
        self.run_size_and_render_tests(
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
        self.run_size_and_render_tests(
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
        self.run_size_and_render_tests(
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

    #
    # Utilities:
    #

    def run_size_and_render_tests(
            self,
            block: Block,
            expected_unconstrained_size: Size,
            expected_size_given_width_constraint_only: Callable[[int], Size],
            expected_size_given_height_constraint_only: Callable[[int], Size],
            expected_size_given_both_constraints: Callable[[int, int], Size],
            expected_canvas: Callable[[Size], Canvas],
            width_constraints_to_test: Optional[List[int]] = None,
            height_constraints_to_test: Optional[List[int]] = None,
    ):
        if width_constraints_to_test is None:
            width_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
        if height_constraints_to_test is None:
            height_constraints_to_test = DEFAULT_TEST_CONSTRAINTS

        observed_sizes = (
            {self.run_unconstrained_size_test(
                block,
                expected_unconstrained_size
            )}
            | self.run_horizontal_squeeze_test(
                block,
                expected_size_given_width_constraint_only,
                width_constraints_to_test=width_constraints_to_test
            )
            | self.run_vertical_squeeze_test(
                block,
                expected_size_given_height_constraint_only,
                height_constraints_to_test=height_constraints_to_test
            )
            | self.run_both_directions_squeeze_test(
                block,
                expected_size_given_both_constraints,
                width_constraints_to_test=width_constraints_to_test,
                height_constraints_to_test=height_constraints_to_test
            )
        )

        self.run_render_test(
            block,
            {_ for _ in observed_sizes if _.width < 1000 and _.height < 1000},
            expected_canvas
        )

    def run_unconstrained_size_test(
            self,
            block: Block,
            expected_unconstrained_size: Size
    ) -> Size:
        observed_size = expected_unconstrained_size
        self.assertEqual(
            observed_size,
            block.unconstrained_size
        )
        return observed_size

    def run_horizontal_squeeze_test(
            self,
            block: Block,
            expected_size_given_width_constraint_only: Callable[[int], Size],
            width_constraints_to_test: Optional[List[int]] = None,
    ) -> Set[Size]:
        if width_constraints_to_test is None:
            width_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
        observed_sizes: Set[Size] = set()
        for width_constraint in width_constraints_to_test:
            observed_size = block.measure(
                width_constraint=width_constraint
            )
            self.assertEqual(
                expected_size_given_width_constraint_only(width_constraint),
                observed_size
            )
            if observed_size < Size(width=100, height=100):
                observed_sizes.add(observed_size)
        return observed_sizes

    def run_vertical_squeeze_test(
            self,
            block: Block,
            expected_size_given_height_constraint_only: Callable[[int], Size],
            height_constraints_to_test: Optional[List[int]] = None,
    ) -> Set[Size]:
        if height_constraints_to_test is None:
            height_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
        observed_sizes: Set[Size] = set()
        for height_constraint in height_constraints_to_test:
            observed_size: Size = block.measure(
                height_constraint=height_constraint
            )
            self.assertEqual(
                expected_size_given_height_constraint_only(height_constraint),
                observed_size
            )
            if observed_size < Size(width=100, height=100):
                observed_sizes.add(observed_size)
        return observed_sizes

    def run_both_directions_squeeze_test(
            self,
            block: Block,
            expected_size_given_both_constraints: Callable[[int, int], Size],
            width_constraints_to_test: Optional[List[int]] = None,
            height_constraints_to_test: Optional[List[int]] = None,
    ) -> Set[Size]:
        if width_constraints_to_test is None:
            width_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
        if height_constraints_to_test is None:
            height_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
        observed_sizes: Set[Size] = set()
        for height_constraint in height_constraints_to_test:
            for width_constraint in width_constraints_to_test:
                observed_size = block.measure(
                    width_constraint=width_constraint,
                    height_constraint=height_constraint
                )
                self.assertEqual(
                    expected_size_given_both_constraints(
                        width_constraint,
                        height_constraint
                    ),
                    observed_size
                )
                if observed_size < Size(width=100, height=100):
                    observed_sizes.add(observed_size)
        return observed_sizes

    def run_render_test(
            self,
            block: Block,
            sizes: Set[Size],
            expected_canvas_at_sizes: Callable[[Size], Canvas]
    ):
        for size in sizes:
            self.assertEqual(
                expected_canvas_at_sizes(size),
                block.render(granted_size=size)
            )
