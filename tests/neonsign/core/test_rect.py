from unittest import TestCase

from neonsign.core.point import Point
from neonsign.core.rect import Rect
from neonsign.core.size import Size


class TestRect(TestCase):

    def test_properties(self):
        r = Rect(top_left=Point(x=10, y=20), size=Size(width=90, height=180))
        self.assertEqual(Point(x=100, y=20), r.top_right)
        self.assertEqual(Point(x=10, y=200), r.bottom_left)
        self.assertEqual(Point(x=100, y=200), r.bottom_right)
        self.assertEqual(10, r.left)
        self.assertEqual(20, r.top)
        self.assertEqual(100, r.right)
        self.assertEqual(200, r.bottom)

    def test_transformations(self):
        r = Rect(top_left=Point(x=10, y=20), size=Size(width=90, height=180))
        self.assertEqual(r, r.moved_by())
        self.assertEqual(
            Rect(top_left=Point(x=11, y=20), size=Size(width=90, height=180)),
            r.moved_by(x_delta=1)
        )
        self.assertEqual(
            Rect(top_left=Point(x=10, y=22), size=Size(width=90, height=180)),
            r.moved_by(y_delta=2)
        )
        self.assertEqual(
            Rect(top_left=Point(x=11, y=22), size=Size(width=90, height=180)),
            r.moved_by(x_delta=1, y_delta=2)
        )
        self.assertEqual(
            Rect(top_left=Point(x=0, y=0), size=Size(width=90, height=180)),
            r.moved_to_origin()
        )

    def test_constructors(self):
        self.assertEqual(
            Rect(top_left=Point(x=0, y=0), size=Size(width=0, height=0)),
            Rect.zero()
        )
        self.assertEqual(
            Rect(top_left=Point(x=0, y=0), size=Size(width=10, height=20)),
            Rect.from_origin(Size(width=10, height=20))
        )

    def test_intersect(self):
        r0 = Rect(top_left=Point(x=0, y=0), size=Size(width=7, height=5))
        r1 = Rect(top_left=Point(x=3, y=-1), size=Size(width=5, height=3))
        r2 = Rect(top_left=Point(x=3, y=3), size=Size(width=5, height=3))
        r3 = Rect(top_left=Point(x=-1, y=3), size=Size(width=5, height=3))
        r4 = Rect(top_left=Point(x=-1, y=-1), size=Size(width=5, height=3))
        r5 = Rect(top_left=Point(x=1, y=1), size=Size(width=5, height=3))
        r6 = Rect(top_left=Point(x=6, y=1), size=Size(width=5, height=3))
        r7 = Rect(top_left=Point(x=9, y=1), size=Size(width=5, height=3))

        test_cases = [
            (r0, r1, Size(width=4, height=2), Point(x=3, y=0), Point(x=0, y=1)),
            (r0, r2, Size(width=4, height=2), Point(x=3, y=3), Point(x=0, y=0)),
            (r0, r3, Size(width=4, height=2), Point(x=0, y=3), Point(x=1, y=0)),
            (r0, r4, Size(width=4, height=2), Point(x=0, y=0), Point(x=1, y=1)),
            (r0, r5, Size(width=5, height=3), Point(x=1, y=1), Point(x=0, y=0)),
            (r0, r6, Size(width=1, height=3), Point(x=6, y=1), Point(x=0, y=0)),
        ]

        for x, y, expected_size, expected_top_left_in_x, expected_top_left_in_y in test_cases:
            intersect_in_x = x.intersect(y)
            self.assertEqual(expected_size, intersect_in_x.size)
            self.assertEqual(expected_top_left_in_x, intersect_in_x.top_left)
            intersect_in_y = y.intersect(x)
            self.assertEqual(expected_size, intersect_in_y.size)
            self.assertEqual(expected_top_left_in_y, intersect_in_y.top_left)

        self.assertIsNone(r0.intersect(r7))
