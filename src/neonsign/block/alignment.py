from enum import Enum


class Alignment(Enum):
    """Alignment in an axis.

    A text block has two axes:

    - the x-axis goes from left to right horizontally, and
    - the y-axis goes from top to bottom vertically.

    Use the values in the ``Alignment`` enum to choose a preferred general
    position (start, center, or end) in either the x-axis or the y-axis.
    The exact location is determined by the styled block that is asking for the
    alignment preference.
    """

    START = 'start'
    CENTER = 'center'
    END = 'end'
