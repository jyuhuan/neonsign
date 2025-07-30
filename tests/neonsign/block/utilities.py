import sys
from typing import Callable, List, Optional, Set
from unittest import TestCase

from neonsign import (
    Block
)
from neonsign.block.canvas import Canvas
from neonsign.core.size import Size

MAX = sys.maxsize
"""An alias for ``sys.maxsize`` to keep test code short."""


DEFAULT_TEST_CONSTRAINTS: List[int] = list(range(0, 30, 2)) + [MAX]


def run_size_and_render_tests(
        test_case: TestCase,
        block: Block,
        expected_unconstrained_size: Size,
        expected_size_given_width_constraint_only: Callable[[int], Size],
        expected_size_given_height_constraint_only: Callable[[int], Size],
        expected_size_given_both_constraints: Callable[[int, int], Size],
        expected_canvas: Callable[[Size], Canvas],
        width_constraints_to_test: Optional[List[int]] = None,
        height_constraints_to_test: Optional[List[int]] = None,
):
    if width_constraints_to_test is None:
        width_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
    if height_constraints_to_test is None:
        height_constraints_to_test = DEFAULT_TEST_CONSTRAINTS

    observed_sizes = (
        {run_unconstrained_size_test(
            test_case,
            block,
            expected_unconstrained_size
        )}
        | run_horizontal_squeeze_test(
            test_case,
            block,
            expected_size_given_width_constraint_only,
            width_constraints_to_test=width_constraints_to_test
        )
        | run_vertical_squeeze_test(
            test_case,
            block,
            expected_size_given_height_constraint_only,
            height_constraints_to_test=height_constraints_to_test
        )
        | run_both_directions_squeeze_test(
            test_case,
            block,
            expected_size_given_both_constraints,
            width_constraints_to_test=width_constraints_to_test,
            height_constraints_to_test=height_constraints_to_test
        )
    )

    run_render_test(
        test_case,
        block,
        {_ for _ in observed_sizes if _.width < 1000 and _.height < 1000},
        expected_canvas
    )

def run_unconstrained_size_test(
        test_case: TestCase,
        block: Block,
        expected_unconstrained_size: Size
) -> Size:
    observed_size = expected_unconstrained_size
    test_case.assertEqual(
        observed_size,
        block.unconstrained_size
    )
    return observed_size

def run_horizontal_squeeze_test(
        test_case: TestCase,
        block: Block,
        expected_size_given_width_constraint_only: Callable[[int], Size],
        width_constraints_to_test: Optional[List[int]] = None,
) -> Set[Size]:
    if width_constraints_to_test is None:
        width_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
    observed_sizes: Set[Size] = set()
    for width_constraint in width_constraints_to_test:
        observed_size = block.measure(
            width_constraint=width_constraint
        )
        test_case.assertEqual(
            expected_size_given_width_constraint_only(width_constraint),
            observed_size
        )
        if observed_size < Size(width=100, height=100):
            observed_sizes.add(observed_size)
    return observed_sizes

def run_vertical_squeeze_test(
        test_case: TestCase,
        block: Block,
        expected_size_given_height_constraint_only: Callable[[int], Size],
        height_constraints_to_test: Optional[List[int]] = None,
) -> Set[Size]:
    if height_constraints_to_test is None:
        height_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
    observed_sizes: Set[Size] = set()
    for height_constraint in height_constraints_to_test:
        observed_size: Size = block.measure(
            height_constraint=height_constraint
        )
        test_case.assertEqual(
            expected_size_given_height_constraint_only(height_constraint),
            observed_size
        )
        if observed_size < Size(width=100, height=100):
            observed_sizes.add(observed_size)
    return observed_sizes

def run_both_directions_squeeze_test(
        test_case: TestCase,
        block: Block,
        expected_size_given_both_constraints: Callable[[int, int], Size],
        width_constraints_to_test: Optional[List[int]] = None,
        height_constraints_to_test: Optional[List[int]] = None,
) -> Set[Size]:
    if width_constraints_to_test is None:
        width_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
    if height_constraints_to_test is None:
        height_constraints_to_test = DEFAULT_TEST_CONSTRAINTS
    observed_sizes: Set[Size] = set()
    for height_constraint in height_constraints_to_test:
        for width_constraint in width_constraints_to_test:
            observed_size = block.measure(
                width_constraint=width_constraint,
                height_constraint=height_constraint
            )
            test_case.assertEqual(
                expected_size_given_both_constraints(
                    width_constraint,
                    height_constraint
                ),
                observed_size
            )
            if observed_size < Size(width=100, height=100):
                observed_sizes.add(observed_size)
    return observed_sizes

def run_render_test(
        test_case: TestCase,
        block: Block,
        sizes: Set[Size],
        expected_canvas_at_sizes: Callable[[Size], Canvas]
):
    for size in sizes:
        test_case.assertEqual(
            expected_canvas_at_sizes(size),
            block.render(granted_size=size)
        )
