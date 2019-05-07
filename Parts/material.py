from Parts.color import Color

class Material(object):

    def __init__(self,color=Color(), ambientFactor=0.8, difuseFactor=0.7, specularFactor=0.2, shadeFactor=0.5, reflects=False):
        self.ambientFactor = ambientFactor
        self.difuseFactor = difuseFactor
        self.specularFactor = specularFactor
        self.shadeFactor = shadeFactor
        self.reflects = reflects
        self.color = color

    def getBaseColor(self,p=None):
        return self.color

    def calcShade(self):
        return self.color * self.shadeFactor


    def calcColor(self, theta, phi, shaded=False, p =None, tracelevel=0 ):
        '''
        Calculating Color
        :param theta:
        :param phi: angel between surfacenormal and lightray
        :param shaded: angel between surfacenormal and reflected lightray
        :param p:
        :return:
        '''
        newColor = self.getBaseColor()* self.ambientFactor
        if shaded:
            return self.calcShade()

        newColor += newColor * self.difuseFactor * phi
        newColor += newColor * self.specularFactor * (theta ** 16)

        return newColor


class CheckboardMaterial(object):

    def __init__(self,reflects=False):
        self.baseColor = Color(255, 255, 255)
        self.otherColor = Color(0, 0, 0)
        self.ambientFactor = 1.0
        self.difuseFactor = 0.6
        self.specularFactor = 0.2
        self.shadeFactor = 0.2
        self.checkSize = 0.7
        self.reflects = reflects

    def getBaseColor(self, p):
        v = p
        v = v / self.checkSize
        if int((int(v[0] + 50.5) + int(v[1] + 0.5) + int(v[2] + 0.5))) % 2:
            return self.otherColor
        return self.baseColor

    def calcShade(self,p):
        return self.getBaseColor(p) * self.shadeFactor

    def calcColor(self, theta, phi, shaded=False, p=None, tracelevel=0):
        newColor = self.getBaseColor(p)
        if shaded and tracelevel == 0:
            return self.calcShade(p)

        newColor = newColor * self.ambientFactor
        if phi > 0:
            newColor += newColor * self.difuseFactor * phi
        newColor += newColor * self.specularFactor * (theta ** 32)

        return newColor