from math import pi, sqrt
from unittest import TestCase

from Vec2 import Vec2


# noinspection PyTypeChecker
class TestVec2(TestCase):
    def test_int(self):
        self.assertEqual(Vec2(1.1, 5.2).int(), (1, 5))
        self.assertEqual(Vec2(1.1, 5.7).int(), (1, 6))
        self.assertEqual(Vec2(-1.1, 5.2).int(), (-1, 5))
        self.assertEqual(Vec2(-1.1, -5.6).int(), (-1, -6))

    def test___eq__(self):
        self.assertTrue(Vec2(1, 2) == Vec2(1.0, 2.0))
        self.assertFalse(Vec2(1, 2) == Vec2(-1, 2))

    def test___bool__(self):
        self.assertTrue(Vec2(1, 2))
        self.assertFalse(Vec2(0.0, 0.0))

    def test___add__(self):
        self.assertEqual(Vec2(1, 2) + Vec2(3, -4), Vec2(4, -2))

    def test___iadd__(self):
        v = Vec2(1, 2)
        u = v
        v += Vec2(3, -4)
        self.assertEqual(v, Vec2(4, -2))
        self.assertTrue(u is v)

    def test___neg__(self):
        self.assertEqual(-Vec2(1, 2), Vec2(-1, -2))
        self.assertEqual(Vec2(3, -4), --Vec2(3, -4))

    def test___sub__(self):
        self.assertEqual(Vec2(1, 2) - Vec2(3, -4), Vec2(-2, 6))

    def test___isub__(self):
        v = Vec2(1, 2)
        u = v
        v -= Vec2(3, -4)
        self.assertEqual(v, Vec2(-2, 6))
        self.assertTrue(u is v)

    def test___mul__(self):
        self.assertEqual(3.3 * Vec2(1, -2), Vec2(3.3, -6.6))

    def __imul__(self):
        v = Vec2(1, -2)
        v *= 3.3
        u = v
        self.assertEqual(v, Vec2(3.3, -6.6))
        self.assertTrue(u is v)

    def test___truediv__(self):
        self.assertEqual(Vec2(1, -2) / 2, Vec2(0.5, -1))

    def __idiv__(self):
        v = Vec2(1, -2)
        v *= 3.3
        u = v
        self.assertEqual(v, Vec2(3.3, -6.6))
        self.assertTrue(u is v)

    def test___matmul__(self):
        self.assertEqual(Vec2(1, 2) @ Vec2(3, -4), -5)

    def test___mod__(self):
        self.assertEqual(-10, Vec2(1, 2) % Vec2(3, -4))

    def test_perp(self):
        self.assertEqual(Vec2(-4, 3), Vec2(3, 4).perp())
        self.assertEqual(Vec2(-4, 3), ~Vec2(3, 4))

    def test_mag2(self):
        self.assertEqual(5, Vec2(1, -2).mag2())

    def test_mag(self):
        self.assertEqual(5, Vec2(3, -4).mag())

    def test_hat(self):
        self.assertAlmostEqual(Vec2(0.6, -0.8), Vec2(3, -4).hat(), 7)

    def test_normalize(self):
        v = Vec2(3, -4)
        v.normalize()
        self.assertAlmostEqual(Vec2(0.6, -0.8), v, 7)

    def test_rotated(self):
        self.assertAlmostEqual(Vec2(1, -2).rotated(pi / 2), Vec2(2, 1), 7)
        self.assertAlmostEqual(Vec2(1, 1).rotated(pi / 4), Vec2(0, sqrt(2)), 7)

    def test_change_to(self):
        v = Vec2(1, 2)
        u = v
        w = Vec2(3, -4)
        v.change_to(w)
        self.assertEqual(w, v)
        self.assertFalse(v is w)
        self.assertTrue(u is v)

    def test_copy(self):
        v = Vec2(1, 2)
        w = v.copy()
        self.assertEqual(v, w)
        self.assertFalse(v is w)
