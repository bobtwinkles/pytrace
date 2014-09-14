import numbers
import collections

class Color:
    # Color format constants
    RGB = 1
    HSV = 2
    namemap = {RGB: "RGB"
              ,HSV: "HSV"}

    def __init__(self, color, fmt=RGB):
        if not isinstance(color, collections.Sequence):
            raise TypeError("color must be a Sequence")
        if len(color) != 3:
            raise ValueError("Length of Color must be 3")
        if fmt == Color.RGB:
            if isinstance(color[0], numbers.Integral):
                color = [x / 256 for x in color]
            r, g, b = color
            self.r = r
            self.g = g
            self.b = b
        else:
            if fmt in namemap:
                raise NotImplementedError("Format type {0}".format(namemap[fmt]))
            else:
                raise NotImplementedError("Format type {0} completely unknown".format(fmt))

    def __str__(self):
        return "<Color: {r} {g} {b}>".format(**self.__dict__)
