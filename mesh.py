import math
from geometry import Vec3, BoundingVolume
from materials import Material
import abc

class Vertex:
    def __init__(self, pos, normal):
        if not isinstance(pos, Vec3):
            raise TypeError("pos must be a Vec3")
        if not isinstance(normal, Vec3):
            raise TypeError("normal must be a Vec3")

        self.pos = pos
        self.normal = normal

class Triangle:
    def __init__(self, a, b, c, mat):
        if not all([isinstance(x, Vertex) for x in [a, b, c]]):
            raise TypeError("a, b, and c must all be verticies")
        if not isinstance(mat, Material):
            raise TypeError('mat must be a Material')

        self.a = a
        self.b = b
        self.c = c
        self.material = mat

    # TODO: implement some sort of smoothing function
    def normal(self, p):
        return self.a.normal

    def bounding_volume(self):
        a = self.a.pos
        b = self.b.pos
        c = self.c.pos
        d = Vec3(min(a.x, b.x, c.x),
                 min(a.y, b.y, c.y),
                 min(a.z, b.z, c.z))
        e = Vec3(max(a.x, b.x, c.x),
                 max(a.y, b.y, c.y),
                 max(a.z, b.z, c.z))
        return BoundingVolume(d, e, self)
