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
    state = DroneState.State()

    
    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):
        self.initializeCamera()
        analyzer = oa.ObjectAnalyzer()
        while (True):
            
            grabbed, frame = self.capture.read()
            if not grabbed:
                #print("Frame not grabbed")
                continue
            analyzer.analyzeFrame(frame, self.state)
            self.state.printInfo()
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        
        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()
    
        
    def initializeCamera(self):
        #self.capture.open("tcp://192.168.1.1:5555")
        self.capture.open(0)
        
controllerObj = Controller()
controllerObj.main()