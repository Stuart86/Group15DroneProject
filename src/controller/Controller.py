import cv2
from state import DroneState
from circle import ObjectAnalyzer as oa
from QR.QReader import findAndReadQR
from styrringsalgoritmer import libardrone
import time

    #Camera
    

class Controller(object):

    
    capture = cv2.VideoCapture()
    #drone = libardrone.ARDrone()

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
        frameCounter = 0
        #self.drone.takeoff()

        while (True):
            t1 = time.time()


            
            grabbed, frame = self.capture.read()
            if not grabbed:
                #print("Frame not grabbed")
                continue
            frameCounter = (frameCounter + 1)%2

            if (frameCounter % 2 == 0):

                continue
            result = findAndReadQR(frame)
            if(len(result) > 0):
                for i in result:
                    print (i)

            analyzer.analyzeFrame(frame, self.state)

            t2 = time.time()
            #print("Time: ", t2-t1)

            #self.state.printInfo()
            
            
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