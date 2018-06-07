'''
Created on 6. jun. 2018

@author: Bruger
'''


class State(object):
    circleSeen = False
    QRCodeSeen = False

    # Where is the image center compared to the circle
    aboveCenter = False
    underCenter = False
    rightOfCenter = False
    leftOfCenter = False
    middleOfCenter = False

    # Distance
    distance = 0

    # circle
    circleCorrect = False  # Correct circle order. 1 to n

    def __init__(self):
        '''
        Constructor
        '''
        
    def setCircleSeen(self, circleSeen): 
        self.circleSeen = circleSeen    
    
    def setQRCodeSeen(self, QRCodeSeen): 
        self.QRCodeSeen = QRCodeSeen    

    def printInfo(self): 
        print("DroneState:")
        print("aboveCenter: ", self.aboveCenter)
        print("underCenter: ", self.underCenter)
        print("rightOfCenter: ", self.rightOfCenter)
        print("leftOfCenter: ", self.leftOfCenter)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        