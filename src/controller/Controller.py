import cv2
from state import DroneState
from circle import ObjectAnalyzer as oa
from QR.QReader import findAndReadQR
import time
from styrringsalgoritmer import libardrone
#from circle import ImageCreater as IC
from cv2 import imshow
    #Camera
    

class Controller(object):

    
    capture = cv2.VideoCapture()
    drone = libardrone.ARDrone()
    
    time1 = 0
    time1Set = False
    
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
    
    cv2.setTrackbarPos(trackbarLRName,trackbarName,10)
    cv2.setTrackbarPos(trackbarBFName,trackbarName,30)
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
        #self.initializeCamera()
        analyzer = oa.ObjectAnalyzer()
        #imageCreaterObj = IC.ImageCreater()

        

        while (True):
            if cv2.waitKey(1) & 0xFF == ord('w'):
                print "Take off"
                break
        self.drone.takeoff()
        self.drone.asyncCommand(-0.7, 0.5, 0, 0, 1, 0)
        time.sleep(5)
        while (True):
            
            #imageCreaterObj.updateTrackbarValues()
            #imageCreaterObj.drawEllipse()
            #frame = imageCreaterObj.getImage()
            
            #grabbed, readFrame = self.capture.read()
            #if grabbed:
            #    imshow("Webcam", readFrame)
                
            grabbed, frame = self.drone.readVideo()
            if not grabbed:
                #print("Frame not grabbed")
                continue
            
            #Scan the image for different figures. 
            self.getQRResult(frame)
            analyzer.analyzeFrame(frame, self.state)
            #print "CircleSeen: ", self.state.circleSeen
            self.updateTrackbarValues()
            self.navigate()
            self.state.updateCounters()
            
            


            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.drone.land()
                break

        # When everything done, release the capture
        #self.capture.release()
        cv2.destroyAllWindows()
        self.drone.land()
    
        
    def initializeCamera(self):
        #self.capture.open("tcp://192.168.1.1:5555")
        self.capture.open(0)

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
            self.drone.asyncCommand(-0.02, 0.02, 0.5, 0, 1, 0)
            time.sleep(1.5)
            print "afterFly"
            
        #Hover in air to find circle.
        if not self.time1Set:
            self.time1 = time.time()
            self.time1Set = True
        if time.time() - self.time1 < 0.1:
            print "LR: ", self.LR, " BF: ", self.BF, " UD: ", self.UD, " ROT: ", self.ROT
            self.drone.asyncCommand(self.LR,self.BF, self.UD, self.ROT, 0.05, 0.05)
            return
        self.time1Set = False
        
        if self.state.ellipseSeen: 
            #print "Ellipse seen"
            #Are the ellipse in the center of the screen?
            if not self.state.droneCenteredWithEllipse():           #We don't give a shit if the drone is centered at the ellipse center
                #if self.state.droneAboveEllipse():
                #    self.drone.asyncCommand(0, 0, -0.1, 0, 0.05, 0)
                #    print "Fly down"
                #if self.state.droneUnderEllipse():
                #    self.drone.asyncCommand(0, 0, 0.1, 0, 0.05, 0)
                #    print "Fly up"
                if self.state.droneRightOfEllipse():
                    #self.drone.asyncCommand(0, 0.1, 0, 0.5, 0.05, 0)
                    print "Rotate left"
                if self.state.droneLeftOfEllipse():
                    #self.drone.asyncCommand(0, 0.1, 0, -0.5, 0.05, 0)
                    print "Rotate right"

            if self.state.circleSeen:                                       #We are able to detect a circle
                #print "Circle seen"
                #Check if circle is in the center of the image
                if not self.state.droneRightOfCenter() and not self.state.droneLeftOfCenter():
                    if self.state.droneCentered():
                        self.drone.asyncCommand(0, -0.1,0.05, 0, 0.1, 0)
                        if self.state.circleDiameterEqualToHeight():
                            self.drone.asyncCommand(0, -0.2, 0.1, 0, 0.5, 0)
                        print "moveForward"
                        
                else:
                    lf = 0
                    bf = 0
                    ud = 0
                    rot = 0
                    timer1 = 0.075
                    if self.state.droneAboveCenter():
                        print "Fly down"
                        ud = -0.4
                    if self.state.droneUnderCenter():
                        print "Fly up"
                        ud = 0.7

                    if self.state.droneRightOfCenter():
                        lf = -0.2
                        print "Fly Left"
                    if self.state.droneLeftOfCenter():
                        print "Fly Right"
                        lf = 0.2
                    print "lf: ", lf, " bf: ", bf, " rot: ",rot,#\n"
                    self.drone.asyncCommand(lf, bf, ud, rot, timer1, 0)

                    
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
            
                #self.drone.move(-0.05, -0.05, 0, 0)
                #time.sleep(0.01)
                #self.drone.move(0, 0, 0, 0)
                print "Centered"
            else: 
                print "Not centered"
                if self.state.droneLeftOfCenter():
                    #self.drone.move(0, 0, 0, 0.3)
                    #time.sleep(0.01)
                    #self.drone.move(0, 0, 0, 0)
                    print "Center: rotate right"
                if self.state.droneRightOfCenter():
                    #self.drone.move(0, 0, 0, -0.3)
                    #time.sleep(0.01)
                    #self.drone.move(0, 0, 0, 0.0)
                    print "Center: rotate left"
                
                if self.state.droneUnderCenter():
                    #self.drone.move(0, 0, 0.5, 0)
                    #time.sleep(0.1)
                    print "Fly up"
                if self.state.droneAboveCenter():
                    #self.drone.move(0, 0, -0.5, 0)
                    #time.sleep(0.1)
                    print "Fly down"
                
        else:
            print "Not in center"
            
            if self.state.droneLeftOfCenter():
                #self.drone.move(0, 0, 0, 0.1)
                #time.sleep(0.05)
                #self.drone.move(0, 0, 0, 0)
                print "Fly right"
            if self.state.droneRightOfCenter():
                #self.drone.move(0, 0, 0, -0.1)
                #time.sleep(0.05)
                #self.drone.move(0, 0, 0, 0)
                print "Fly left"
            if self.state.droneUnderCenter():
                #self.drone.move(0, 0, 0.5, 0)
                #time.sleep(0.01)
                print "Fly up"
            if self.state.droneAboveCenter():
                #self.drone.move(0, 0, -0.5, 0)
                #time.sleep(0.01)
                print "Fly down"
        
controllerObj = Controller()
controllerObj.main()