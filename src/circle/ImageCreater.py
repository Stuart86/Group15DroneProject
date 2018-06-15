'''
Created on 12. jun. 2018

@author: lasse
'''
import numpy as np
import cv2
from cv2 import imshow
from _tkinter import create
if __name__ == '__main__':
    pass

class ImageCreater:
    
    width = 1280
    height = 720
    color = [255,0,0]
    
    ellipseX = 0
    ellipseY = 0
    ellipseFirstAxis = 0
    ellipseSecondAxis = 0
    ellipseAngle = 0
    ellipseStartAngle = 0
    ellipseEndAngle = 0
    ellipseRed = 0
    ellipseBlue = 0
    ellipseGreen = 0
    ellipseLineThickness = 5
    
    trackbarName = 'EllipseVariables'
    ellipseXName = 'XCoor'
    ellipseYName = 'YCoor'
    ellipseFirstAxisName = 'MainAxis'
    ellipseSecondAxisName = 'SubAxis'
    ellipseAngleName = 'Angle'
    ellipseStartAngleName = 'StartAngle'
    ellipseEndAngleName = 'EndAngle'
    ellipseRedName = 'Red'
    ellipseBlueName = 'Blue'
    ellipseGreenName = 'Green'
    ellipseLineThicknessName = 'Line'

    
    img = np.zeros((height,width,3), np.uint8)
    
    def drawEllipse(self):
        img = np.zeros((self.height,self.width,3), np.uint8)

        center = (int(self.ellipseX),int(self.ellipseY))
        axes = (int(self.ellipseFirstAxis), int(self.ellipseSecondAxis))
        color = (self.ellipseBlue,self.ellipseGreen,self.ellipseRed)

        cv2.ellipse(img, center, axes, self.ellipseAngle, self.ellipseStartAngle , self.ellipseEndAngle, color, self.ellipseLineThickness)
        imshow("Ellipse", img)
        return img
    
    
    
    def createTrackbars(self):
        pass
        
    def updateTrackbarValues(self):
        self.ellipseX = cv2.getTrackbarPos(self.ellipseXName,self.trackbarName)
        self.ellipseY = cv2.getTrackbarPos(self.ellipseYName,self.trackbarName)
        self.ellipseFirstAxis = cv2.getTrackbarPos(self.ellipseFirstAxisName,self.trackbarName)
        self.ellipseSecondAxis = cv2.getTrackbarPos(self.ellipseSecondAxisName,self.trackbarName)
        self.ellipseAngle = cv2.getTrackbarPos(self.ellipseAngleName,self.trackbarName)
        self.ellipseStartAngle = cv2.getTrackbarPos(self.ellipseStartAngleName,self.trackbarName)
        self.ellipseEndAngle = cv2.getTrackbarPos(self.ellipseEndAngleName,self.trackbarName)
        self.ellipseRed = cv2.getTrackbarPos(self.ellipseRedName,self.trackbarName)
        self.ellipseBlue = cv2.getTrackbarPos(self.ellipseBlueName,self.trackbarName)
        self.ellipseGreen = cv2.getTrackbarPos(self.ellipseGreenName,self.trackbarName)
        self.ellipseLineThickness = cv2.getTrackbarPos(self.ellipseLineThicknessName,self.trackbarName)
    
    def onChange(self):
        pass
    
    cv2.namedWindow(trackbarName)
    cv2.resizeWindow(trackbarName,780,780)
    cv2.createTrackbar(ellipseXName,trackbarName,0,width-1, onChange)
    cv2.createTrackbar(ellipseYName,trackbarName,0,height-1, onChange)
    cv2.createTrackbar(ellipseFirstAxisName,trackbarName,0,1000, onChange)
    cv2.createTrackbar(ellipseSecondAxisName,trackbarName,0,1000, onChange)
    cv2.createTrackbar(ellipseAngleName,trackbarName,0,360, onChange)
    cv2.createTrackbar(ellipseStartAngleName,trackbarName,0,360, onChange)
    cv2.createTrackbar(ellipseEndAngleName,trackbarName,0,360, onChange)
    cv2.createTrackbar(ellipseRedName,trackbarName,0,255, onChange)
    cv2.createTrackbar(ellipseBlueName,trackbarName,0,255, onChange)
    cv2.createTrackbar(ellipseGreenName,trackbarName,0,255, onChange)
    cv2.createTrackbar(ellipseLineThicknessName,trackbarName,0,255, onChange)
    
    def main(self):
        
    
        
        while True:
            self.updateTrackbarValues()
            self.drawEllipse()
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()     
    
    

imageCreater = ImageCreater()
imageCreater.main()        
    
    
