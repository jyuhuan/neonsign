from unittest import TestCase

from neonsign.core.point import Point


class TestPoint(TestCase):

    def test_moving(self):
        p = Point(x=10, y=20)
        self.assertEqual(p, p.moved_by())
        self.assertEqual(p, p.moved_by(x_delta=0))
        self.assertEqual(p, p.moved_by(y_delta=0))
        self.assertEqual(p, p.moved_by(x_delta=0, y_delta=0))
        self.assertEqual(Point(x=11, y=20), p.moved_by(x_delta=1))
        self.assertEqual(Point(x=10, y=22), p.moved_by(y_delta=2))
        self.assertEqual(Point(x=11, y=22), p.moved_by(x_delta=1, y_delta=2))

    def test_origin_constructor(self):
        self.assertEqual(0, Point.origin().x)
        self.assertEqual(0, Point.origin().y)

    def test_string_representation(self):
        p = Point(x=10, y=20)
        self.assertEqual('(10, 20)', str(p))
