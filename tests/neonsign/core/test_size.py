import sys
from unittest import TestCase

from neonsign.core.size import Size


class TestSize(TestCase):

    def test_constructors(self):
        self.assertEqual(Size(width=0, height=0), Size.zero())
        self.assertEqual(
            Size(width=sys.maxsize, height=sys.maxsize),
            Size.max()
        )
        for l in range(0, 100, 5):
            self.assertEqual(Size(width=l, height=l), Size.square(l))

    def test_validation(self):
        with self.assertRaises(ValueError) as e:
            Size(width=-1, height=0)
        self.assertEqual(
            'The width of a size must be non-negative, and not -1!',
            str(e.exception)
        )
        with self.assertRaises(ValueError) as e:
            Size(width=0, height=-1)
        self.assertEqual(
            'The height of a size must be non-negative, and not -1!',
            str(e.exception)
        )

    def test_properties(self):
        self.assertEqual(0, Size(width=0, height=0).area)
        self.assertEqual(0, Size(width=0, height=10).area)
        self.assertEqual(0, Size(width=10, height=0).area)
        self.assertEqual(200, Size(width=10, height=20).area)

    def test_can_fit_within(self):
        size_0 = Size(width=0, height=0)
        size_1 = Size(width=10, height=20)
        size_2 = Size(width=100, height=200)
        size_3 = Size(width=200, height=100)
        self.assertTrue(size_0.can_fit_within(size_1))
        self.assertTrue(size_1.can_fit_within(size_1))
        self.assertTrue(size_1.can_fit_within(size_2))
        self.assertFalse(size_2.can_fit_within(size_3))

    def test_updating_methods(self):
        self.assertEqual(
            Size(width=1, height=20),
            Size(width=10, height=20).with_updated_width(1)
        )
        self.assertEqual(
            Size(width=10, height=2),
            Size(width=10, height=20).with_updated_height(2)
        )
        self.assertEqual(
            Size(width=1, height=2),
            Size(width=10, height=20)
            .with_updated_width(1)
            .with_updated_height(2)
        )
        self.assertEqual(
            Size(width=11, height=20),
            Size(width=10, height=20).increased_by(width_delta=1)
        )
        self.assertEqual(
            Size(width=10, height=22),
            Size(width=10, height=20).increased_by(height_delta=2)
        )
        self.assertEqual(
            Size(width=11, height=22),
            Size(width=10, height=20).increased_by(
                width_delta=1,
                height_delta=2
            )
        )

    def test_comparison_operators(self):
        size_0 = Size.zero()
        size_1 = Size(width=10, height=20)
        size_2 = Size.max()
        self.assertTrue(size_0 < size_1)
        self.assertTrue(size_1 < size_2)
        self.assertTrue(size_0 <= size_0)
        self.assertTrue(size_0 <= size_1)
        self.assertTrue(size_0 <= size_2)
        self.assertTrue(size_2 > size_1)
        self.assertTrue(size_1 > size_0)
        self.assertTrue(size_2 >= size_2)
        self.assertTrue(size_2 >= size_1)
        self.assertTrue(size_2 >= size_0)

    def test_string_representation(self):
        self.assertEqual('10x20', str(Size(width=10, height=20)))
