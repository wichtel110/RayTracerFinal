'''

'''

import numpy as np
from PIL import Image
from Parts.camera import Camera
from Parts.render import Render
from Objects.sphere import Sphere
from Objects.plane import Plane
from Objects.triangle import Triangle
from Objects.light import Light
from Parts.material import Material,CheckboardMaterial
from Parts.color import Color

from threading import Thread

'''
Settings For Camera, Materials etc.
'''

#
# Grundlegendes (Bildgröße usw)
#
HEIGHT = 200
WIDTH = 200

#
# Camera Einstellungen
#

E = np.array([0,1.8,10])
UP = np.array([0,1,0])
C = np.array([0,3,0])
FIELDOFVIEW = 45


### Render Setting

STARTLEVEL = 0
MAXLEVEL = 2


### Material and Color

BGCOLOR = Color(0,0,0)
redMat = Material(color=Color(200,0,0),reflects=True)
blueMat = Material(color=Color(0,0,200),reflects=True)
greenMat = Material(color=Color(0, 200, 0),reflects=True)
yellowMat = Material(color=Color(255, 255, 0))
greyMat = Material(color=Color(100,100,100))

checkBoard = CheckboardMaterial()

### Objects
objList =[
    Triangle(np.array([0, 4, .1]), np.array([1.5, 1.5,.1]), np.array([-1.5, 1.5, .1]), material=yellowMat),
    Sphere(np.array([0, 4.25,.5]),1,material=redMat),
    Sphere(np.array([-1.5,1.75, .5]),1,material=blueMat),
    Sphere(np.array([1.5, 1.75, .5]), 1,material=greenMat),
    Plane(np.array([0,0,0]), np.array([0,1,0]),material=checkBoard)
]

### Lights
lightList =[
    Light(np.array([30, 30, 10]))
]

if __name__ == '__main__':
    camera = Camera(E,C,UP,FIELDOFVIEW,WIDTH,HEIGHT)
    render = Render(camera,BGCOLOR,maxTraceLevel=MAXLEVEL,objectList=objList,lightList=lightList)


    render.startRender(STARTLEVEL)

    im = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    pictureGen = render.startRender(traceLevel=STARTLEVEL)



    for pixel in pictureGen:
        '''
        0: x
        1: y
        2: r,g,b
        '''
        im.putpixel((pixel[0], pixel[1]), (int(pixel[2][0]),int(pixel[2][1]),int(pixel[2][2])))


    from datetime import datetime
    im.save("{}.png".format(datetime.now()), "PNG")