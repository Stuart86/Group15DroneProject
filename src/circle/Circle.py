import math

from cv2 import imshow
import cv2
from state import DroneState
from cv2 import imshow

import numpy as np


#Variables
#Frames and such
class Circle: 
    #Circles:

    listOfCircles = [] 
    printedCircles = []

    error = 1
    amountOfCircles = 1

    def setError(self, error):
        self.error = error
    
    def setAmountOfCircles(self, circles):
        self.amountOfCircles = circles
        
        
    def printCircleOnFrame(self, circleToBePrinted, frame, width, height, State):
        avarageCenter = (int(round(circleToBePrinted[0])),int(round(circleToBePrinted[1])))
        avarageRadius = int(round(circleToBePrinted[2]))
        cv2.circle(frame, avarageCenter, avarageRadius, (255, 0, 255), 3)
        #cv2.circle(frame, avarageCenter, 1, (100, 100, 0), 3)
       
        State.circleRadius = avarageRadius
        State.circleArea = float(avarageRadius * avarageRadius * 3.14159265)
        State.circleXCoor = circleToBePrinted[0]
        State.circleYCoor = circleToBePrinted[1]
        State.circleSeen = True
        State.resetCircleCounter()
        imshow("Circle", frame)
        



    def circleSimilar(self, circle1, circle2):
        try:
            if(math.fabs(circle1[0]-circle2[0]) >= self.error or math.fabs(circle1[1]-circle2[1]) >= self.error or math.fabs(circle1[2]-circle2[2]) >= self.error):             
                    return False
            return True  
        except OverflowError: 
            print "Circle1: ", circle1, " Circle2: ", circle2
         
    def circleKnown(self, newCircle):
        for c in self.listOfCircles:
            if(len(c) == 1):
                avarageCircle = c[0]
            else:
                avarageCircle = np.mean(c, axis = 0)
                
            if(self.circleSimilar(avarageCircle, newCircle)):
                c.append(newCircle)
                
                break
        self.listOfCircles.append([newCircle])
        return
        
    
            
    def enoughNewCircles(self, frame, width, height, state):
        for c in self.listOfCircles:
            if(len(c) == self.amountOfCircles):
                #print(self.amountOfCircles)
                circleToBePrinted = np.mean(c, axis = 0)
                self.printCircleOnFrame(circleToBePrinted,frame,width, height, state)
                self.listOfCircles.remove(c)
        return;









