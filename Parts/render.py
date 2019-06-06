from Parts.ray import Ray
from Parts.color import Color

class Render(object):
    def __init__(self, camera, bgcolor, maxTraceLevel, objectList, lightList):
        self.camera = camera
        self.bgcolor = bgcolor
        self.maxTraceLevel = maxTraceLevel
        self.objectList = objectList
        self.lightList = lightList



    def startRender(self, traceLevel):
        for y in range(self.camera.hRes):
            for x in range(self.camera.wRes):
                ray = self.camera.calcRay(x, y)
                color = self.traceRay(traceLevel, ray)
                yield [x, self.camera.hRes - 1 - y, [int(color[0]),int(color[1]),int(color[2])]]


    def traceRay(self, traceLevel, ray):
        hitPointData = self.intersect(traceLevel, ray)  # maxLevel = maximale Rekursions−Tiefe
        if hitPointData:
            return self.shade(traceLevel, hitPointData)
        return self.bgcolor

    def shade(self, traceLevel, hitPointData):
        directColor = self.computeColor(hitPointData,traceLevel)

        reflectColor = Color(0,0,0)
        if hitPointData["obj"].material.reflects:
            reflectedRay = self.computeReflectedRay(hitPointData)
            reflectColor = self.traceRay(traceLevel + 1, reflectedRay)


        return directColor + reflectColor* 0.5


    def computeReflectedRay(self, hitPointData):
        interSectionPoint = hitPointData["ray"].pointAtParameter(hitPointData["hitdist"])
        normal = hitPointData["obj"].normalAt(interSectionPoint)

        return Ray(interSectionPoint, hitPointData["ray"].reflect(normal))

    def computeColor(self, hitPointData, traceLevel):
        obj = hitPointData["obj"]
        ray = hitPointData["ray"]
        hitdist = hitPointData["hitdist"]

        interSectionPoint = ray.pointAtParameter(hitdist)
        normal = obj.normalAt(interSectionPoint)

        for light in self.lightList:
            lightRay = Ray(interSectionPoint, light.position - interSectionPoint)

            phi = normal.dot(lightRay.direction)
            lightRay_r = lightRay.reflect(normal)

            theta = lightRay_r.dot(ray.direction*-1)

            color = obj.material.calcColor(phi=phi, theta=theta, shaded=self.isInShadow(lightRay), p=interSectionPoint, tracelevel=traceLevel)

        return color

    def isInShadow(self, lightRay):

        ### Schatten wird krisselig dargestellt bei hit > 0
        for obj in self.objectList:
            hit = obj.intersectionParameter(lightRay)
            if hit:
                if hit > 0.00001:
                    return True
        return False

    def intersect(self, traceLevel, ray):
        if traceLevel >= self.maxTraceLevel:
            return None

        hitPointData = None
        maxdist = float('inf')

        for shape in self.objectList:
            hitdist = shape.intersectionParameter(ray)
            if hitdist:
                if .0001 < hitdist < maxdist:
                    maxdist = hitdist
                    intersectionPoint = ray.pointAtParameter(hitdist)
                    color = shape.material.getBaseColor(intersectionPoint)
                    hitPointData = {
                        "obj": shape,
                        "hitdist": hitdist,
                        "color": color,
                        "ray": ray,
                        "reflecting": bool(shape.material.reflects)
                    }

        return hitPointData