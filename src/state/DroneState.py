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

    def __init__(self, params):
        '''
        Constructor
        '''
        
    def setCircleSeen(self, circleSeen): 
        self.circleSeen = circleSeen    
    
    def setQRCodeSeen(self, QRCodeSeen): 
        self.QRCodeSeen = QRCodeSeen    

    def setAboveCenter(self, aboveCenter):
        self.aboveCenter = aboveCenter
        
    def setUnderCenter(self, underCenter):
        self.underCenter = underCenter
        
    def setRightOfCenter(self, rightOfCenter):
        self.rightOfCenter = rightOfCenter
        
    def setLeftOfCenter(self, leftOfCenter):
        self.leftOfCenter = leftOfCenter
        
    def setMiddleOfCenter(self, middleOfCenter):
        self.middleOfCenter = middleOfCenter
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        