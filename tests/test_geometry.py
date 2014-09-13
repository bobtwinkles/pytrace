from geometry import *

import unittest
import math

class TestVec3(unittest.TestCase):
    def test_eq(self):
        a = Vec3(0, 0, 0)
        b = Vec3(0, 0, 0)
        c = Vec3(0, 0, 1)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_div(self):
        a = Vec3(1, 1, 1)
        b = Vec3(0.5, 0.5, 0.5)
        self.assertEqual(a / int(2), b)
        self.assertEqual(a / float(2), b)

    def test_mul(self):
        a = Vec3(1, 1, 1)
        b = Vec3(0.5, 0.5, 0.5)
        self.assertEqual(b * int(2)  , a)
        self.assertEqual(b * float(2), a)

    def test_add(self):
        a = Vec3(1, 1, 1)
        b = Vec3(2, 2, 2)
        c = Vec3(3, 3, 3)
        self.assertEqual(a + a, b)
        self.assertEqual(a + b, c)

    def test_subtract(self):
        a = Vec3(1, 1, 1)
        b = Vec3(2, 2, 2)
        c = Vec3(3, 3, 3)
        self.assertEqual(c - a, b)
        self.assertEqual(b - a, a)

    def test_mag(self):
        a = Vec3(1, 2, 3)
        self.assertEqual(a.mag2(), 1 + 4 + 9)
        self.assertEqual(a.mag(), math.sqrt(14))

    def test_cross(self):
        i = Vec3(1, 0, 0)
        j = Vec3(0, 1, 0)
        k = Vec3(0, 0, 1)
        self.assertEqual(k.cross(i), j)
        self.assertEqual(i.cross(k), -j)
        self.assertEqual(i.cross(j), k)
        self.assertEqual(j.cross(i), -k)
        self.assertEqual(j.cross(k), i)
        self.assertEqual(k.cross(j), -i)

    def test_dot(self):
        i = Vec3(1, 0, 0)
        j = Vec3(0, 1, 0)
        k = Vec3(0, 0, 1)
        b = Vec3(1, 2, 3)
        a = Vec3(3, 2, 1)
        self.assertEqual(i.dot(b), 1)
        self.assertEqual(b.dot(i), 1)
        self.assertEqual(b.dot(b), b.mag2())
        self.assertEqual(a.dot(b), 3 + 4 + 3)

class TestBoundingVolue(unittest.TestCase):
    def setUp(self):
        self.unit = BoundingVolume(Vec3(0, 0, 0), Vec3(1, 1, 1))

    def test_eq(self):
        a = BoundingVolume(Vec3(0, 0, 0), Vec3(1, 1, 1))
        b = BoundingVolume(Vec3(1, 1, 1), Vec3(0, 0, 0))
        self.assertTrue(a == b)

    def test_lwh(self):
        self.assertEqual(self.unit.width, 1)
        self.assertEqual(self.unit.height, 1)
        self.assertEqual(self.unit.depth, 1)

    def test_contains(self):
        self.assertTrue(self.unit.contains(Vec3(0.5, 0.5, 0.5)))

if __name__ == "__main__":
    unittest.main()
