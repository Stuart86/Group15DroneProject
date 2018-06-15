'''
Created on 6. jun. 2018

@author: Bruger
'''

class MyClass(object):
   
    
    circleSeen = False
    QRCodeSeen = False
    
    
    #Where is the image center compared to the circle
    aboveCenter = False
    underCenter = False
    rightOfCenter = False
    leftOfCenter = False
    middleOfCenter = False
    
    #Distance
    distance = 0
    
    #circle
    circleCorrect =  False #Correct circle order. 1 to n
    
   
   


    def __init__(self, params):
        '''
        Constructor
        '''
        