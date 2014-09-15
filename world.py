from geometry import *
from copy import copy
from warnings import warn

class KVTree:
    LEAF = 0
    NODE = 1

    def __init__(self, bvs, axis='x', parent=None):
        """ bvs = bounding volumes """
        # print('init')
        self.parent = parent
        self.axis = axis
        self.volumes = bvs
        self.left = None
        self.right = None
        self.min_pos = None
        self.max_pos = None
        self.split_pos = None
        self.mode = self.LEAF

        # TODO: integrate this with the min_pos/max_pos search
        vecs = []
        for x in self.volumes:
            vecs.append(x.a)
            vecs.append(x.b)
        self.minvec, self.maxvec = get_min_max_vec3(vecs)
        self.bv = BoundingVolume(self.minvec, self.maxvec, self)

        if len(bvs) <= 16:
            return

        threshold = 0.5 * len(bvs)
        min_pos = bvs[0].a.__getattribute__(axis)
        max_pos = bvs[0].a.__getattribute__(axis)
        pairs = []
        for i in range(len(bvs)):
            bv = bvs[i]
            bv_pair = (bv.a.__getattribute__(axis), bv.b.__getattribute__(axis))
            if bv_pair[0] < min_pos:
                min_pos = bv_pair[0]
            elif bv_pair[1] > max_pos:
                max_pos = bv_pair[1]
            pairs.append((bv_pair[0], bv_pair[1], bv))

        split = 0.5
        split_pos = ( split * (max_pos - min_pos) ) + min_pos
        f = len(bvs)
        left = []
        right = []
        both = []
        i = 1
        while f > threshold and i < 16:
            # TODO: Be more intellegent about how we clear/append to these lists
            left.clear()
            right.clear()
            both.clear()
            for pair in pairs:
                if pair[1] < split_pos:
                    left.append(pair[2])
                elif pair[0] > split_pos:
                    right.append(pair[2])
                else:
                    both.append(pair[2])

            f = abs(len(left) - len(right)) + len(both)

            # print(f, threshold, split, len(bvs), len(left), len(both), len(right))
            if len(left) + len(right) + len(both) != len(bvs):
                raise RuntimeError("Somehow the total number of things we have in left,right,both is {0} when it should be {1}".format(\
                        len(left) + len(right) + len(both), len(bvs)))

            if f <= threshold:
                break;
            i += 1
            if len(left) > len(right):
                split -= ( 1 / ( 2 ** i ) )
            else:
                split += ( 1 / ( 2 ** i ) )
            split_pos = ( split * ( max_pos - min_pos ) ) + min_pos

        if i == 16:
            warn("Failed to split bvs to a threshold of 0.5")

        next_axis = 'x'
        if axis == 'x':
            next_axis = 'y'
        if axis == 'y':
            next_axis = 'z'

        # print('left')
        self.left = KVTree(left + both, next_axis, self)
        # print('right')
        self.right = KVTree(right + both, next_axis, self)
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.split_pos = split_pos
        self.mode = self.NODE

    def render_debug_wavefront_mesh(self, fname):
        import os
        try:
            os.remove(fname)
        except:
            pass
        f = open(fname, 'w')
        f.write("# debug mesh for KVTree\n")
        f.write("g DebugMesh\n")
        self._print_data(f)

    def _print_data(self, f, current_index=1):
        minvec, maxvec = self.minvec, self.maxvec

        f.write("o DebugMesh.{0}\n".format(current_index))
        f.write("v {0} {1} {2}\n".format(minvec.x, minvec.y, minvec.z)) # iii
        f.write("v {0} {1} {2}\n".format(minvec.x, minvec.y, maxvec.z)) # iia
        f.write("v {0} {1} {2}\n".format(minvec.x, maxvec.y, minvec.z)) # iai
        f.write("v {0} {1} {2}\n".format(minvec.x, maxvec.y, maxvec.z)) # iaa
        f.write("v {0} {1} {2}\n".format(maxvec.x, minvec.y, minvec.z)) # aii
        f.write("v {0} {1} {2}\n".format(maxvec.x, minvec.y, maxvec.z)) # aia
        f.write("v {0} {1} {2}\n".format(maxvec.x, maxvec.y, minvec.z)) # aai
        f.write("v {0} {1} {2}\n".format(maxvec.x, maxvec.y, maxvec.z)) # aaa
        f.write("f {0} {1} {2} {3}\n".format(current_index + 0, current_index + 1, current_index + 3, current_index + 2))
        f.write("f {0} {1} {2} {3}\n".format(current_index + 4, current_index + 5, current_index + 7, current_index + 6))
        f.write("f {0} {1} {2} {3}\n".format(current_index + 1, current_index + 3, current_index + 7, current_index + 5))
        f.write("f {0} {1} {2} {3}\n".format(current_index + 0, current_index + 2, current_index + 6, current_index + 4))
        f.write("f {0} {1} {2} {3}\n".format(current_index + 0, current_index + 1, current_index + 5, current_index + 4))
        f.write("f {0} {1} {2} {3}\n".format(current_index + 2, current_index + 3, current_index + 7, current_index + 6))
        current_index += 8

        if self.left is None or self.right is None:
            return current_index

        current_index = self.left._print_data(f, current_index)
        current_index = self.right._print_data(f, current_index)
        return current_index

    def compute_intersection(self, ray_pos, ray_dir):
        # three cases:
        # ray is inside already
        # ray is outside heading in
        # ray does not intersect
        print(self.bv, ray_pos, ray_dir)
        dx0, dy0, dz0 = float('inf'), float('inf'), float('inf')
        dx1, dy1, dz1 = float('inf'), float('inf'), float('inf')
        tmin = 0
        tmax = 0
        if ray_dir.x != 0:
            dx0 = (self.bv.a.x - ray_pos.x) / ray_dir.x
            dx1 = (self.bv.b.x - ray_pos.x) / ray_dir.x
        if ray_dir.y != 0:
            dy0 = (self.bv.a.y - ray_pos.y) / ray_dir.y
            dy1 = (self.bv.b.y - ray_pos.y) / ray_dir.y
        if ray_dir.z != 0:
            dz0 = (self.bv.a.z - ray_pos.z) / ray_dir.z
            dy1 = (self.bv.b.y - ray_pos.y) / ray_dir.y
        tmin = max([x for x in [min(dx0, dx1), min(dy0, dy1), min(dz0, dz1)] if x != float('inf')])
        if ray_dir.x != 0:
            dx0, dx1 = -dx0, -dx1
        if ray_dir.y != 0:
            dy0, dy1 = -dy0, -dy1
        if ray_dir.z != 0:
            dz0, dz1 = -dz0, -dz1
        tmax = min(max(dx0, dx1), max(dy0, dy1), max(dz0, dz1))

        if tmax < 0:
            return float('-inf'), float('inf')
        if tmin > tmax:
            return float('-inf'), float('inf')
        return (tmin, tmax)


class World:
    def __init__(self, tris):
        self.tris = tris
        self.build_acceleration_structure()

    def build_acceleration_structure(self):
        self.kvtree = KVTree([x.bounding_volume() for x in self.tris])

    def trace_ray(self, pos, direction):
        t_min, t_max = self.kvtree.compute_intersection(pos, direction)
        print(t_min, t_max)
        self._search_node(self.kvtree, pos, direction, t_min, t_max)
        print(t_min, t_max)
