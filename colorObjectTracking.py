import cv2
import numpy as np
import argparse
import Header
#Using OpenCV Version 3.3.1

#max and min for HSV
H_MIN = 0
H_MAX = 256
S_MIN = 0
S_MAX = 256
V_MIN = 0
V_MAX = 256

#default capture for width and height
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

#number of objects detected in a frame
MAX_NUM_OBJECTS = 50

#min and max object area
MIN_OBJECT_AREA = 20*20
MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH/1.5

#names for each window
windowName1 = "Original"
windowName2 = "HSV"
windowName3 = "Threshold"
windowName4 = "After Morph Changes"

#setup for canny edge detector
lowThreshold = 0
max_lowThreshold = 100
window_name = 'Edge Map'
title_trackbar = 'Min Threshold:'
ratio = 3
kernel_size = 3

#called when a trackbar is changed
def nothing(val):
    pass

# NOT NEEDED
#def intToString(number):

#Create the Trackbars
def createTrackbars():
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("H_MIN", "Trackbars", H_MIN, H_MAX, nothing)
    cv2.createTrackbar("H_MAX", "Trackbars", H_MAX, H_MAX, nothing)
    cv2.createTrackbar("S_MIN", "Trackbars", S_MIN, S_MAX, nothing)
    cv2.createTrackbar("S_MAX", "Trackbars", S_MAX, S_MAX, nothing)
    cv2.createTrackbar("V_MIN", "Trackbars", V_MIN, V_MAX, nothing)
    cv2.createTrackbar("V_MAX", "Trackbars", V_MAX, V_MAX, nothing)


def drawObject(theObjects, frame, temp, contours, hierarchy):  
    
    for i in range(0,len(theObjects)):
        cv2.drawContours(frame, contours, i, theObjects[i].getColor(), 3, 8, hierarchy)
        cv2.circle(frame,(theObjects[i].getXPos(),theObjects[i].getXPos()), 5, theObjects[i].getColor())
        cv2.putText(frame, str(theObjects[i].getXPos()) + " , " + str(theObjects[i].getYPos()), (theObjects[i].getXPos(),theObjects[i].getXPos() + 20), 1, 1, theObjects[i].getColor())
        cv2.putText(frame, theObjects[i].getType(), (theObjects[i].getXPos(),theObjects[i].getXPos() - 20), 1, 2, theObjects[i].getColor())

def drawObject(theObjects, frame):
        for i in range(0,len(theObjects)):
                cv2.circle(frame, (theObjects[i].getXPos(),theObjects[i].getXPos()), 10, (0,0,255))
                cv2.putText(frame, str(theObjects[i].getXPos()) + " , " + str(theObjects[i].getYPos()), (theObjects[i].getXPos(),theObjects[i].getXPos() + 20), 1, 1, (0, 255, 0))                
                cv2.putText(frame, theObjects[i].getType(), (theObjects[i].getXPos(),theObjects[i].getXPos() - 30), 1, 2, theObjects[i].getColor())

def morphImage(thresh):
        erosion_type = cv2.MORPH_RECT
        dilatation_type = cv2.MORPH_RECT
        erosion_element = cv2.getStructuringElement(erosion_type, (3,3) )
        dilatation_element = cv2.getStructuringElement(dilatation_type, (8,8))
        cv2.erode(thresh, thresh, erosion_element)
        cv2.erode(thresh, thresh, erosion_element)
        cv2.dilate(thresh, thresh, dilatation_element)
        cv2.dilate(thresh, thresh, dilatation_element)

def trackFilteredObject(threshold, HSV, cameraFeed, theObject = None):
        objects = []
        #temp = np.zeros(threshold.shape, np.uint8)
        temp = threshold.copy()
        contours = []
        hierarchy = []
        _,contours, hierarchy = cv2.findContours(temp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE, contours, hierarchy)

        refArea = 0
        objectFound = False

        if(len(hierarchy) > 0):
                numObjects = len(hierarchy)

        if(numObjects < MAX_NUM_OBJECTS):
                index = 0
                while index >=0:
                        moment = cv2.moments(contours[index])
                        area = moment['m00'] #access the value of the key m00

                        if(area > MIN_OBJECT_AREA):
                                object = Header.Object()
                                object.setXPos(moment['m10'] / area)
                                object.setXPos(moment['m01'] / area)

                                if(theObject):
                                        object.setType(theObject.getType())
                                        object.setColor(theObject.getColor())

                                objects.append(object)
                                objectFound = True
                        else:
                                objectFound = False
                        index = hierarchy[0][index][0]
                
                if(objectFound == True):
                        drawObject(objects, cameraFeed)
                
        else:
                cv2.putText(cameraFeed,"Too Noisy! Fix this", (0, 50), 1, 2, (0, 0, 255), 2)

if __name__ == '__main__':
    
        """Start the Camera"""
        cap = cv2.VideoCapture(0)
        calibrationMode = True

        if (calibrationMode):
                createTrackbars()

        while True:
                _, cameraFeed = cap.read()
                HSV = cv2.cvtColor(cameraFeed, cv2.COLOR_BGR2HSV)

                if (calibrationMode == True):
                        HSV = cv2.cvtColor(cameraFeed, cv2.COLOR_BGR2HSV)
                        threshold = cv2.inRange(HSV, (0, 0, 0), (179, 255, 255))
                        cv2.namedWindow(window_name,  cv2.CV_WINDOW_AUTOSIZE)
                        cv2.createTrackbar("Min Threshold", window_name, lowThreshold, max_lowThreshold, nothing)
                        trackFilteredObject(threshold, HSV, cameraFeed)
                else:
                        blue, yellow, red, green = Header.Object("blue", "yellow", "red", "green")

                        theList = [blue, yellow, red, green]
                        
                        for obj in theList:
                                HSV = cv2.cvtColor(cameraFeed, cv2.COLOR_BGR2HSV)
                                threshold = cv2.inRange(HSV, obj.getHSVmin(), obj.getHSVmax())
                                morphImage(threshold)
                                trackFilteredObject(obj, threshold, HSV, cameraFeed)
                
                cv2.imshow(windowName1, cameraFeed)
                key = cv2.waitKey(30) #wait one second
                if key == 27:            #the 'esc' key
                        break

        """Destroy all windows when 'esc' is pressed"""
        cap.release()
        cv2.destroyAllWindows()


"""def example():
        a,b = 0,0
        if a == 0:
                b = 0
        else:
                b = 1
        b"""














"""Point o1,o2;
listofpoints = [o1,o2] #vector<Points>
listofpoints[0]
listoflist = [theObjects]#vector<vector<Point>>
drawObject(theObjects,)"""