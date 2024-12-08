from typing import Optional
from unittest import TestCase

from neonsign.string.styled_string import StyledString


def validate_styled_string(
        test_case: TestCase,
        expression: StyledString,
        expected_structure: Optional[StyledString] = None,
        expected_rendering: Optional[str] = None,
        expected_content: Optional[str] = None,
        expected_layout_size: Optional[int] = None,
):
    """Validates the correctness of a styled string expression.

    Args:

        test_case: The ``TestCase`` instance. Needed for making assertions.

        expression: The `s(...)` expression to be validated.

        expected_structure: A ``StyledString`` instance describing the correct
            structure that the expression is expected to evaluate to. This
            argument is optional. The correctness of the structure will only be
            checked if this argument is provided.

        expected_rendering: The correct result (a Python ``str``) that the
            expression is expected to render. This argument is optional. The
            correctness of the rendered string will only be checked if this
            argument is provided.

        expected_content: The correct text-only content that the expression is
            expected to return. This argument is optional. The correctness of
            the text-only content will only be checked if this argument is
            provided.

        expected_layout_size: The correct layout size that the expression is
            expected to return. The argument is optional. The correctness of the
            layout size will only be checked if this argument is provided.

    """

    if expected_structure is not None:
        test_case.assertEqual(expected_structure, expression)

    if expected_rendering is not None:
        test_case.assertEqual(expected_rendering, expression.rendered)

    if expected_content is not None:
        test_case.assertEqual(expected_content, expression.content)

    if expected_layout_size is not None:
        test_case.assertEqual(expected_layout_size, expression.layout_size)
