import math
import numbers
import copy

class Vec3:
    def __init__(self, x, y, z):
        if not isinstance(x, numbers.Real):
            raise TypeError("x must be an instance of numbers.Real")
        if not isinstance(y, numbers.Real):
            raise TypeError("y must be an instance of numbers.Real")
        if not isinstance(z, numbers.Real):
            raise TypeError("z must be an instance of numbers.Real")
        self.x = x
        self.y = y
        self.z = z

    def mag2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def mag(self):
        return math.sqrt(self.mag2())

    def normal(self):
        return self / self.mag()

    def cross(self, other):
        if not isinstance(other, Vec3):
            raise TypeError("Can only cross with other Vec3s")
        x = ( self.y * other.z ) - ( self.z * other.y )
        y = ( self.z * other.x ) - ( self.x * other.z )
        z = ( self.x * other.y ) - ( self.y * other.x )
        return Vec3(x, y, z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def dist2(self, other):
        return ( self.x - other.x ) ** 2 + ( self.y - other.y ) ** 2 + ( self.z - other.z) ** 2

    def dist(self, other):
        return math.sqrt(self.dist2(other))

    # implement vector swizling for no good reason other than "BECAUSE WE CAN"
    def __getattribute__(self, name):
        if len(name) == 3 and all([c in "xyz" for c in name]):
            data = []
            for i in range(0, 3):
                if c[i] == 'x':
                    data.append(self.x)
                elif c[i] == 'y':
                    data.append(self.y)
                elif c[i] == 'z':
                    data.append(self.z)
            return Vec3(data[0], data[1], data[2])
        else:
            return object.__getattribute__(self, name)

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return Vec3(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            return Vec3(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __repr__(self):
        return "<{x}, {y}, {z}>".format(x=self.x, y=self.y, z=self.z)

def get_min_max_vec3(l):
    i = copy.copy(l[0]) # mIn
    a = copy.copy(l[0]) # mAx
    for j in l:
        if j.x < i.x:
            i.x = j.x
        elif j.x > a.x:
            a.x = j.x
        if j.y < i.y:
            i.y = j.y
        elif j.y > a.y:
            a.y = j.y
        if j.z < i.z:
            i.z = j.z
        elif j.z > a.z:
            a.z = j.z
    return (i, a)

class BoundingVolume:
    def __init__(self, a, b, content):
        if not isinstance(a, Vec3):
            raise TypeError("a must be a Vec3")
        if not isinstance(b, Vec3):
            raise TypeError("b must be a Vec3")
        self._a = a
        self._b = b
        self.recompute_corners()
        self.content = content

    def get_width(self):
        return self.b.x - self.a.x

    def get_height(self):
        return self.b.y - self.a.y

    def get_depth(self):
        return self.b.z - self.a.z

    def get_a(self):
        return self._a

    def set_a(self, a):
        self._a = a
        self.recompute_corners()

    def set_b(self, b):
        self._b = b
        self.recompute_corners()

    def recompute_corners(self):
        a = self._a
        b = self._b
        self._a = Vec3(min(a.x, b.x)
                      ,min(a.y, b.y)
                      ,min(a.z, b.z))
        self._b = Vec3(max(a.x, b.x)
                      ,max(a.y, b.y)
                      ,max(a.z, b.z))

    def corners(self):
        a = self.a
        b = self.b
        return [Vec3(a.x, a.y, a.z)
               ,Vec3(a.x, a.y, b.z)
               ,Vec3(a.x, b.y, a.z)
               ,Vec3(a.x, b.y, b.z)
               ,Vec3(b.x, a.y, a.z)
               ,Vec3(b.x, a.y, b.z)
               ,Vec3(b.x, b.y, a.z)
               ,Vec3(b.x, b.y, b.z)]

    def faces(self):
        # We should be using ccw winding
        corners = self.corners()
        return [(corners[0], corners[1], corners[3], corners[2])
               ,(corners[0], corners[4], corners[5], corners[1])
               ,(corners[0], corners[2], corners[6], corners[4])
               ,(corners[7], corners[3], corners[1], corners[5])
               ,(corners[7], corners[5], corners[4], corners[6])
               ,(corners[7], corners[6], corners[2], corners[3])]

    def get_b(self):
        return self._b

    def contains(self, p):
        if isinstance(p, Vec3):
            dp = p - self.a
            db = self.b - self.a
            return db.x > dp.x and db.y > dp.y and db.z > dp.z and dp.x > 0 and dp.y > 0 and dp.z > 0

        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, BoundingVolume):
            return NotImplemented

        return self.a == other.a and self.b == other.b

    width = property(get_width)
    height = property(get_height)
    depth = property(get_depth)
    a = property(get_a, set_a)
    b = property(get_b, set_b)

    def __str__(self):
        return ("<BoundingVolume {_a} {_b}>".format(**self.__dict__))

    def __repr__(self):
        return ("<BoundingVolume {_a} {_b}>".format(**self.__dict__))
