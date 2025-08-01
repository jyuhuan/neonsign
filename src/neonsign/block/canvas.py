from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Any, Callable, List, Tuple, Union, final

from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size
from neonsign.string.styled_string import StyledString
from neonsign.string.syntax import s


class CanvasAnchor(Enum):
    TOP_LEFT = 'top_left'
    TOP_MID = 'top_mid'
    TOP_RIGHT = 'top_right'
    MID_LEFT = 'left_mid'
    CENTER = 'center'
    MID_RIGHT = 'right_mid'
    BOTTOM_LEFT = 'bottom_left'
    BOTTOM_MID = 'bottom_mid'
    BOTTOM_RIGHT = 'bottom_right'


class Pixel(ABC):

    @property
    @abstractmethod
    def rendered(self) -> str:
        pass

    def __str__(self) -> str:
        return self.rendered


PixelSource = Union[Pixel, StyledString, str, None]
"""A union of types that can be converted to Pixel."""


def construct_pixel(obj: PixelSource = None) -> Pixel:
    if obj is None:
        return TransparentPixel()
    elif isinstance(obj, Pixel):
        return obj
    elif isinstance(obj, StyledString):
        return StyledStringPixel(obj)
    elif isinstance(obj, str):
        return StyledStringPixel(s(obj))
    else:
        raise TypeError(f'Pixel type {type(obj)} is not supported!')


def px(obj: PixelSource = None) -> Pixel:
    """A shorthand for construct_pixel."""
    return construct_pixel(obj)


@dataclass
class StyledStringPixel(Pixel):
    styled_string: StyledString

    def __post_init__(self):
        if len(self.styled_string.content) != 1:
            raise Exception(
                f'Only a StyledString with exactly 1 character can be used as '
                f'a pixel, but {len(self.styled_string.content)} were provided!'
            )

    @property
    def rendered(self) -> str:
        return str(self.styled_string)



class TransparentPixel(Pixel):
    @property
    def rendered(self) -> str:
        return ' '

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TransparentPixel)

    def __hash__(self) -> int:
        return hash(' ')


@final
@dataclass(frozen=True)
class Canvas:
    pixels: Tuple[Tuple[Pixel, ...], ...]

    @property
    def size(self) -> Size:
        if len(self.pixels) == 0:
            return Size(width=0, height=0)
        else:
            return Size(width=len(self.pixels[0]), height=len(self.pixels))

    def at(self, x: int, y: int) -> Pixel:
        return self.pixels[y][x]

    def map(self, f: Callable[[Pixel], PixelSource]) -> Canvas:
        return Canvas(
            pixels=tuple(
                tuple(
                    px(f(pixel))
                    for pixel in row
                )
                for row in self.pixels
            )
        )

    def map_with_index(
            self,
            f: Callable[[int, int, Pixel], PixelSource]
    ) -> Canvas:
        return Canvas(
            pixels=tuple(
                tuple(
                    px(f(x, y, self.at(x=x, y=y)))
                    for x in range(0, self.size.width)
                )
                for y in range(0, self.size.height)
            )
        )

    def crop_or_pad_to(
            self,
            new_size: Size,
            anchor: CanvasAnchor = CanvasAnchor.TOP_LEFT,
            filler: Callable[[], PixelSource] = lambda: TransparentPixel()
    ) -> Canvas:
        if new_size == self.size:
            return self

        x_left = lambda: 0
        x_mid = lambda: new_size.width // 2 - self.size.width // 2
        x_right = lambda: new_size.width - self.size.width

        y_top = lambda: 0
        y_mid = lambda: new_size.height // 2 - self.size.height // 2
        y_bottom = lambda: new_size.height - self.size.height

        content_top_left_in_new_canvas: Point = {
            CanvasAnchor.TOP_LEFT: lambda: Point(x=x_left(), y=y_top()),
            CanvasAnchor.TOP_MID: lambda: Point(x=x_mid(), y=y_top()),
            CanvasAnchor.TOP_RIGHT: lambda: Point(x=x_right(), y=y_top()),
            CanvasAnchor.MID_LEFT: lambda: Point(x=x_left(), y=y_mid()),
            CanvasAnchor.CENTER: lambda: Point(x=x_mid(), y=y_mid()),
            CanvasAnchor.MID_RIGHT: lambda: Point(x=x_right(), y=y_mid()),
            CanvasAnchor.BOTTOM_LEFT: lambda: Point(x=x_left(), y=y_bottom()),
            CanvasAnchor.BOTTOM_MID: lambda: Point(x=x_mid(), y=y_bottom()),
            CanvasAnchor.BOTTOM_RIGHT: lambda: Point(x=x_right(), y=y_bottom())
        }[anchor]()

        def pixel_factory(x: int, y: int) -> Pixel:
            if (
                content_top_left_in_new_canvas.x <= x <
                    content_top_left_in_new_canvas.x + self.size.width and
                content_top_left_in_new_canvas.y <= y <
                    content_top_left_in_new_canvas.y + self.size.height
            ):
                return self.at(
                    x=x - content_top_left_in_new_canvas.x,
                    y=y - content_top_left_in_new_canvas.y
                )
            else:
                return px(filler())
        return Canvas.of(new_size, pixel_factory)

    def crop_or_pad_to_rect(
            self,
            rect: Rect,
            filler: Callable[[], PixelSource] = lambda: TransparentPixel()
    ) -> Canvas:
        def pixel_factory(x: int, y: int) -> Pixel:
            if (
                    0 <= x + rect.top_left.x < self.size.width and
                    0 <= y + rect.top_left.y < self.size.height
            ):
                return self.at(x=x + rect.top_left.x, y=y + rect.top_left.y)
            else:
                return px(filler())
        return Canvas.of(rect.size, pixel_factory)

    def replace(self, start: Point, size: Size, new_canvas: Canvas) -> Canvas:
        def pixel_factory(x: int, y: int) -> Pixel:
            if (
                start.x <= x < min(self.size.width, start.x + size.width) and
                start.y <= y < min(self.size.height, start.y + size.height)
            ):
                new_pixel = new_canvas.at(x=x - start.x, y=y - start.y)
                if isinstance(new_pixel, TransparentPixel):
                    return self.at(x=x, y=y)
                else:
                    return new_pixel
            else:
                return self.at(x=x, y=y)
        return Canvas.of(self.size, pixel_factory)

    @classmethod
    def concatenate_horizontally(cls, *canvases: Canvas) -> Canvas:
        if len(canvases) == 0:
            return Canvas.empty()
        if len(set(_.size.height for _ in canvases)) != 1:
            raise Exception(
                f'The canvases being concatenated horizontally do not have the '
                f'same height!'
            )
        height = canvases[0].size.height
        pixels = [[] for _ in range(0, height)]
        for canvas in canvases:
            for y in range(0, height):
                for x in range(0, canvas.size.width):
                    pixels[y].append(canvas.at(x=x, y=y))
        return Canvas.from_pixels(pixels)

    @classmethod
    def concatenate_vertically(cls, *canvases: Canvas) -> Canvas:
        if len(canvases) == 0:
            return Canvas.empty()
        if len(set(_.size.width for _ in canvases)) != 1:
            raise Exception(
                f'The canvases being concatenated vertically do not have the '
                f'same width!'
            )
        return Canvas(
            pixels=reduce(
                lambda x, y: x + y,
                [_.pixels for _ in canvases],
                ()
            )
        )

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                pixel.rendered if pixel is not None else ' '
                for pixel in row
            )
            for row in self.pixels
        )

    @classmethod
    def of(
            cls,
            size: Size,
            pixel_factory: Callable[[int, int], PixelSource] = lambda x, y: px()
    ) -> Canvas:
        return Canvas(
            pixels=tuple(
                tuple(
                    px(pixel_factory(x, y))
                    for x in range(0, size.width)
                )
                for y in range(0, size.height)
            )
        )

    @classmethod
    def from_pixels(cls, pixels: List[List[Pixel]]) -> Canvas:
        return Canvas(pixels=tuple(tuple(l) for l in pixels))

    @classmethod
    def empty(cls) -> Canvas:
        return Canvas(pixels=())
