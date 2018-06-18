import time

from cv2 import imshow
import cv2
from state import DroneState
from QR.QReader import findAndReadQR
from circle import ObjectAnalyzerTest as oa
from styrringsalgoritmer import libardrone


#from circle import ImageCreater as IC
    #Camera
class Controller(object):

    
    capture = cv2.VideoCapture("output.mkv")
    
    drone = libardrone.ARDrone()
    
    time1 = 0
    time1Set = False
    
    QRFoundThisIteration = False
    
    
    '''
    classdocs
    '''
    state = DroneState.State()
    
    
    
    LR = 0
    BF = 0
    UD = 0
    ROT = 0
    time1 = 0
    trackbarName = "Move"
    trackbarLRName = "LR"
    trackbarBFName = "BF"
    trackbarUDName = "UD"
    trackbarROTName = "ROT"
    trackbartime1Name = "time1" 
    
    
    def nothing(self):
        pass
    
    
    cv2.namedWindow(trackbarName)
    cv2.resizeWindow(trackbarName,780,780)
    
    cv2.createTrackbar(trackbarLRName,trackbarName,0,1000,nothing)
    cv2.createTrackbar(trackbarBFName,trackbarName,0,1000,nothing)
    cv2.createTrackbar(trackbarUDName,trackbarName,0,1000,nothing)
    cv2.createTrackbar(trackbarROTName,trackbarName,0,1000,nothing)
    
    cv2.setTrackbarPos(trackbarLRName,trackbarName,0)
    cv2.setTrackbarPos(trackbarBFName,trackbarName,0)
    cv2.setTrackbarPos(trackbarUDName,trackbarName,0)
    cv2.setTrackbarPos(trackbarROTName,trackbarName,0)
    

    
    def updateTrackbarValues(self):
        self.LR = cv2.getTrackbarPos(self.trackbarLRName,self.trackbarName)/float(1000)
        self.BF = cv2.getTrackbarPos(self.trackbarBFName,self.trackbarName)/float(1000)
        self.UD = cv2.getTrackbarPos(self.trackbarUDName,self.trackbarName)/float(1000)
        self.ROT = cv2.getTrackbarPos(self.trackbarROTName,self.trackbarName)/float(1000)
        
        
    
        
    
    
    

    
    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):
        self.initializeCamera()
        analyzer = oa.ObjectAnalyzer()
        #imageCreaterObj = IC.ImageCreater()

        

        while (True):
            if cv2.waitKey(1) & 0xFF == ord('w'):
                print "Take off"
                break
        self.drone.takeoff()
        time.sleep(5)
        continueGrabbing = True
        #while (self.capture.isOpened()):

        while (True):
            #imageCreaterObj.updateTrackbarValues()
            #imageCreaterObj.drawEllipse()
            #frame = imageCreaterObj.getImage()
            
            #grabbed, readFrame = self.capture.read()
            #if grabbed:
            #    imshow("Webcam", readFrame)
            if cv2.waitKey(1) & 0xFF == ord('1'):
                self.state.circleReached = 1
                print "1"
            elif cv2.waitKey(1) & 0xFF == ord('2'):
                self.state.circleReached = 2
                print "2"
            elif cv2.waitKey(1) & 0xFF == ord('3'):
                self.state.circleReached = 3
                print "3"
            elif cv2.waitKey(1) & 0xFF == ord('4'):
                self.state.circleReached = 4
                print "4"
            elif cv2.waitKey(1) & 0xFF == ord('5'):
                self.state.circleReached = 5
                print "5"
            elif cv2.waitKey(1) & 0xFF == ord('6'):
                self.state.circleReached = 6
                print "6"
            
            if cv2.waitKey(1) & 0xFF == ord('w'):
                
                if continueGrabbing:
                    continueGrabbing = False
                    print "Pause"
                else:
                    continueGrabbing = True
                    print "Continue"
            grabbed, frame = self.drone.readVideo()
            #if continueGrabbing:
            #    grabbed, frame = self.capture.read()
            #    
                
            if not grabbed:
                    print("Frame not grabbed")
                    continue
            #imshow("Frame",frame)
                
            
            self.getQRResult(frame)
            if self.QRFoundThisIteration:
                analyzer.advancedCircleScanning(frame, self.state)
                self.QRFoundThisIteration = False               #Reset for next loop

            else:
                analyzer.normalCircleScanning(frame, self.state)
            
            #print "CircleSeen: ", self.state.circleSeen
            self.updateTrackbarValues()
            self.navigate()
            self.state.updateCounters()
            
            if self.state.QRCodeSeen:
                print "QRAboveCenter", self.state.QRAboveCenter()
                print "QRUnderCenter", self.state.QRUnderCenter()
                print "QRLeftOfCenter", self.state.QRLeftOfCenter()
                print "QRRightOfCenter", self.state.QRRightOfCenter()
                print "Distance", self.state.QRdistance
                print "\n"
            


            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.drone.land()
                break

        # When everything done, release the capture
        #self.capture.release()
        cv2.destroyAllWindows()
        #self.drone.land()
    
        
    def initializeCamera(self):
        #self.capture.open("tcp://192.168.1.1:5555")
        self.capture.open("output.mkv")

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

            self.state.QRRotatedRight = result.QRRotatedRight
            self.state.QRRotatedLeft = result.QRRotatedLeft
            self.state.QRRightside = result.rightSide
            self.state.QRLeftside = result.leftSide
            self.state.QRLowerside = result.lowerSide
            self.state.QRUpperside = result.upperSide


    def navigate(self):
        if not self.state.flownOnce:
            print "FLY "
            self.state.flownOnce = True
            self.drone.asyncCommand(0, -0.15, 0.35, 0, 0.75, 0)
            time.sleep(1.2)
            self.drone.asyncCommand(0, 0.1, 0, 0, 0.3, 0)
            time.sleep(1.8)
            print "afterFly"
            
        #Hover in air to find circle.
        if not self.time1Set:
            self.time1 = time.time()
            self.time1Set = True
        if time.time() - self.time1 < 0.15:
            #print "LR: ", self.LR, " BF: ", self.BF, " UD: ", self.UD, " ROT: ", self.ROT
            self.drone.asyncCommand(self.LR,self.BF, self.UD, self.ROT, 0.05, 0.05)
            return
        self.time1Set = False
        
         
        #print "Ellipse seen"
        #Are the ellipse in the center of the screen?

        
        if self.state.QRCodeSeen:           #We don't give a shit if the drone is centered at the ellipse center
            print "QR"
            if self.state.QRCentered():
                if self.state.QRminDist():
                    print "Go through the ring"
                    self.drone.asyncCommand(0, 0, 0.7, 0, 1, 0)
                    time.sleep(1.1)
                    self.drone.asyncCommand(0, -0.5, 0, 0, 1, 0)
                    self.state.QRCodeSeen = False
                else:
                    print "Go closer to the ring"
                    self.drone.asyncCommand(0, -0.1, 0, 0, 0.5, 0)
            else:
                       
                lf = 0
                bf = 0
                ud = 0
                rot = 0
                timer1 = 0.1
                if self.state.QRAboveCenter():
                    print "Fly up"
                    ud = 0.7
                if self.state.QRUnderCenter():
                    print "Fly down"
                    ud = -0.4

                if self.state.QRRightOfCenter():
                    lf = 0.15
                    print "Fly right"
                    
                if self.state.QRLeftOfCenter():
                    print "Fly left"
                    lf = -0.15
                #print "lf: ", lf, " bf: ", bf, " rot: ",rot,#\n"
                self.drone.asyncCommand(lf, bf, ud, rot, timer1, 0.5)

        
        
        if self.state.circleSeen and self.state.QRCodeSeen:
            lf = 0
            bf = 0
            ud = 0
            rot = 0
            timer1 = 0.1
       
            if self.state.droneRightOfCenter():
                lf = -0.15
                rot = -0.05
                print "Fly Left"
            if self.state.droneLeftOfCenter():
                print "Fly Right"
                lf = 0.15
                rot = 0.05
            #print "lf: ", lf, " bf: ", bf, " rot: ",rot,#\n"
            self.drone.asyncCommand(lf, bf, ud, rot, timer1, 0.5)
               
                          
        if self.state.circleSeen and not self.state.QRCodeSeen:                                      #We are able to detect a circle
            
            #print "Circle seen"
            #Check if circle is in the center of the image
            if not self.state.droneRightOfCenter() and not self.state.droneLeftOfCenter():
                if self.state.droneCentered():
                    if self.state.circleDiameterEqualToHeight():
                        self.drone.asyncCommand(0, -0.3, 0, 0, 1, 0.75)
                        print "RightInCenter"
                        self.state.circleSeen = False
                        #self.drone.asyncCommand(0, 0, -0.4, 0, 0.5, 0)
                    else:      
                        self.drone.asyncCommand(0, -0.5, 0.05, 0, 0.2, 0.75)
                        print "DroneCentered"
               
                    
            else:
                lf = 0
                bf = 0
                ud = 0
                rot = 0
                timer1 = 0.1
                if self.state.droneAboveCenter():
                    print "Fly down"
                    ud = -0.4
                if self.state.droneUnderCenter():
                    print "Fly up"
                    ud = 0.7

                if self.state.droneRightOfCenter():
                    lf = -0.15
                    print "Fly Left"
                if self.state.droneLeftOfCenter():
                    print "Fly Right"
                    lf = 0.15
                #print "lf: ", lf, " bf: ", bf, " rot: ",rot,#\n"
                self.drone.asyncCommand(lf, bf, ud, rot, timer1, 0.5)
               

                
        else:
            #self.drone.asyncCommand(0, 0, 0, -0.1, 0.05, 0.05)
            print "Nothing found"
    
  
controllerObj = Controller()
controllerObj.main()