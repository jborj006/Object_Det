#import cv2
import numpy as np

class Object:

    def __init__(self, name = None ):
        self._xPos = 0 #all private initializations 
        self._yPos = 0
        self._type = None
        self._HSVmin = np.array([0, 0, 0])
        self._HSVmax = np.array([0, 0, 0])
        self._Color = np.array([0, 0, 0])

        if name == None: #Object()
            self.setType('Object')
            self.setColor(np.array([0, 0, 0]))
        else:#Object(name)
            if name == 'blue':
                #using HSV
                self.setHSVmin(np.array([92,0,0]))
                self.setHSVmax(np.array([124,256,256]))

                #using BGR
                self.setColor(np.array([255,0,0]))
            elif name == 'green':
                #using HSV
                self.setHSVmin(np.array([34, 50, 50]))
                self.setHSVmax(np.array([80, 220, 200]))

                #using BGR
                self.setColor(np.array([0, 255, 0]))
            elif name == 'yellow':
                #using HSV
                self.setHSVmin(np.array([20, 124, 123]))
                self.setHSVmax(np.array([30, 256, 256]))

                #using BGR
                self.setColor(np.array([0, 255, 255]))
            elif name == 'red':
                #using HSV
                self.setHSVmin(np.array([0, 200, 0]))
                self.setHSVmax(np.array([19, 255, 255]))

                #using BGR
                self.setColor(np.array([0, 0, 255]))


    def getXPos(self):
        return self.xPos

    def setXPos(self, x):
        self.xPos = x
        return

    def getYPos(self):
        return self.yPos

    def setYPos(self, y):
        self.yPos = y
        return

    def getHSVmin(self):
        return self._HSVmin

    def getHSVmax(self):
        return self._HSVmax

    def setHSVmin(self, min_):
        self._HSVmin = min_

    def setHSVmax(self, max_):
        self._HSVmax = max_

    def getColor(self):
        return self._Color

    def setColor(self, c):
        self._Color = c

    def getType(self):
        return self._type

    def setType(self, t):
        self._type = t
        
        
# if __name__ == "__main__":
#     o = Object()
#     print o.getColor()
#     o = Object('blue')
#     print o.getColor()
    
