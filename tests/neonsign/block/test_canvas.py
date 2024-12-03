from unittest import TestCase

from neonsign import s
from neonsign.block.canvas import (
    Canvas, CanvasAnchor, StyledStringPixel,
    TransparentPixel, px
)
from neonsign.core.size import Size


class TestCanvas(TestCase):

    def test_constructors(self):

        canvas_0: Canvas = Canvas.empty()
        self.assertEqual(Size.zero(), canvas_0.size)
        self.assertEqual((), canvas_0.pixels)

        canvas_1: Canvas = Canvas.of(
            size=Size(width=3, height=2),
            pixel_factory=lambda x, y: str(x + y * 3)
        )
        self.assertEqual(Size(width=3, height=2), canvas_1.size)
        self.assertEqual(
            (
                (px('0'), px('1'), px('2')),
                (px('3'), px('4'), px('5')),
            ),
            canvas_1.pixels
        )

        canvas_2: Canvas = Canvas.from_pixels(
            [
                [px('a'), px('b')],
                [px('c'), px('d')],
                [px('e'), px('f')],
            ]
        )
        self.assertEqual(Size(width=2, height=3), canvas_2.size)
        self.assertEqual(
            (
                (px('a'), px('b')),
                (px('c'), px('d')),
                (px('e'), px('f')),
            ),
            canvas_2.pixels
        )

    def test_pixel_construction(self):
        self.assertEqual(TransparentPixel(), px())
        self.assertEqual(StyledStringPixel(s('a')), px('a'))
        self.assertEqual(StyledStringPixel(s('a')), px(s('a')))
        self.assertEqual(TransparentPixel(), px(TransparentPixel()))
        self.assertEqual(
            StyledStringPixel(s('a')),
            px(StyledStringPixel(s('a')))
        )

    def test_retrieving_pixels(self):
        canvas = Canvas.from_pixels(
            pixels=[
                [px('0'), px('1'), px('2')],
                [px('3'), px('4'), px('5')],
            ]
        )
        self.assertEqual(px('0'), canvas.at(x=0, y=0))
        self.assertEqual(px('1'), canvas.at(x=1, y=0))
        self.assertEqual(px('2'), canvas.at(x=2, y=0))
        self.assertEqual(px('3'), canvas.at(x=0, y=1))
        self.assertEqual(px('4'), canvas.at(x=1, y=1))
        self.assertEqual(px('5'), canvas.at(x=2, y=1))

    def test_mapping(self):
        canvas = Canvas.from_pixels(
            pixels=[
                [px('a'), px('b'), px('c')],
                [px('d'), px('e'), px('f')],
            ]
        )
        mapped_canvas_1 = canvas.map(lambda p: p.styled_string.content.upper())
        self.assertEqual(canvas.size, mapped_canvas_1.size)
        self.assertEqual(
            (
                (px('A'), px('B'), px('C')),
                (px('D'), px('E'), px('F')),
            ),
            mapped_canvas_1.pixels
        )

        mapped_canvas_2 = canvas.map_with_index(
            lambda x, y, p: str(x + y * 3)
        )
        self.assertEqual(canvas.size, mapped_canvas_2.size)
        self.assertEqual(
            (
                (px('0'), px('1'), px('2')),
                (px('3'), px('4'), px('5')),
            ),
            mapped_canvas_2.pixels
        )

    def test_concatenation(self):
        canvas_1 = Canvas.from_pixels(
            pixels=[
                [px('0'), px('1'), px('2')],
                [px('3'), px('4'), px('5')],
            ]
        )
        canvas_2 = Canvas.from_pixels(
            pixels=[
                [px('a'), px('b'), px('c')],
                [px('d'), px('e'), px('f')],
            ]
        )
        canvas_3 = Canvas.from_pixels(
            pixels=[
                [px('A'), px('B')],
                [px('C'), px('D')],
                [px('D'), px('F')],
                [px('G'), px('H')],
            ]
        )

        canvas_4 = Canvas.concatenate_vertically(canvas_1, canvas_2)
        self.assertEqual(Size(width=3, height=4), canvas_4.size)
        self.assertEqual(
            (
                (px('0'), px('1'), px('2')),
                (px('3'), px('4'), px('5')),
                (px('a'), px('b'), px('c')),
                (px('d'), px('e'), px('f')),
            ),
            canvas_4.pixels
        )

        canvas_5 = Canvas.concatenate_horizontally(canvas_3, canvas_4)
        self.assertEqual(Size(width=5, height=4), canvas_5.size)
        self.assertEqual(
            (
                (px('A'), px('B'), px('0'), px('1'), px('2')),
                (px('C'), px('D'), px('3'), px('4'), px('5')),
                (px('D'), px('F'), px('a'), px('b'), px('c')),
                (px('G'), px('H'), px('d'), px('e'), px('f')),
            ),
            canvas_5.pixels
        )

        with self.assertRaises(Exception) as e:
            Canvas.concatenate_vertically(canvas_1, canvas_3)
        self.assertEqual(
            'The canvases being concatenated vertically do not have the same '
            'width!',
            str(e.exception)
        )

        with self.assertRaises(Exception) as e:
            Canvas.concatenate_horizontally(canvas_1, canvas_3)
        self.assertEqual(
            'The canvases being concatenated horizontally do not have the same '
            'height!',
            str(e.exception)
        )

        self.assertEqual(Canvas.empty(), Canvas.concatenate_horizontally())
        self.assertEqual(Canvas.empty(), Canvas.concatenate_vertically())

    def test_cropping(self):
        canvas = Canvas.from_pixels(
            pixels=[
                [px('A'), px('B'), px('C'), px('D'), px('E')],
                [px('F'), px('G'), px('H'), px('I'), px('J')],
                [px('K'), px('L'), px('M'), px('N'), px('O')],
                [px('P'), px('Q'), px('R'), px('S'), px('T')],
            ]
        )

        self.assertEqual(
            (
                (px('A'), px('B'), px('C'), px('D'), px('E')),
                (px('F'), px('G'), px('H'), px('I'), px('J')),
                (px('K'), px('L'), px('M'), px('N'), px('O')),
                (px('P'), px('Q'), px('R'), px('S'), px('T')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.TOP_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px('A'), px('B'), px('C')),
                (px('F'), px('G'), px('H')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.TOP_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px('B'), px('C'), px('D')),
                (px('G'), px('H'), px('I')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.TOP_MID
            ).pixels
        )

        self.assertEqual(
            (
                (px('C'), px('D'), px('E')),
                (px('H'), px('I'), px('J')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.TOP_RIGHT
            ).pixels
        )

        self.assertEqual(
            (
                (px('F'), px('G'), px('H')),
                (px('K'), px('L'), px('M')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.MID_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px('G'), px('H'), px('I')),
                (px('L'), px('M'), px('N')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.CENTER
            ).pixels
        )

        self.assertEqual(
            (
                (px('H'), px('I'), px('J')),
                (px('M'), px('N'), px('O')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.MID_RIGHT
            ).pixels
        )

        self.assertEqual(
            (
                (px('K'), px('L'), px('M')),
                (px('P'), px('Q'), px('R')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.BOTTOM_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px('L'), px('M'), px('N')),
                (px('Q'), px('R'), px('S')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.BOTTOM_MID
            ).pixels
        )

        self.assertEqual(
            (
                (px('M'), px('N'), px('O')),
                (px('R'), px('S'), px('T')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=3, height=2),
                anchor=CanvasAnchor.BOTTOM_RIGHT
            ).pixels
        )

    def test_padding(self):
        canvas = Canvas.from_pixels(
            pixels=[
                [px('A'), px('B'), px('C'), ],
                [px('D'), px('E'), px('F'), ],
            ]
        )

        self.assertEqual(
            (
                (px('A'), px('B'), px('C'), px(), px()),
                (px('D'), px('E'), px('F'), px(), px()),
                (px(), px(), px(), px(), px()),
                (px(), px(), px(), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.TOP_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px('A'), px('B'), px('C'), px()),
                (px(), px('D'), px('E'), px('F'), px()),
                (px(), px(), px(), px(), px()),
                (px(), px(), px(), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.TOP_MID
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px('A'), px('B'), px('C')),
                (px(), px(), px('D'), px('E'), px('F')),
                (px(), px(), px(), px(), px()),
                (px(), px(), px(), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.TOP_RIGHT
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px(), px(), px()),
                (px('A'), px('B'), px('C'), px(), px()),
                (px('D'), px('E'), px('F'), px(), px()),
                (px(), px(), px(), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.MID_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px(), px(), px()),
                (px(), px('A'), px('B'), px('C'), px()),
                (px(), px('D'), px('E'), px('F'), px()),
                (px(), px(), px(), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.CENTER
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px(), px(), px()),
                (px(), px(), px('A'), px('B'), px('C')),
                (px(), px(), px('D'), px('E'), px('F')),
                (px(), px(), px(), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.MID_RIGHT
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px(), px(), px()),
                (px(), px(), px(), px(), px()),
                (px('A'), px('B'), px('C'), px(), px()),
                (px('D'), px('E'), px('F'), px(), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.BOTTOM_LEFT
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px(), px(), px()),
                (px(), px(), px(), px(), px()),
                (px(), px('A'), px('B'), px('C'), px()),
                (px(), px('D'), px('E'), px('F'), px()),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.BOTTOM_MID
            ).pixels
        )

        self.assertEqual(
            (
                (px(), px(), px(), px(), px()),
                (px(), px(), px(), px(), px()),
                (px(), px(), px('A'), px('B'), px('C')),
                (px(), px(), px('D'), px('E'), px('F')),
            ),
            canvas.crop_or_pad_to(
                new_size=Size(width=5, height=4),
                anchor=CanvasAnchor.BOTTOM_RIGHT
            ).pixels
        )


    def test_string_representation(self):
        self.assertEqual(
            '012\n345',
            str(
                Canvas.of(
                    size=Size(width=3, height=2),
                    pixel_factory=lambda x, y: str(x + y * 3)
                )
            )
        )
