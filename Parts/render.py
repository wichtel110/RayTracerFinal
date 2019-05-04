from Parts.ray import Ray
from Parts.color import Color
import numpy as np
import math

class Render(object):

    def __init__(self,camera, bgcolor, maxTraceLevel,objectList,lightList):
        self.camera = camera
        self.bgcolor = bgcolor
        self.maxTraceLevel = maxTraceLevel
        self.objectList = objectList
        self.lightList = lightList

    def startRender(self,traceLevel):
        for y in range(self.camera.hRes):
            for x in range(self.camera.wRes):
                ray = self.camera.calcRay(x, y)
                color = self.traceRay(traceLevel, ray)
                yield (x,y, color)

    def traceRay(self,traceLevel, ray):
        hitPointData = self.intersect(traceLevel,ray)  # maxLevel = maximale Rekursions−Tiefe

        if hitPointData:
            return self.shade(traceLevel, hitPointData)

        return self.bgcolor


    def shade(self, traceLevel, hitPointData):
        directColor = self.computeColor(hitPointData)


        if hitPointData["obj"].material.reflects:
            reflectedRay = self.computeReflectedRay(hitPointData)
            reflectColor = self.traceRay(traceLevel+1, reflectedRay)
        else:
            reflectColor = Color(0,0,0)


        return directColor + reflectColor


    def computeReflectedRay(self,hitPointData):
        interSectionPoint = hitPointData["ray"].pointAtParameter(hitPointData["hitdist"])
        normal = hitPointData["obj"].normalAt(interSectionPoint)
        #d = hitPointData["ray"].direction
        #n = hitPointData["obj"].normalAt(origin)
        #newDirection = d - (n*n.dot(d))*2

        reflectedRay = Ray(interSectionPoint, hitPointData["ray"].reflect(normal))

        return reflectedRay

    def computeColor(self, hitPointData):
        obj = hitPointData["obj"]
        ray = hitPointData["ray"]
        hitdist = hitPointData["hitdist"]

        interSectionPoint = ray.pointAtParameter(hitdist)
        normal = obj.normalAt(interSectionPoint)


        for light in self.lightList:
            lightRay = Ray(interSectionPoint,light.position - interSectionPoint)

            phi = normal.dot(lightRay.direction)
            lightRay_r = lightRay.reflect(normal)

            theta = lightRay_r.dot(-1*ray.direction)

            color = obj.material.calcColor(normal, theta=theta,phi=phi, shaded=self.isInShadow(lightRay))

        return color


    def isInShadow(self,lightRay):

        for obj in self.objectList:
            hit = obj.intersectionParameter(lightRay)
            if hit:
                if hit > 0:
                    return hit
        return 0

    def intersect(self,traceLevel, ray):
        if traceLevel >= self.maxTraceLevel:
            return None

        hitPointData = None
        maxdist = float('inf')

        for shape in self.objectList:
            hitdist = shape.intersectionParameter(ray)
            if hitdist:
                hitdist = math.fabs(hitdist)
                if .0001 < hitdist < maxdist:
                    maxdist = hitdist
                    color = shape.material.getBaseColor()
                    hitPointData = {
                        "obj": shape,
                        "hitdist": hitdist,
                        "color": color,
                        "ray": ray,
                        "reflecting": bool(shape.material.reflects)
                    }

        return hitPointData

    def colorAt(self,ray,shape,hitdist):
        color = shape.getBaseColor()
        factor = 1-(hitdist/100)


        #SHadow True Or not


        newColor = (int(color[0] * factor),int(color[1] * factor),int(color[2] * factor))


        return newColor



