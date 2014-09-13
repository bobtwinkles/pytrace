import math
from geometry import Vec3

class Vertex:
    def __init__(self, pos, normal):
        if not isinstance(pos, Vec3):
            raise TypeError("pos must be a Vec3")
        if not isinstance(normal, Vec3):
            raise TypeError("normal must be a vec3")
