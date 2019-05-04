from Parts.color import Color

class Material(object):

    def __init__(self,color =Color(), ambientFactor=0.9, difuseFactor=0.5, specularFactor=0.5, shadeFactor= 0.95, reflects=False):
        self.ambientFactor = ambientFactor
        self.difuseFactor = difuseFactor
        self.specularFactor = specularFactor
        self.shadeFactor = shadeFactor
        self.reflects = reflects
        self.color = color

    def getBaseColor(self):
        return self.color

    def calcShade(self):
        return self.color * self.shadeFactor


    def calcColor(self, theta, phi, shaded=False ):
        newColor = self.color
        if shaded:
            return self.calcShade()

        newColor = newColor * self.ambientFactor
        if phi > 0:
            newColor += newColor * self.difuseFactor * phi
        newColor += newColor * self.specularFactor * (theta ** 32)

        return newColor