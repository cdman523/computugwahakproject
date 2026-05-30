import math as m


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __sub__(self, other: "Vector") -> "Vector":
        return self + other * (-1)

    def __truediv__(self, scalar: float) -> "Vector":
        return self * (1 / scalar)

    def __eq__(self, other: "Vector") -> bool:
        return (self.x, self.y) == (other.x, other.y)

    @classmethod
    def angVec(cls, r: float, theta: float) -> "Vector":
        return cls(m.cos(m.radians(theta)), m.sin(m.radians(theta))) * r

    def __abs__(self) -> float:
        return m.hypot(self.x, self.y)

    @property
    def angle(self) -> float:
        return m.degrees(m.atan2(self.y, self.x))
