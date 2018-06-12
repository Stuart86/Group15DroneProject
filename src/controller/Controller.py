import cv2
from state import DroneState
from circle import ObjectAnalyzer as oa
from QR.QReader import findAndReadQR
import time
from styrringsalgoritmer import libardrone

    #Camera
    

class Controller(object):

    
    capture = cv2.VideoCapture()
    drone = libardrone.ARDrone()

    '''
    classdocs
    '''
    state = DroneState.State()


    
    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):
        #self.initializeCamera()
        analyzer = oa.ObjectAnalyzer()
       
        

        while (True):
            if cv2.waitKey(1) & 0xFF == ord('w'):
                print "Take off"
                break
        self.drone.takeoff()
        time.sleep(5)
        while (True):
            t1 = time.time()
            grabbed, frame = self.drone.readVideo()
            if not grabbed:
                print("Frame not grabbed")
                continue
            
            #Scan the image for different figures. 
            self.getQRResult(frame)
            analyzer.analyzeFrame(frame, self.state)
            #print "CircleSeen: ", self.state.circleSeen
            self.navigate()
            self.state.updateCounters()
            
            

            t2 = time.time()
            #print("Time: ", t2-t1)

            #self.state.printInfo()
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.drone.land()
                break

        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()
    
        
    def initializeCamera(self):
        self.capture.open("tcp://192.168.1.1:5555")
        #self.capture.open(0)

    def getQRResult(self,frame):
        result = findAndReadQR(frame)
        if result is not None:                   
            self.state.QRCodeSeen = True
            self.state.QRdistance = result.distance
            self.state.mostRecentQR = result
            self.state.QRxCoor = result.x
            self.state.QRyCoor = result.y
            self.state.QRdata = result.data
            self.state.resetQRCounter()


    def navigate(self):
        if not self.state.flownOnce:
            print "FLY "
            self.state.flownOnce = True
            self.drone.move(0, 0, 1, 0)
            time.sleep(1)
            self.drone.move(0, 0, 0, 0)
        t1 = time.time()
        while time.time() - t1 < 1:
            self.drone.move(-0.06, 0.01, 0, 0)
            time.sleep(0.05)
            self.drone.move(0, 0, 0, 0)
            time.sleep(0.05)
        if self.state.ellipseSeen or True:                                          #We see something red
            if self.state.circleSeen:                                       #We are able to detect a circle
                if True: #self.state.areasSimilar():                              #The ellipse and the circles area are similar enough to conclude that we are in front of the are. 
                    if self.state.QRCodeSeen:
                        None           
                    else:
                        self.navigateDroneTowardsCenter()
                else:
                    
                    print "Navigate to right or left to make the ellipses area bigger"
            else:
                print "Fly closer to ellipse"
        else:
            print "Rotate to find ellipse"
            
    
    def navigateDroneTowardsCenter(self):
        print "\n"
        self.state.printCenters()
        print "droneCentered: ", self.state.droneCentered()
        print "droneRightOfCenter: ", self.state.droneRightOfCenter()
        print "droneLeftOfCenter: ", self.state.droneLeftOfCenter()
        print "droneAboveCenter: ", self.state.droneAboveCenter()
        print "droneUnderCenter: ", self.state.droneUnderCenter()
        print "droneRightOfEllipse: ", self.state.droneRightOfEllipse()
        print "droneLeftOfEllipse: ", self.state.droneLeftOfEllipse()
        print "droneAboveEllipse: ", self.state.droneAboveEllipse()
        print "droneUnderEllipse: ", self.state.droneUnderEllipse()
        
        
        if not self.state.droneRightOfCenter() and not self.state.droneLeftOfCenter():
            print "in center"
            if self.state.droneCentered():
            
                self.drone.move(-0.05, -0.05, 0, 0)
                time.sleep(0.01)
                self.drone.move(0, 0, 0, 0)
                print "Centered"
            else: 
                print "Not centered"
                if self.state.droneLeftOfCenter():
                    self.drone.move(0, 0, 0, 0.3)
                    time.sleep(0.01)
                    self.drone.move(0, 0, 0, 0)
                    print "Center: rotate right"
                if self.state.droneRightOfCenter():
                    self.drone.move(0, 0, 0, -0.3)
                    time.sleep(0.01)
                    self.drone.move(0, 0, 0, 0.0)
                    print "Center: rotate left"
                
                if self.state.droneUnderCenter():
                    self.drone.move(0, 0, 0.5, 0)
                    time.sleep(0.1)
                    print "Fly up"
                if self.state.droneAboveCenter():
                    self.drone.move(0, 0, -0.5, 0)
                    time.sleep(0.1)
                    print "Fly down"
                
        else:
            print "Not in center"
            
            if self.state.droneLeftOfCenter():
                self.drone.move(0, 0, 0, 0.1)
                time.sleep(0.05)
                self.drone.move(0, 0, 0, 0)
                print "Fly right"
            if self.state.droneRightOfCenter():
                self.drone.move(0, 0, 0, -0.1)
                time.sleep(0.05)
                self.drone.move(0, 0, 0, 0)
                print "Fly left"
            if self.state.droneUnderCenter():
                self.drone.move(0, 0, 0.5, 0)
                time.sleep(0.01)
                print "Fly up"
            if self.state.droneAboveCenter():
                self.drone.move(0, 0, -0.5, 0)
                time.sleep(0.01)
                print "Fly down"
        
controllerObj = Controller()
controllerObj.main()