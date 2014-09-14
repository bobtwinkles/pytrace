import abc
from color import Color

class Material(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def computeColor(position, normal, origination_position, world):
        """
        Compute the color of a surface at position with normal normal being hit by a
        camera ray originating at origination_position in the world"""
        pass

class BSDF(Material):
    def __init__(self, color):
        self.color = color

    def computeColor(position, normal, incidence, world):
        return self.color
