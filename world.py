from geometry import *
from copy import copy
from warnings import warn

class KVTree:
    def __init__(self, bvs, axis='x'):
        """ bvs = bounding volumes """
        if len(bvs) <= 16:
            self.volumes = bvs
            return
        threshold = 0.6 * len(bvs)
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
            i += 1
            if len(left) > len(right):
                split -= ( 1 / ( 2 ** i ) )
            else:
                split += ( 1 / ( 2 ** i ) )
            split_pos = ( split * ( max_pos - min_pos ) ) + min_pos
            #print(f, threshold, split, min_pos, max_pos, len(bvs), len(left), len(right), len(both))

        if i == 16:
            warn("Failed to split bvs to a threshold of 0.6")

        next_axis = 'x'
        if axis == 'x':
            next_axis = 'y'
        if axis == 'y':
            next_axis = 'z'

        self.volumes = bvs
        self.left = KVTree(left + both, next_axis)
        self.right = KVTree(right + both, next_axis)
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.split_pos = split_pos

class World:
    def __init__(self, tris):
        self.tris = tris
        self.build_acceleration_structure()

    def build_acceleration_structure(self):
        self.kvtree = KVTree([x.bounding_volume() for x in self.tris])
