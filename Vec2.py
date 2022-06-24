import math
from typing import Tuple


class Vec2:
    # initialization in two different ways
    def __init__(self, x: Tuple[float, float] or float = (0, 0), y: float = None):
        if y is None:
            try:
                if len(x) == 2:
                    self.x: float = x[0]
                    self.y: float = x[1]
            except TypeError:
                raise ValueError("Incorrect single-argument instantiation of Vec2")
        else:
            self.x = x
            self.y = y

    # code representation
    def __repr__(self) -> str:
        return "Vec2(" + str(self.x) + ", " + str(self.y) + ")"

    # make Vec2 readable like a list of two elements
    def __len__(self) -> int:
        return 2

    def __getitem__(self, i: int) -> float:
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError("Index out of range.")

    # Output as a tuple of integers, necessary for pygame graphics
    def int(self) -> Tuple[int, int]:
        return round(self.x), round(self.y)

    # Check if the vector is nonzero
    # return false if vector is the zero vector, true otherwise
    def __bool__(self) -> bool:
        if self.x == 0 and self.y == 0:
            return False
        else:
            return True

    def __eq__(self, other: 'Vec2') -> bool:
        return self.x == other.x and self.y == other.y

    # + operator overload
    # return a new Vec2 that is the vector sum of self and other
    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    # += operator overload
    # mutate self to be the vector sum of self and other
    def __iadd__(self, other: 'Vec2') -> 'Vec2':
        self.x += other.x
        self.y += other.y
        return self

    # - unary operator overload
    # return a new vector that is opposite this one
    def __neg__(self) -> 'Vec2':
        return Vec2(-self.x, -self.y)

    # - operator overload
    def __sub__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x - other.x, self.y - other.y)

    # -= operator overload
    def __isub__(self, other: 'Vec2') -> 'Vec2':
        self.x -= other.x
        self.y -= other.y
        return self

    # * operator overload (scalar multiplication)
    def __mul__(self, other: float) -> 'Vec2':
        return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> 'Vec2':
        return Vec2(self.x * other, self.y * other)

    # *= operator overload
    def __imul__(self, other: float) -> 'Vec2':
        self.x *= other
        self.y *= other
        return self

    # / operator overload (scalar division)
    def __truediv__(self, other: float) -> 'Vec2':
        return Vec2(self.x / other, self.y / other)

    # /= operator overload
    def __idiv__(self, other: float) -> 'Vec2':
        self.x /= other
        self.y /= other
        return self

    # @ operator overload (dot product between vectors, returns a scalar)
    def __matmul__(self, other: 'Vec2') -> float:
        return self.x * other.x + self.y * other.y

    # perpendicular to a vector, rotated counterclockwise by 90 degrees
    def perp(self) -> 'Vec2':
        return Vec2(-self.y, self.x)

    # makes ~ operator equivalent to perp()
    # ~~v is this equivalent to -v
    def __invert__(self) -> 'Vec2':
        return self.perp()

    # % operator overload (cross product between vectors, returns a scalar, which is the z component of the result)
    # equivalent to self.perp() @ other, or ~self @ other
    def __mod__(self, other: 'Vec2') -> float:
        return ~self @ other

    # magnitude squared
    def mag2(self) -> float:
        return self.x * self.x + self.y * self.y

    # magnitude
    def mag(self) -> float:
        return math.sqrt(self.mag2())

    def __abs__(self) -> float:
        return self.mag()  # overload abs() operator

    # unit vector
    # return a new unit vector in the same direction
    def hat(self) -> 'Vec2':
        try:
            length = self.mag()
            return self / length
        except ZeroDivisionError:
            return Vec2(0, 0)

    # normalize this vector
    def normalize(self) -> 'Vec2':
        length = self.mag()
        self.x /= length
        self.y /= length
        return self

    # rotation to return a new vector
    # return a new vector with a counterclockwise rotation
    def rotated(self, radians_or_sine: float, cosine: float = None) -> 'Vec2':
        if cosine is None:
            radians = radians_or_sine
            s = math.sin(radians)
            c = math.cos(radians)
        else:
            s = radians_or_sine
            c = cosine
        return Vec2(c * self.x - s * self.y, s * self.x + c * self.y)

    def change_to(self, other: 'Vec2') -> 'Vec2':
        self.x = other[0]
        self.y = other[1]
        return self

    def copy(self) -> 'Vec2':
        return Vec2(self)

    def rotate_sin_cos(self, s, c) -> 'Vec2':
        return Vec2(c * self.x - s * self.y, s * self.x + c * self.y)
