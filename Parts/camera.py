import numpy as np
import math
from Parts.ray import Ray


class Camera(object):
    def __init__(self,e,c,up,fieldOfView, wRes, hRes):
        self.e = e
        self.c = c
        self.up = up
        self.fieldOfView = fieldOfView
        self.wRes = wRes
        self.hRes = hRes

        ### Koordinatensystem Bestimmen

        self.f = (c-e)/ np.linalg.norm(c-e)
        self.s = np.cross(self.f,up) / np.linalg.norm(np.cross(self.f,up))

        self.u = np.cross(self.s,self.f)

        #Gradmaß in Bogenmaß umrechnen und halbieren
        self.alpha = (fieldOfView/180. * math.pi) / 2.

        self.height = 2 * math.tan(self.alpha)
        self.width = (self.wRes / self.hRes) * self.height

    def calcRay(self,x,y):
        pixelWidth = self.width / self.wRes
        pixelHeight = self.height / self.hRes
        xcomp = self.s * (x * pixelWidth - self.width / 2)
        ycomp = self.u * (y * pixelHeight - self.height / 2)

        return Ray(self.e, self.f + xcomp + ycomp)