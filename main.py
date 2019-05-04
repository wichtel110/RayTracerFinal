import numpy as np
from PIL import Image
from Parts.camera import Camera
from Parts.render import Render
from Objects.sphere import Sphere
from Objects.plane import Plane
from Objects.triangle import Triangle
from Objects.light import Light
from Parts.material import Material

from Parts.color import Color
#
# Grundlegendes (Bildgröße usw)
#
HEIGHT = 400
WIDTH = 400


#
# Camera Einstellungen
#

E = np.array([0,1.8,10])
UP = np.array([0,1,0])
C = np.array([0,3,0])
FIELDOFVIEW = 45


### Render Setting

STARTLEVEL = 0
MAXLEVEL = 3


###
BGCOLOR = Color(0,0,0)
redMat = Material(color=Color(230,40,0),reflects=True)
blueMat = Material(color=Color(0,40,230),reflects=True)
greenMat = Material(color=Color(40, 230, 0),reflects=True)
yellowMat = Material(color=Color(255, 255, 0))
greyMat = Material(color=Color(100,100,100))



###
objList =[
    Plane(np.array([0,0,0]), np.array([0,-1,0]),material=greyMat ),
    Triangle(np.array([0, 1.5, 3.7]), np.array([1, 3, 3.7]), np.array([-1, 3, 3.7]), material=yellowMat),
    Sphere(np.array([0,1.2,4]),0.7,material=redMat),
    Sphere(np.array([-0.8,3,4]),0.7,material=blueMat),
    Sphere(np.array([0.8, 3, 4]), 0.7,material=greenMat)
]

lightList =[
    Light(np.array([30, -30, 30]))
]






color1 = Color(255,0,0)
color2 = Color(20,250,0)

print(color1 + color2)
print(color1 - color2)
print(color2 * 0.2)



if __name__ == '__main__':
    camera = Camera(E,C,UP,FIELDOFVIEW,WIDTH,HEIGHT)
    render = Render(camera,BGCOLOR,maxTraceLevel=MAXLEVEL,objectList=objList,lightList=lightList)

    im = Image.new("RGB", (WIDTH, HEIGHT), (0,0,123))
    pix = im.load()

    pictureGen = render.startRender(traceLevel=STARTLEVEL)


    for pixel in pictureGen:
        #0 = x
        #1 = y
        #2 = color
        im.putpixel((pixel[0], pixel[1]), (int(pixel[2][0]),int(pixel[2][1]),int(pixel[2][2])))


    im.save("test2.png", "PNG")