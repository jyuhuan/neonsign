from __future__ import annotations

from typing import Union

from neonsign.styled_string import PlainString, ConcatenatedString, StyledString


def construct_multiple(*contents: Union[str, StyledString]) -> StyledString:
    if len(contents) == 1:
        return construct_single(contents[0])
    return ConcatenatedString(
        tuple(construct_single(obj) for obj in contents)
    )


def construct_single(obj: Union[str, StyledString]) -> StyledString:
    if isinstance(obj, StyledString):
        return obj
    if isinstance(obj, str):
        return PlainString(obj)
    raise TypeError(
        f'Contents passed to s() must be either a str or a StyledString, '
        f'but {obj} is a {type(obj)}!'
    )
