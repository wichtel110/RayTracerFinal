import math
import numpy as np


class Sphere(object):
    def __init__(self,center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def __repr__(self):
        return 'Sphere( % s, % s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v*v - co.dot(co) + self.radius * self.radius

        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self,p):
        return (p-self.center)/ np.linalg.norm(p-self.center)

    def getMaterialReflection(self):
        return self.material.reflects

    def getBaseColor(self):
        return self.material.getBaseColor()