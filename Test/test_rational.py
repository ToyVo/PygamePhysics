from unittest import TestCase

from Rational import Rational


class TestRational(TestCase):
    def test_init(self):
        self.assertRaises(TypeError, lambda: Rational(1.5, 2))
        self.assertRaises(TypeError, lambda: Rational(2, 2.5))
        self.assertRaises(TypeError, lambda: Rational(1.5, 2.5))
        self.assertRaises(ValueError, lambda: Rational(4, 0))

    def test_eq(self):
        self.assertEqual(Rational(3, 4), Rational(3, 4))
        self.assertNotEqual(Rational(3, 4), Rational(-3, 4))
        self.assertNotEqual(Rational(3, 4), Rational(3, -4))
        self.assertEqual(Rational(3, 4), Rational(-3, -4))
        self.assertEqual(Rational(2, 5), Rational(12, 30))
        self.assertEqual(Rational(2, -5), Rational(-12, 30))

    def test_add(self):
        self.assertEqual(Rational(7, 12), Rational(1, 3) + Rational(1, 4))
        self.assertEqual(Rational(5, 12), Rational(1, 6) + Rational(1, 4))

    def test_sub(self):
        self.assertEqual(Rational(1, 12), Rational(1, 3) - Rational(1, 4))
        self.assertEqual(Rational(-1, 12), Rational(1, 6) - Rational(1, 4))

    def test_mul(self):
        self.assertEqual(Rational(15, 8), Rational(5, 2) * Rational(3, 4))
        self.assertEqual(Rational(5, 8), Rational(5, 6) * Rational(3, 4))

    def test_div(self):
        self.assertEqual(Rational(20, 21), Rational(5, 7) / Rational(3, 4))
        self.assertEqual(Rational(10, 9), Rational(5, 6) / Rational(3, 4))

    def test_neg(self):
        self.assertEqual(Rational(-3, 4), -Rational(3, 4))

    def test_abs(self):
        self.assertEqual(Rational(3, 4), abs(Rational(3, 4)))
        self.assertEqual(Rational(3, 4), abs(Rational(-3, 4)))

    def test_int(self):
        self.assertEqual(0, int(Rational(3, 4)))
        self.assertEqual(1, int(Rational(5, 4)))
        self.assertEqual(2, int(Rational(9, 4)))
        self.assertEqual(-1, int(Rational(-2, 3)))

    def test_float(self):
        self.assertAlmostEqual(0.75, float(Rational(3, 4)))
        self.assertAlmostEqual(1.25, float(Rational(5, 4)))
        self.assertAlmostEqual(2.25, float(Rational(9, 4)))
        self.assertAlmostEqual(-2 / 3, float(Rational(-2, 3)))
