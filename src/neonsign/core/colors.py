from __future__ import annotations

import colorsys
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Set, Tuple, final

_ALLOWED_SIMPLE_COLOR_NAMES: Set[str] = {
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'bright-black',
    'bright-red',
    'bright-green',
    'bright-yellow',
    'bright-blue',
    'bright-magenta',
    'bright-cyan',
    'bright-white',
}


class Color(ABC):
    """A class that represents a color.

    Overview
    --------

    Anywhere NeonSign expects you to specify a color, you should provide an
    instance of ``Color``.

    Obtaining an instance
    ---------------------

    Use the class methods and constants on this class to obtain an instance. Do
    not call the initializer of any concrete color class directly.

    Examples:

     - ``Color.GREEN`` obtains the color green.
       The exact color value depends on the terminal and its configuration.

     - ``Color.color8(1)`` obtains the 8-bit color at index 1.

     - ``Color.rgb(255, 10, 20)`` obtains the 24-bit color, (255, 10, 20).

    """

    BLACK: Color
    """The black color configured in the terminal."""

    RED: Color
    """The red color configured in the terminal."""

    GREEN: Color
    """The green color configured in the terminal."""

    YELLOW: Color
    """The yellow color configured in the terminal."""

    BLUE: Color
    """The blue color configured in the terminal."""

    MAGENTA: Color
    """The magenta color configured in the terminal."""

    CYAN: Color
    """The cyan color configured in the terminal."""

    WHITE: Color
    """The white color configured in the terminal."""

    BRIGHT_BLACK: Color
    """The bright version of the black color configured in the terminal."""

    BRIGHT_RED: Color
    """The bright version of the red color configured in the terminal."""

    BRIGHT_GREEN: Color
    """The bright version of the green color configured in the terminal."""

    BRIGHT_YELLOW: Color
    """The bright version of the yellow color configured in the terminal."""

    BRIGHT_BLUE: Color
    """The bright version of the blue color configured in the terminal."""

    BRIGHT_MAGENTA: Color
    """The bright version of the magenta color configured in the terminal."""

    BRIGHT_CYAN: Color
    """The bright version of the cyan color configured in the terminal."""

    BRIGHT_WHITE: Color
    """The bright version of the white color configured in the terminal."""

    @classmethod
    def rgb(cls, red: int, green: int, blue: int) -> Color:
        """Obtains the 24-bit color with the specified red, green and blue
        components.

        Args:
            red: The red component. Must be between 0 and 255.
            green: The green component. Must be between 0 and 255.
            blue: The blue component. Must be between 0 and 255.

        Returns:
            The 24-bit color with the specified components.

        Raises:
            ValueError: when the red, green or blue value is not between 0 and
                255.
        """
        return Color24(red, green, blue)

    @classmethod
    def hex(cls, hex_string: str) -> Color:
        """Obtains the 24-bit color with the specified hexadecimal value.

        Args:
            hex_string: A string that starts with the # sign, followed by the
                hexadecimal value of the color. For example: '#FF0000' for red.

        Returns:
            The 24-bit color with the specified hexadecimal value.

        Raises:
            ValueError: when the hex string is not valid.
        """
        return Color24.from_hex(hex_string)

    @classmethod
    def hsl(cls, hue: int, saturation: int, lightness: int) -> Color:
        """Obtains the 24-bit color with the specified hue, saturation and
        lightness using the HSL color model.

        Args:
            hue: The hue value.
                Must be between 0 and 360, inclusive.
            saturation: The saturation value.
                Must be between 0 and 100, inclusive.
            lightness: The lightness value.
                Must be between 0 and 100, inclusive.

        Returns:
            The 24-bit color with the specified components.

        Raises:
            ValueError: when the hue, saturation or lightness value is not
                within its valid range.
        """
        return Color24.from_hsl(
            hue=hue,
            saturation=saturation,
            lightness=lightness
        )

    @classmethod
    def hsv(cls, hue: int, saturation: int, value: int) -> Color:
        """Obtains the 24-bit color with the specified hue, saturation and
        value using the HSV color model.

        Args:
            hue: The hue value.
                Must be between 0 and 360, inclusive.
            saturation: The saturation value.
                Must be between 0 and 100, inclusive.
            value: The value.
                Must be between 0 and 100, inclusive.

        Returns:
            The 24-bit color with the specified components.

        Raises:
            ValueError: when the hue, saturation or value is not within its
                valid range.
        """
        return Color24.from_hsv(
            hue=hue,
            saturation=saturation,
            value=value
        )


    @classmethod
    def color8(cls, index: int) -> Color:
        """Obtains the 8-bit color at the index specified.

        Args:
            index: The index of the 8-bit color. There are in total 256 8-bit
                colors. A valid index is between 0 and 255, inclusive.

        Returns:
            The 8-bit color at the specified index.

        Raises:
            ValueError: when the index is not between 0 and 255.
        """
        return Color8(index)


@final
@dataclass(frozen=True)
class SimpleColor(Color):
    """
    A color identified by a simple name.

    Do not create an instance directly. Use the constants in :class:`Colors`.
    For example, :attr:`Color.GREEN`.
    """

    name: str
    """The unique name of the color."""

    def __post_init__(self):
        if self.name not in _ALLOWED_SIMPLE_COLOR_NAMES:
            raise ValueError(f'Cannot create color with name "{self.name}"!')


@final
@dataclass(frozen=True)
class Color8(Color):
    """An 8-bit color.

    Do not create an instance directly. Use :func:`Color.color8`.
    """

    index: int
    """The zero-based index of one of the 8-bit terminal colors.
    
    There are in total 256 8-bit colors. A valid index is between 0 and 255, 
    inclusive.
    """

    def __post_init__(self):
        if not 0 <= self.index <= 255:
            raise ValueError(
                f'Index for an 8-bit color must be within 0 and 255, '
                f'not {self.index}!'
            )


@final
@dataclass(frozen=True)
class Color24(Color):
    """A 24-bit color.

    Do not create an instance directly. Use :func:`Color.rgb`.
    """

    red: int
    """The red component of the color. Must be between 0 and 255."""

    green: int
    """The green component of the color. Must be between 0 and 255."""

    blue: int
    """The blue component of the color. Must be between 0 and 255."""

    def __post_init__(self):
        _require_values_to_be_in_range(
            values_by_name={
                'red': self.red,
                'green': self.green,
                'blue': self.blue,
            },
            required_ranges_by_name={
                name: (0, 255)
                for name in ('red', 'green', 'blue')
            }
        )

    @classmethod
    def from_hex(cls, hex_string: str) -> Color24:
        """Creates a 24-bit color with the specified hexadecimal value.

        Args:
            hex_string: A string that starts with the # sign, followed by the
                hexadecimal value of the color. For example: '#FF0000' for red.

        Returns:
            The 24-bit color with the specified hexadecimal value.

        Raises:
            ValueError: when the hex string is not valid.
        """

        if not hex_string.startswith('#'):
            raise ValueError(
                f"A color in hexadecimal format should start with the # sign, "
                f"but '{hex_string}' does not!"
            )
        hex_value = hex_string[1:]
        if len(hex_value) == 3:
            expanded_hex_value = ''.join(c * 2 for c in hex_value)
        elif len(hex_value) == 6:
            expanded_hex_value = hex_value
        else:
            raise ValueError(
                f"A hex code for 24-bit color must be 3-character or "
                f"6-character long, excluding the # sign at the beginning, but "
                f"'{hex_value}' is {len(hex_value)}-character long!"
            )
        return Color24(
            red=int(expanded_hex_value[0:2], base=16),
            green=int(expanded_hex_value[2:4], base=16),
            blue=int(expanded_hex_value[4:6], base=16)
        )

    @classmethod
    def from_hsl(cls, hue: int, saturation: int, lightness: int) -> Color24:
        """Creates a 24-bit color with the specified hue, saturation and
        lightness using the HSL color model.

        Args:
            hue: The hue value.
                Must be between 0 and 360, inclusive.
            saturation: The saturation value.
                Must be between 0 and 100, inclusive.
            lightness: The lightness value.
                Must be between 0 and 100, inclusive.

        Returns:
            The 24-bit color with the specified components.

        Raises:
            ValueError: when the hue, saturation or lightness value is not
                within its valid range.
        """
        _require_values_to_be_in_range(
            values_by_name={
                'hue': hue,
                'saturation': saturation,
                'lightness': lightness
            },
            required_ranges_by_name={
                'hue': (0, 360),
                'saturation': (0, 100),
                'lightness': (0, 100)
            },
        )
        (red, green, blue) = colorsys.hls_to_rgb(
            h=1.0 * hue / 360.0,
            l=1.0 * lightness / 100.0,
            s=1.0 * saturation / 100.0
        )
        return Color24(
            red=round(red * 255),
            green=round(green * 255),
            blue=round(blue * 255)
        )

    @classmethod
    def from_hsv(cls, hue: int, saturation: int, value: int) -> Color24:
        """Obtains a 24-bit color with the specified hue, saturation and value
        using the HSV color model.

        Args:
            hue: The hue value.
                Must be between 0 and 360, inclusive.
            saturation: The saturation value.
                Must be between 0 and 100, inclusive.
            value: The value.
                Must be between 0 and 100, inclusive.

        Returns:
            The 24-bit color with the specified components.

        Raises:
            ValueError: when the hue, saturation or value is not within its
                valid range.
        """
        _require_values_to_be_in_range(
            values_by_name={
                'hue': hue,
                'saturation': saturation,
                'value': value
            },
            required_ranges_by_name={
                'hue': (0, 360),
                'saturation': (0, 100),
                'value': (0, 100)
            },
        )
        (red, green, blue) = colorsys.hsv_to_rgb(
            h=1.0 * hue / 360,
            s=1.0 * saturation / 100.0,
            v=1.0 * value / 100.0
        )
        return Color24(
            red=round(red * 255),
            green=round(green * 255),
            blue=round(blue * 255)
        )


def _require_values_to_be_in_range(
        values_by_name: Dict[str, int],
        required_ranges_by_name: Dict[str, Tuple[int, int]],
):
    names_of_invalid_values: Set[str] = {
        name
        for (name, (min_value, max_value)) in required_ranges_by_name.items()
        if not min_value <= values_by_name[name] <= max_value
    }
    if len(names_of_invalid_values) > 0:
        summary = '\n'.join(
            f' - {name} = {values_by_name[name]} (required to be within '
            f'{required_ranges_by_name[name]})'
            for name in sorted(names_of_invalid_values)
        )
        raise ValueError(
            f'The following values are out of their required ranges:\n{summary}'
        )



Color.BLACK = SimpleColor('black')
Color.RED = SimpleColor('red')
Color.GREEN = SimpleColor('green')
Color.YELLOW = SimpleColor('yellow')
Color.BLUE = SimpleColor('blue')
Color.MAGENTA = SimpleColor('magenta')
Color.CYAN = SimpleColor('cyan')
Color.WHITE = SimpleColor('white')
Color.BRIGHT_BLACK = SimpleColor('bright-black')
Color.BRIGHT_RED = SimpleColor('bright-red')
Color.BRIGHT_GREEN = SimpleColor('bright-green')
Color.BRIGHT_YELLOW = SimpleColor('bright-yellow')
Color.BRIGHT_BLUE = SimpleColor('bright-blue')
Color.BRIGHT_MAGENTA = SimpleColor('bright-magenta')
Color.BRIGHT_CYAN = SimpleColor('bright-cyan')
Color.BRIGHT_WHITE = SimpleColor('bright-white')
