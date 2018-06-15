'''
Created on 6. jun. 2018

@author: Bruger
'''
import math

import numpy as np


class State(object):
    
    imageXCenter = 640 #1280/2
    imageYCenter = 360 #720/2


    maximumCircleRadius = 45
    

    #Do we see the circle or QR-code
    circleSeen = False
    QRCodeSeen = False
    ellipseSeen = False
    
    #When was it that we saw the circle and QR-code last time? Counter for setting circleSeen and QRCodeSeen to false. 
    circleLastSeen = 0
    QRLastSeen = 0
    ellipseLastSeen = 0
    
    #The maximum value for the counter
    counterMaxValue = 25
    
    routineStarted = False
    flownOnce = False
    
    #The circle and QR-code object. 
    mostRecentCircle = None
    mostRecentQR = None
    


    #Circle information
    circleXCoor = 0
    circleYCoor = 0
    circleRadius = 0
    circleArea = 0
    
    
    
    
    #Ellipse information
    ellipseArea = None
    listOfEllipses = []
    oldListOfEllipses = []
    ellipseAreaThreshold = 1                       #Entries in the list before we can determine if the area is bigger. 
    ellipseXCoor = 0
    ellipseYCoor = 0
    ellipseThreshold = 70
    
    #Directions we moved to make ellipse area bigger
    moveLeft = False
    moveRight = False
    moveForward = False
    moveBackwards = False       
    
    
    #difference in coordinates
    centerThreshold = 75
    
    ellipseCircleThreshold = 35
    
    

    # Distance
    distance = None
    
    
    
    #QR information
    dict = ["P.00", "P.01", "P.02", "P.03", "P.04", "P.05", "P.06"]
    indexReached = 0            #Circle number that we've reached. 
    QRdistance = None
    QRdata = None
    circleDiameter = None
    QRxCoor = None
    QRyCoor = None
    
    areaThreshold = 30
    
    













    def __init__(self):
        '''
        Constructor
        '''
        
   
    def printInfo(self): 
        print("DroneState:")
        print("aboveCenter: ", self.aboveCenter)
        print("underCenter: ", self.underCenter)
        print("rightOfCenter: ", self.rightOfCenter)
        print("leftOfCenter: ", self.leftOfCenter)
        
    
    def circleCorrect(self):
        return self.dict[self.indexReached] == self.QRdata
    
    def iterateCircleIndex(self):
        self.indexReached += 1
        
        
        
    def resetCircleCounter(self):
        self.circleLastSeen = self.counterMaxValue
        
    def resetQRCounter(self):
        self.QRLastSeen = self.counterMaxValue
    def resetEllipseCounter(self):
        self.ellipseLastSeen = self.counterMaxValue
    
    def updateCounters(self):
        if self.circleLastSeen == 0:
            self.circleSeen = False
        elif self.circleLastSeen > 0:
            self.circleLastSeen -= 1
        
        if self.QRLastSeen == 0:
            self.QRCodeSeen = False
        elif self.QRLastSeen > 0:
            self.QRLastSeen -= 1
        
        if self.ellipseLastSeen == 0:
            self.ellipseSeen = False
        elif self.ellipseLastSeen > 0:
            self.ellipseLastSeen -= 1
        
    
    
    def areasSimilar(self):
        if self.QRCodeSeen or self.routineStarted:
            return True
        return math.fabs(self.circleXCoor-self.ellipseXCoor) < self.ellipseCircleThreshold and math.fabs(self.circleYCoor-self.ellipseYCoor) < self.ellipseCircleThreshold
            
    def droneCentered(self):
        if self.routineStarted:
            return True

        if math.fabs(self.imageXCenter-self.circleXCoor*2) < self.centerThreshold:
            if math.fabs(self.imageYCenter-self.circleYCoor*2) < self.centerThreshold:
                return True
        return False
    
    def droneCenteredWithEllipse(self):
        return math.fabs(self.ellipseXCoor*2 - self.imageXCenter) < self.ellipseThreshold
        #math.fabs(self.ellipseYCoor - self.imageYCenter) < self.ellipseThreshold and 
            
    def printCenters(self):
        print "ImageYCenter: ", self.imageYCenter, " imageXCenter: ", self.imageXCenter
        print "CircleYCenter: ", self.circleYCoor, " CircleXCenter: ", self.circleXCoor
        print "EllipseYCenter: ", self.ellipseYCoor, " EllipseXCoor: ", self.ellipseXCoor
        print "AreaSimilar: ", self.areasSimilar(), " circleArea/ellipseArea: ", self.circleArea/self.ellipseArea,  "\n"
    
    def droneAboveCenter(self):
        return math.fabs(self.imageYCenter - self.circleYCoor*2) > self.centerThreshold and self.imageYCenter < self.circleYCoor*2
    def droneUnderCenter(self):
        return math.fabs(self.imageYCenter - self.circleYCoor*2) > self.centerThreshold and self.imageYCenter > self.circleYCoor*2
    def droneRightOfCenter(self):
        return math.fabs(self.imageXCenter - self.circleXCoor*2) > self.centerThreshold and self.imageXCenter > self.circleXCoor*2
    def droneLeftOfCenter(self):
        return math.fabs(self.imageXCenter - self.circleXCoor*2) > self.centerThreshold and self.imageXCenter < self.circleXCoor*2
        
    
    def droneLeftOfEllipse(self):
        return math.fabs(self.imageXCenter - self.ellipseXCoor*2) > self.ellipseThreshold and self.imageXCenter < self.ellipseXCoor*2
    def droneRightOfEllipse(self):
        return math.fabs(self.imageXCenter - self.ellipseXCoor*2) > self.ellipseThreshold and self.imageXCenter > self.ellipseXCoor*2
    def droneAboveEllipse(self):
        return math.fabs(self.imageYCenter - self.ellipseYCoor*2) > self.ellipseThreshold and self.imageYCenter > self.ellipseYCoor*2
    def droneUnderEllipse(self):
        return math.fabs(self.imageYCenter - self.ellipseYCoor*2) > self.ellipseThreshold and self.imageYCenter < self.ellipseYCoor*2
    
    def circleDiameterEqualToHeight(self):
        return math.fabs(self.circleRadius - self.circleYCoor) < self.maximumCircleRadius or math.fabs(self.circleRadius - self.circleXCoor) < self.maximumCircleRadius
    
    
    
    def addEllipseArea(self, area):
        self.listOfEllipses.append(area)
    
    
    def ellipseAreaGettingBigger(self):
        
        if len(self.listOfEllipses) > 30:
            if np.mean(self.listOfEllipses) > np.mean(self.oldListOfEllipses):
                self.oldListOfEllipses = self.listOfEllipses
                self.listOfEllipses = []
                return True
            else:
                return False
        return None
                
    def resetCircleInfo(self):
      self.circleSeen = False  
    
    
    
    
    
    
    
    
    
        