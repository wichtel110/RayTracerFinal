import numpy as np

class Ray(object):

    def __init__(self,origin, direction):
        self.origin = origin #Point
        self.direction = direction / np.linalg.norm(direction) #Vector normalisiert

    def __repr__(self):
        return 'Ray( % s, % s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self,t):
        return self.origin + self.direction * t

    def reflect(self,n):
        n = n / np.linalg.norm(n)
        return self.direction - (n*n.dot(self.direction))*2