from unittest import TestCase

from neonsign import FrameStyle


class TestFrameStyles(TestCase):

    def test(self):
        self._check_correctness(
            FrameStyle.REGULAR,
            '┌─┬─┐\n'
            '│ │ │\n'
            '├─┼─┤\n'
            '│ │ │\n'
            '└─┴─┘'
        )
        self._check_correctness(
            FrameStyle.BOLD,
            '┏━┳━┓\n'
            '┃ ┃ ┃\n'
            '┣━╋━┫\n'
            '┃ ┃ ┃\n'
            '┗━┻━┛'
        )
        self._check_correctness(
            FrameStyle.DOUBLE,
            '╔═╦═╗\n'
            '║ ║ ║\n'
            '╠═╬═╣\n'
            '║ ║ ║\n'
            '╚═╩═╝'
        )
        self._check_correctness(
            FrameStyle.ROUNDED,
            '╭─┬─╮\n'
            '│ │ │\n'
            '├─┼─┤\n'
            '│ │ │\n'
            '╰─┴─╯'
        )

    def _check_correctness(
            self,
            style: FrameStyle,
            expected
    ):
        self.assertEqual(
            expected,
            '\n'.join([
                ''.join([
                    style.top_left,
                    style.horizontal_line,
                    style.top_mid,
                    style.horizontal_line,
                    style.top_right,
                ]),
                ''.join([
                    style.vertical_line,
                    ' ',
                    style.vertical_line,
                    ' ',
                    style.vertical_line,
                ]),
                ''.join([

                    style.left_mid,
                    style.horizontal_line,
                    style.center,
                    style.horizontal_line,
                    style.right_mid,
                ]),
                ''.join([
                    style.vertical_line,
                    ' ',
                    style.vertical_line,
                    ' ',
                    style.vertical_line,
                ]),
                ''.join([
                    style.bottom_left,
                    style.horizontal_line,
                    style.bottom_mid,
                    style.horizontal_line,
                    style.bottom_right
                ])
            ])
        )

