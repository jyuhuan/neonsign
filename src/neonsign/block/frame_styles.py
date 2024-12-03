from __future__ import annotations

from typing import final


@final
class FrameStyle:
    """The set of characters to use for building the frame surrounding a framed
    text block."""

    def __init__(
            self,
            top_left: str,
            top_mid: str,
            top_right: str,
            left_mid: str,
            center: str,
            right_mid: str,
            bottom_left: str,
            bottom_mid: str,
            bottom_right: str,
            horizontal_line: str,
            vertical_line: str,
    ):
        self.top_left = top_left
        self.top_mid = top_mid
        self.top_right = top_right
        self.left_mid = left_mid
        self.center = center
        self.right_mid = right_mid
        self.bottom_left = bottom_left
        self.bottom_mid = bottom_mid
        self.bottom_right = bottom_right
        self.horizontal_line = horizontal_line
        self.vertical_line = vertical_line

    REGULAR: FrameStyle
    ROUNDED: FrameStyle
    BOLD: FrameStyle
    DOUBLE: FrameStyle


FrameStyle.REGULAR = FrameStyle(
    top_left='┌',
    top_mid='┬',
    top_right='┐',
    left_mid='├',
    center='┼',
    right_mid='┤',
    bottom_left='└',
    bottom_mid='┴',
    bottom_right='┘',
    horizontal_line='─',
    vertical_line='│',
)

FrameStyle.BOLD = FrameStyle(
    top_left='┏',
    top_mid='┳',
    top_right='┓',
    left_mid='┣',
    center='╋',
    right_mid='┫',
    bottom_left='┗',
    bottom_mid='┻',
    bottom_right='┛',
    horizontal_line='━',
    vertical_line='┃',
)

FrameStyle.DOUBLE = FrameStyle(
    top_left='╔',
    top_mid='╦',
    top_right='╗',
    left_mid='╠',
    center='╬',
    right_mid='╣',
    bottom_left='╚',
    bottom_mid='╩',
    bottom_right='╝',
    horizontal_line='═',
    vertical_line='║',
)

FrameStyle.ROUNDED = FrameStyle(
    top_left='╭',
    top_mid='┬',
    top_right='╮',
    left_mid='├',
    center='┼',
    right_mid='┤',
    bottom_left='╰',
    bottom_mid='┴',
    bottom_right='╯',
    horizontal_line='─',
    vertical_line='│',
)
