'''
Created on 6. jun. 2018

@author: Bruger
'''
import math
import numpy as np


class State(object):
    
    imageXCenter = 640 #1280/2
    imageYCenter = 360 #720/2

    #Do we see the circle or QR-code
    circleSeen = False
    QRCodeSeen = False
    ellipseSeen = False
    
    #When was it that we saw the circle and QR-code last time? Counter for setting circleSeen and QRCodeSeen to false. 
    circleLastSeen = 0
    QRLastSeen = 0
    ellipseLastSeen = 0
    
    #The maximum value for the counter
    counterMaxValue = 50
    
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
    centerThreshold = 70
    

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
        #print "CircleArea: ", self.circleArea, " ellipseArea: ", self.ellipseArea, " ratio: ", (self.circleArea/self.ellipseArea)
        #print "Result: ", (self.circleArea < self.ellipseArea and  self.circleArea/self.ellipseArea > 0.6)
        return self.circleArea < self.ellipseArea and  self.circleArea/self.ellipseArea > 0.6
            
    def droneCentered(self):
        if self.routineStarted:
            return True

        if math.fabs(self.imageXCenter-self.circleXCoor*2) < self.centerThreshold:
            if math.fabs(self.imageYCenter-self.circleYCoor*2) < self.centerThreshold:
                return True
        return False
    
    def printCenters(self):
        print "ImageYCenter: ", self.imageYCenter, " imageXCenter: ", self.imageXCenter
        print "CircleYCenter: ", self.circleYCoor*2, " imageYCenter: ", self.circleXCoor*2, "\n"
    
    def droneAboveCenter(self):
        
        return math.fabs(self.imageYCenter - self.circleYCoor*2) > self.centerThreshold and self.imageYCenter > self.circleYCoor*2
    def droneUnderCenter(self):
        return math.fabs(self.imageYCenter - self.circleYCoor*2) > self.centerThreshold and self.imageYCenter < self.circleYCoor*2
    def droneRightOfCenter(self):

        return math.fabs(self.imageXCenter - self.circleXCoor*2) > self.centerThreshold and self.imageXCenter > self.circleXCoor*2
    def droneLeftOfCenter(self):
        return math.fabs(self.imageXCenter - self.circleXCoor*2) > self.centerThreshold and self.imageXCenter < self.circleXCoor*2
        
    
    def droneLeftOfEllipse(self):
        return math.fabs(self.imageXCenter - self.ellipseXCoor) > self.ellipseThreshold and self.imageXCenter < self.ellipseXCoor
    def droneRightOfEllipse(self):
        return math.fabs(self.imageXCenter - self.ellipseXCoor) > self.ellipseThreshold and self.imageXCenter > self.ellipseXCoor
    def droneAboveEllipse(self):
        return math.fabs(self.imageYCenter - self.ellipseYCoor) > self.ellipseThreshold and self.imageYCenter > self.ellipseYCoor
    def droneUnderEllipse(self):
        return math.fabs(self.imageYCenter - self.ellipseYCoor) > self.ellipseThreshold and self.imageYCenter < self.ellipseYCoor
    
    
    
    
    def addEllipseArea(self, area):
        self.listOfEllipses.append(area)
    
    
    def ellipseAreaGettingBigger(self):
        if len(self.ellipseArea) > 30:
            if np.mean(self.ellipseArea) > np.mean(self.oldListOfEllipses):
                self.oldListOfEllipses = self.listOfEllipses
                self.listOfEllipses = []
                return True
            else:
                return False
        return None
                
    
    def correctDroneMovement(self):
        return self.ellipseAreaGettingBigger()            
    
    
    
    
    
    
    
    
    
    
    
        