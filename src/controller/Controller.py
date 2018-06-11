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
            #-----Converting image to LAB Color model----------------------------------- 
            lab= cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            cv2.imshow("lab",lab)
            
            #-----Splitting the LAB image to different channels-------------------------
            l, a, b = cv2.split(lab)
            cv2.imshow('l_channel', l)
            cv2.imshow('a_channel', a)
            cv2.imshow('b_channel', b)
            
            #-----Applying CLAHE to L-channel-------------------------------------------
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            cv2.imshow('CLAHE output', cl)
            
            #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
            limg = cv2.merge((cl,a,b))
            cv2.imshow('limg', limg)
            
            #-----Converting image from LAB Color model to RGB model--------------------
            final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            cv2.imshow('finalLab', final)

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