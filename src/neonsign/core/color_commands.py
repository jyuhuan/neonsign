from neonsign.core.colors import Color, Color24, Color8, SimpleColor
from neonsign.core.style_command import StyleCommand

_SIMPLE_COLOR_COMMANDS = {
    Color.BLACK: 30,
    Color.RED: 31,
    Color.GREEN: 32,
    Color.YELLOW: 33,
    Color.BLUE: 34,
    Color.MAGENTA: 35,
    Color.CYAN: 36,
    Color.WHITE: 37,
    Color.BRIGHT_BLACK: 90,
    Color.BRIGHT_RED: 91,
    Color.BRIGHT_GREEN: 92,
    Color.BRIGHT_YELLOW: 93,
    Color.BRIGHT_BLUE: 94,
    Color.BRIGHT_MAGENTA: 95,
    Color.BRIGHT_CYAN: 96,
    Color.BRIGHT_WHITE: 97,
}
"""Maps a simple color to its corresponding code in terminal."""


def command_for_foreground(color: Color) -> StyleCommand:
    """Creates a style command that sets the terminal's foreground color.

    Args:
        color: The foreground color.

    Returns: A style command that sets the terminal's foreground color to the
        specified color.

    Raises:
        TypeError: when the type of the color is not recognized.

    """

    if isinstance(color, SimpleColor):
        return StyleCommand(command=_SIMPLE_COLOR_COMMANDS[color])
    elif isinstance(color, Color8):
        return StyleCommand(command=38, args=(5, color.index))
    elif isinstance(color, Color24):
        return StyleCommand(
            command=38,
            args=(2, color.red, color.green, color.blue)
        )
    else:
        raise TypeError(f'Unknown color type {type(color)}!')


def command_for_background(color: Color) -> StyleCommand:
    """Creates a style command that sets the terminal's background color.

    Args:
        color: The background color.

    Returns: A style command that sets the terminal's background color to the
        specified color.

    Raises:
        TypeError: when the type of the color is not recognized.

    """

    foreground_command: StyleCommand = command_for_foreground(color)
    return StyleCommand(
        command=foreground_command.command + 10,
        args=foreground_command.args
    )
