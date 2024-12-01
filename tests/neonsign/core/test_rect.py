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

    def test_constructors(self):
        self.assertEqual(
            Rect(top_left=Point(x=0, y=0), size=Size(width=0, height=0)),
            Rect.zero()
        )
