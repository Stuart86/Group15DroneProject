'''
Created on 7. jun. 2018

@author: lasse
'''
from state import DroneState
from circle import ObjectAnalyzer as oa

import cv2

    #Camera
    

class Controller(object):

    
    capture = cv2.VideoCapture()

    '''
    classdocs
    '''
    state = DroneState()

    
    def __init__(self, params):
        '''
        Constructor
        '''
        
    def main(self):
        self.initializeCamera()
        analyzer = oa()
        while (True):
            
            grabbed, frame = self.capture.read()
            
            if not grabbed:
                #print("Frame not grabbed")
                continue
            analyzer.analyzeFrame(frame)
            
        
        # When everything done, release the capture
        self.capture.release()
    
        
    def initializeCamera(self):
        self.capture.open("tcp://192.168.1.1:5555")
        
        
controllerObj = Controller()
controllerObj.main()