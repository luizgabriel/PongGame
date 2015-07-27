class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2d(self.x * other, self.y * other)

    def __neg__(self):
        return self * -1

    def module(self):
        return self.x * self.x + self.y * self.y

    def __float__(self):
        return self.module()

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

    @staticmethod
    def distance(vector2d_A, vector2d_B):
        return float(vector2d_B - vector2d_A)

    @staticmethod
    def null():
        return Vector2d(0, 0)
