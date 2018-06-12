import cv2
from state import DroneState
from circle import ObjectAnalyzer as oa
from QR.QReader import findAndReadQR
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
       
        #self.drone.takeoff()

        while (True):
            t1 = time.time()


            
            grabbed, frame = self.capture.read()
            if not grabbed:
                #print("Frame not grabbed")
                continue
            
            #Scan the image for different figures. 
            self.getQRResult(frame)
            analyzer.analyzeFrame(frame, self.state)
            self.navigate()
            self.state.updateCounters()
            

            t2 = time.time()
            #print("Time: ", t2-t1)

            #self.state.printInfo()
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()
    
        
    def initializeCamera(self):
        self.capture.open("tcp://192.168.1.1:5555")
        #self.capture.open(0)

    def getQRResult(self,frame):
        result = findAndReadQR(frame)
        if(len(result) > 0):
            for i in result:                   
                self.state.QRCodeSeen = True
                self.state.QRdistance = i.distance
                self.state.mostRecentQR = i
                self.state.QRxCoor = i.x
                self.state.QRyCoor = i.y
                self.state.QRdata = i.data
    

    def navigate(self):
        if self.state.ellipseSeen:                                          #We see something red
            if self.state.circleSeen:                                       #We are able to detect a circle
                if self.state.areasSimilar():                               #The ellipse and the circles area are similar enough to conclude that we are in front of the are. 
                    if self.state.QRCodeSeen:
                        if self.state.droneCentered():
                            print "Fly forward. "
                        else:
                            if self.state.droneAboveCenter():
                                print "Fly up"
                            if self.state.droneUnderCenter():
                                print "Fly down"
                            if self.state.droneRightOfCenter():
                                print "Fly right"
                            if self.state.droneLeftOfCenter():
                                print "Fly left"
                    else:
                        self.navigateDroneTowardsCenter()
                else:
                    
                    print "Navigate to right or left to make the ellipses area bigger"
            else:
                print "Fly closer to ellipse"
        else:
            print "Rotate to find ellipse"
            
    
    def navigateDroneTowardsCenter(self):
        if self.state.droneCentered():
            print "Fly forward. Navigate "
        else:
            if self.state.droneAboveCenter():
                print "Fly up"
            if self.state.droneUnderCenter():
                print "Fly down"
            if self.state.droneRightOfCenter():
                print "Fly right"
            if self.state.droneLeftOfCenter():
                print "Fly left"
    
controllerObj = Controller()
controllerObj.main()