import numpy as np

class Plane(object):
    def __init__(self, point, normal,material):
        self.point = point  # point
        self.normal = normal / np.linalg.norm(normal)  # vector
        self.material = material

    def __repr__(self):
        return 'Plane( % s, % s)' % (repr(self.point), repr(self.normal))


    def intersectionParameter(self, ray):
        op = ray.origin - self.point #Richtung von Ursprung des Rays zum Punkt
        a = np.dot(op,self.normal)
        b = np.dot(ray.direction,self.normal)
        if b < 0:
            return -a / b
        else:
            return None


    def normalAt(self, p):
        return self.normal

    def getMaterialReflection(self):
        return self.material.reflects

    def getBaseColor(self):
        return self.material.getBaseColor()