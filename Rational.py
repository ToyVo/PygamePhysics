"""
Create a class of Rational numbers and overload the following operators:
==, +, -, unary -, *, /, abs(), int(), float().
Their output should be obvious, but feel free to ask me any questions.
Be sure to correctly overload == first, because all the other tests depend on this.
When instantiated, the numerator and denominator must be integers, so raise a TypeError if not.
For example: raise(TypeError("Numerator must be an integer.")).
Also, the denominator cannot be zero, so raise a ValueError if this happens.
It would be best to simplify all rationals to lowest terms with positive denominators at instantiation.
You may (should) import math and use math.gcd(a, b) to help with this.
Use the associated test file to help guide you.
(10 pts)
"""
import math


class Rational:
    def __init__(self, numerator, denominator=1):
        if not isinstance(numerator, int):
            raise (TypeError("Numerator must be an integer"))
        elif not isinstance(denominator, int):
            raise (TypeError("Denominator must be an integer"))
        elif denominator == 0:
            raise ValueError("Denominator must not be zero")
        else:
            if denominator < 0:
                denominator *= -1
                numerator *= -1
            greatest_common_denominator = math.gcd(numerator, denominator)
            self.numerator = numerator // greatest_common_denominator
            self.denominator = denominator // greatest_common_denominator

    # Done for you
    def __repr__(self):
        return "Rational(" + str(self.numerator) + ", " + str(self.denominator) + ")"

    def __str__(self):
        return "(" + str(self.numerator) + " / " + str(self.denominator) + ")"

    # ==
    def __eq__(self, other: 'Rational'):
        return self.numerator == other.numerator and self.denominator == other.denominator

    # +
    def __add__(self, other: 'Rational'):
        num = self.numerator * other.denominator
        num += other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Rational(num, denominator)

    # -
    def __sub__(self, other: 'Rational'):
        num = self.numerator * other.denominator
        num -= other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Rational(num, denominator)

    # unary -
    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    # *
    def __mul__(self, other: 'Rational'):
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    # /
    def __truediv__(self, other: 'Rational'):
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)

    # abs()
    def __abs__(self):
        return self.abs()

    def abs(self):
        return Rational(abs(self.numerator), self.denominator)

    # int()
    def __int__(self):
        return self.int()

    def int(self):
        return round(self.numerator // self.denominator)

    # float()
    def __float__(self):
        return self.float()

    def float(self):
        return self.numerator / self.denominator
