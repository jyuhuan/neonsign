from typing import Union

from neonsign.styled_string import StyledString
from neonsign.styled_string_factory import construct_multiple


def s(*contents: Union[str, StyledString]) -> StyledString:
    """Wraps the specified contents so that styles can be added to them.

    Args:
        *contents: One or more Python strings, one or more :class:`StyledString`
            objects, or a mix of both.

    Returns:
        A styled string object.

    Overview
    --------

    All styling methods are offered through the :class:`~neonsign.StyledString`
    class. To use them, wrap your Python string with ``s()``, followed by one or
    more calls to styling methods::

        s('example').bold().background(Color.GREEN)

    """
    return construct_multiple(*contents)
