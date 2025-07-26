from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain
from typing import Tuple, final

from neonsign.core.color_commands import (
    command_for_background, command_for_foreground
)
from neonsign.core.colors import Color
from neonsign.core.style_command import StyleCommand


class StyledString(ABC):
    """A class that represents a string with visual styles.

    Overview
    --------

    This abstract base class provides methods with default implementations
    called *styling methods*, such as :func:`bold`, and :func:`background`. To
    use them, wrap your Python string with the :func:`~neonsign.s` function,
    followed by calls to one or more styling methods::

        s('example').bold().background(Color.GREEN)

    See :doc:`/articles/tutorial` to learn more.


    Printing a styled string
    ------------------------

    To print a styled string to the terminal, simply pass it to Python's
    ``print()`` function::

        print(
            s('example').bold().foreground(Color.GREEN)
        )

    """

    def bold(self) -> StyledString:
        """Increases the intensity of this string.

        Returns:
            A styled string with the bold text style applied.

        Depending on the configuration of the terminal, this may result in a
        bold font or a bright color.

        See Also
        --------

        - :doc:`/articles/tutorial`
        """
        return BoldString(self)

    def light(self) -> StyledString:
        """Decreases the intensity of this string.

        Depending on the configuration of the terminal, this may result in a
        light font or a dim color.

        Returns:
            A styled string with the light text style applied.

        See Also
        --------

        - :doc:`/articles/tutorial`
        """
        return LightString(self)

    def italic(self) -> StyledString:
        """Applies italic text style to this string.

        Returns:
            A styled string with the italic text style applied.

        See Also
        --------

        - :doc:`/articles/tutorial`
        """
        return ItalicString(self)

    def underlined(self) -> StyledString:
        """Draws a horizontal line below this string.

        Returns:
            A styled string with an underline.

        See Also
        --------

        - :doc:`/articles/tutorial`
        """
        return UnderlinedString(self)

    def blinking(self) -> StyledString:
        """Applies a blinking effect to this string."""
        return BlinkingString(self)

    def hidden(self) -> StyledString:
        """Makes this string invisible."""
        return HiddenString(self)

    def crossed_out(self) -> StyledString:
        """Crosses out this string with a horizontal line through the center."""
        return CrossedOutString(self)

    def doubly_underlined(self) -> StyledString:
        """Draws two horizontal lines at the bottom of this string.

        Returns:
            A styled string with two underlines.

        See Also
        --------

        - :doc:`/articles/tutorial`
        """
        return DoublyUnderlinedString(self)

    def framed(self) -> StyledString:
        """Draws a frame around this string."""
        return FramedString(self)

    def overlined(self) -> StyledString:
        """Draws a horizontal line at the above this string."""
        return OverlinedString(self)

    def foreground(self, color: Color) -> StyledString:
        """Applies a foreground color to this string.

        Args:
            color: The color that this string should have.

        Returns:
            A styled string with the specified foreground color.

        See Also
        --------

        .. docsummary::

            articles/tutorial

        .. autosummary::

            Color
            StyledString.background

        """
        return ForegroundColoredString(color, self)

    def background(self, color: Color) -> StyledString:
        """Applies a background color to this string.

        Args:
            color: The color that the background of this string should have.

        Returns:
            A styled string with the specified background color.

        See Also
        --------

        .. docsummary::

            articles/tutorial

        .. autosummary::

            Color
            StyledString.foreground

        """
        return BackgroundColoredString(color, self)

    def inverted(self) -> StyledString:
        """Swaps the foreground and background colors of this string."""
        return ColorInvertedString(self)

    def padded(self, num_spaces: int = 1) -> StyledString:
        """Adds padding to both sides of the string.

        Args:
            num_spaces: The number of space characters to be used as the
                padding, for each side of the string. If unspecified, a single
                space will be used.
        """
        return PaddedString(
            self,
            padding_left=num_spaces,
            padding_right=num_spaces
        )

    def padded_left(self, num_spaces: int = 1) -> StyledString:
        """Adds padding to the left side of the string.

        Args:
            num_spaces: The number of space characters to be used as the
                padding. If unspecified, a single space will be used.
        """
        return PaddedString(self, padding_left=num_spaces, padding_right=0)

    def padded_right(self, num_spaces: int = 1) -> StyledString:
        """Adds padding to the right side of the string.

        Args:
            num_spaces: The number of space characters to be used as the
                padding. If unspecified, a single space will be used.
        """
        return PaddedString(self, padding_left=0, padding_right=num_spaces)

    @property
    def rendered(self) -> str:
        """The rendered string containing the terminal commands that style this
        string according to the styling methods applied.

        You don't need to use this property to print a styled string to the
        terminal. :func:`StyledString.__str__() <neonsign.StyledString.__str__>`
        calls this method for you, so you can simply pass a ``StyledString``
        object to Python's :func:`str` directly to print it.
        """
        return self._render_impl(commands=())

    def __str__(self) -> str:
        """Renders this string as a Python string containing the terminal
        commands that style this string according to the styling methods
        applied.

        You don't need to call this method when printing a styled string. When
        you pass a ``StyledString`` object to Python's :func:`print`,
        ``StyledString.__str__()`` is automatically called.
        """
        return self.rendered

    @abstractmethod
    def _render_impl(self, commands: Tuple[StyleCommand, ...]) -> str:
        pass

    @property
    @abstractmethod
    def content(self) -> str:
        """The text-only content of this styled string."""
        pass

    @property
    @abstractmethod
    def layout_size(self) -> int:
        """The number of characters this string will appear to have when printed
        to the terminal."""
        pass


@final
@dataclass(frozen=True)
class PlainString(StyledString):
    """A plain string without any styles."""
    _content: str

    def _render_impl(self, commands: Tuple[StyleCommand, ...]) -> str:
        return _render_with_style_commands(
            content=self._content,
            commands=commands
        )

    @property
    def content(self) -> str:
        return self._content

    @property
    def layout_size(self) -> int:
        return len(self._content)


@final
@dataclass(frozen=True)
class ConcatenatedString(StyledString):
    """A styled string consisting of concatenated substrings."""
    substrings: Tuple[StyledString, ...]

    def _render_impl(self, commands: Tuple[StyleCommand, ...]) -> str:
        return ''.join(m._render_impl(commands) for m in self.substrings)

    @property
    def content(self) -> str:
        return ''.join(m.content for m in self.substrings)

    @property
    def layout_size(self) -> int:
        return sum(m.layout_size for m in self.substrings)


class StringWithCommand(StyledString):
    """A styled string with a terminal style command applied."""
    def __init__(self, original: StyledString, command: StyleCommand):
        self.original =original
        self.command = command

    def _render_impl(self, commands: Tuple[StyleCommand, ...]) -> str:
        return self.original._render_impl(commands + (self.command,))

    @property
    def content(self) -> str:
        return self.original.content

    @property
    def layout_size(self) -> int:
        return self.original.layout_size


@final
@dataclass
class BoldString(StringWithCommand):
    """A string with the terminal style command ``\\033[1m`` applied."""
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=1))


@final
@dataclass
class LightString(StringWithCommand):
    """A string with the terminal style command ``\\033[2m`` applied."""
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=2))


@final
@dataclass
class ItalicString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=3))


@final
@dataclass
class UnderlinedString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=4))


@final
@dataclass
class BlinkingString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=5))


@final
@dataclass
class HiddenString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=8))


@final
@dataclass
class CrossedOutString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=9))


@final
@dataclass
class DoublyUnderlinedString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=21))


@final
@dataclass
class FramedString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=51))


@final
@dataclass
class OverlinedString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=53))


@final
@dataclass
class ColorInvertedString(StringWithCommand):
    def __init__(self, original: StyledString):
        super().__init__(original=original, command=StyleCommand(command=7))


@final
@dataclass
class ForegroundColoredString(StringWithCommand):
    def __init__(self, color: Color, original: StyledString):
        self.color: Color = color
        super().__init__(
            original=original,
            command=command_for_foreground(color)
        )


@final
@dataclass
class BackgroundColoredString(StringWithCommand):
    def __init__(self, color: Color, original: StyledString):
        self.color: Color = color
        super().__init__(
            original=original,
            command=command_for_background(color)
        )


@final
@dataclass(frozen=True)
class PaddedString(StyledString):
    original: StyledString
    padding_left: int
    padding_right: int

    def _render_impl(self, commands: Tuple[StyleCommand, ...]) -> str:
        spaces_left: str = _render_with_style_commands(
            content=' ' * self.padding_left,
            commands=commands
        ) if self.padding_left > 0 else ''
        spaces_right: str = _render_with_style_commands(
            content=' ' * self.padding_right,
            commands=commands
        ) if self.padding_right > 0 else ''
        content: str = self.original._render_impl(commands)
        return f'{spaces_left}{content}{spaces_right}'

    @property
    def content(self) -> str:
        return self.original.content

    @property
    def layout_size(self) -> int:
        return (
            self.original.layout_size +
            self.padding_left +
            self.padding_right
        )


def _render_with_style_commands(
        content: str,
        commands: Tuple[StyleCommand, ...]
) -> str:
    if len(commands) == 0:
        return content
    render_code: str = ';'.join(
        map(
            str,
            chain.from_iterable(c.terminal_code for c in commands)
        )
    )
    return f'\033[{render_code}m{content}\033[m'
