import math

from cv2 import imshow
import cv2
from state import DroneState

import numpy as np

from state import DroneState


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
        
<<<<<<< HEAD
        #textCenter = (avarageCenter[0]+50,avarageCenter[1]-60)
        #cv2.putText(frame, str(textCenter), textCenter, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
        #trackedCenter = (avarageCenter[0],avarageCenter[1]-60)
        #cv2.putText(frame, 'Tracked', trackedCenter, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)


        print(width/2)
        print(height/2)
        print(avarageCenter)
        #Return to this and make it more efficient. No if statements.
        if (width/2) < avarageCenter[0]*2:
            State.leftOfCenter = True
        else:
            State.leftOfCenter = False
        if (width / 2) > avarageCenter[0]*2:
            State.rightOfCenter = True
        else: 
            State.rightOfCenter = False
        if (height / 2) < avarageCenter[1]*2:
            State.underCenter = True
        else:
            State.underCenter = False
        if (height / 2) > avarageCenter[1]*2:
            State.aboveCenter = True
        else:
            State.aboveCenter = False
        

        #cv2.line(frame, (int(width / 2), int(height / 2)), avarageCenter, (0, 255, 0), 5)
    
        #x = math.sqrt((int(width / 2) - avarageCenter[0]) ** 2 + (int(height / 2) - avarageCenter[1]) ** 2)
    
    #    cv2.putText(frame, "Distance" + str(math.ceil(x)), (int(width / 2) - 100, int(height / 2) + 100),
    #                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
    #                1, cv2.LINE_AA)

        #if (x <= 40):
           # cv2.drawMarker(frame, (int(width / 2), int(height / 2)), (0, 0, 255), markerType=cv2.MARKER_CROSS,
            #               markerSize=10,
             #              thickness=2, line_type=cv2.LINE_AA)
            #cv2.putText(frame, "Locked", (int(width / 2) - 100, int(height / 2) + 150),
            #            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
            #            2, cv2.LINE_AA)

=======
>>>>>>> branch 'Objektgenkendelse' of https://github.com/Stuart86/Group15DroneProject



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









