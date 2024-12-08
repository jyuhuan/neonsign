from dataclasses import dataclass, field
from typing import Tuple, final


@final
@dataclass(frozen=True)
class StyleCommand:
    """A command that tells the terminal to stylize the text it renders.

    Examples:

        - ``StyleCommand(1)`` makes text bold.
        - ``StyleCommand(4)`` draws underline.
        - ``StyleCommand(32)`` makes text green.
        - ``StyleCommand(38, args=(2, r, g, b))`` colors text with an RGB color.
    """

    command: int
    """The number that identifies the style command."""

    args: Tuple[int, ...] = field(default_factory=lambda: ())
    """The arguments that customize the style command.
    
    Not all style commands have arguments. Commands such as bold, underline, and
    simple colors do not have any arguments. For those commands, this field will
    be the empty tuple, ``()``.
    """

    @property
    def terminal_code(self) -> Tuple[int, ...]:
        """The tuple of integers representing the full command including the
        arguments.

        For example, the following code::

            StyleCommand(38, args=(2, 255, 0, 0)).terminal_code

        returns ``(2, 255, 0, 0)``.
        """
        return (self.command,) + self.args
