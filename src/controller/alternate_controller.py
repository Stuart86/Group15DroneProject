from styrringsalgoritmer import libardrone , arnetwork
from QR import QReader
import cv2
import time
import math

distToQR = 200 #in cm
width = 640
heigth = 360

def main():
    cv2.namedWindow("CLICK ME" , cv2.WINDOW_NORMAL)
    drone = libardrone.ARDrone()
    time.sleep(5)
    vx = 0
    vy = 0
    alt = 750
    avgVx = 0
    avgVy = 0
    vxArr = []
    vyArr = []
    maxSpeed = 11110
    while True:
        if cv2.waitKey(1) & 0xFF == ord('w'):
            drone.takeoff()
            time.sleep(3)
            drone.hover()
            drone.move(0, 0, 0.5, 0)
            time.sleep(1)
            break
    while True:
        new, nav = drone.getNavData()
        if new:
            vx = nav[0]["vx"]
            vy = nav[0]["vy"]
            alt = nav[0]["altitude"]
            vxArr.append(vx)
            vyArr.append(vy)
            if(len(vxArr) == 5):
                avgVx = (vxArr[0] + vxArr[1] + vxArr[2] + vxArr[3] + vxArr[4])/5
                avgVy = (vyArr[0] + vyArr[1] + vyArr[2] + vyArr[3] + vyArr[4])/5
                vxArr = []
                vyArr = []
                #print avgVx ," ", avgVy
        ret , frame = drone.readVideo()
        if ret:
            result = QReader.findAndReadQR(frame)
            if result is not None:
                print result.data , " Distance " ,result.distance
                print "x: " , result.x , " y: " , result.y
                xDiff , yDiff = getqrpositionvectorToCenter(result)
                moveLR = xDiff/width
                moveUD = yDiff/heigth
                moveBF = (distToQR/result.distance - 1)/4
                desiredSpeedVx = moveBF*20
                desiredSpeedVy = moveLR*20
                if vx > desiredSpeedVx:
                    moveBF + vx/maxSpeed*1.5
                else:
                    moveBF - vx/maxSpeed*1.5
                if vy > desiredSpeedVy:
                    moveLR - vy/maxSpeed*1.5
                else:
                    moveLR + vy/maxSpeed*1.5
                moveUD = moveUD - ((alt - 1200)/1200)/2


                if  math.fabs(xDiff) < 20 and math.fabs(yDiff) < 20 and math.fabs(moveBF) < 0.002 : ##Do this when drone is reasonably centered
                    drone.move(-vy/maxSpeed*1.3 , -moveBF , 0.5 , 0)
                    time.sleep(2)
                    drone.move(-vy/maxSpeed*1.3 , -0.5 , 0 , 0)
                    time.sleep(1.5)
                    drone.hover()
                    drone.land()
                else:
                    drone.move(moveLR , moveBF , moveUD , 0)
                    #drone.asyncCommand(moveLR , moveBF , moveUD , 0, 0.05,0.01)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break

def getqrpositionvectorToCenter(QRCODE):
    x = QRCODE.x
    y = QRCODE.y
    return width/2 - x , y - heigth/2
if __name__ == "__main__":
    main()