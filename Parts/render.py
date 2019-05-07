from Parts.ray import Ray
from Parts.color import Color
from PIL import Image
from threading import Thread

image = Image.new("RGB", (500, 500), (0, 0, 0))


class Render(object):



    def __init__(self, camera, bgcolor, maxTraceLevel, objectList, lightList):
        self.camera = camera
        self.bgcolor = bgcolor
        self.maxTraceLevel = maxTraceLevel
        self.objectList = objectList
        self.lightList = lightList


    def preRender(self,tracelevel):

        # Create all Slice
        sli = []
        threadList = []
        for x in range(0,self.camera.wRes,100):
            sli.append(x)

        # Create Threads
        for parts in sli:
            threadList.append(Thread(target=self.startRender, args=(tracelevel,parts,parts+100)))

        # Start threads
        for thread in threadList:
            thread.start()

        # Join threads
        for thread in threadList:
            thread.join()


        from datetime import datetime
        image.save("{}.png".format(datetime.now()), "PNG")



    def startRender(self, traceLevel,start,end):

        for y in range(start, end):
            for x in range(self.camera.wRes):
                ray = self.camera.calcRay(x, y)
                color = self.traceRay(traceLevel, ray)
                image.putpixel((x, y), (int(color[0]),int(color[1]),int(color[2])))

        #from datetime import datetime
        #image.save("{}.png".format(datetime.now()), "PNG")


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


        return directColor + reflectColor


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