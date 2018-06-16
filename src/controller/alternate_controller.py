from styrringsalgoritmer import libardrone , arnetwork
from QR import QReader
import cv2
import time
import math

distToQR = 200 #in cm
width = 640
heigth = 360

speedlimit = 100
C = 99
eLR = math.exp(-0.000127642*speedlimit)
eUD = math.exp(-0.000255284*speedlimit)



def main():
    cv2.namedWindow("CLICK ME" , cv2.WINDOW_NORMAL)
    drone = libardrone.ARDrone()
    vx = 0
    vy = 0
    vz = 0
    t1 = 1
    phi = 0
    theta = 0
    prevVx = 0
    prevVy = 0
    prevVz = 0
    prevAlt = 0
    prevTheta = 0
    prevPhi = 0
    t2 = 0
    alt = 750
    avgVx = 0
    avgVy = 0
    vxArr = []
    vyArr = []

    maxSpeed = 11110
    while True:
        if cv2.waitKey(1) & 0xFF == ord('w'):
            #drone.takeoff()
            time.sleep(3)
            #drone.hover()
            #drone.move(0, 0, 0.5, 0)
            time.sleep(1)
            break
    i = 0
    while i < 10 :
        new , nav = drone.getNavData()
        if new:
            i+=1
            prevVx = vx
            prevVy = vy
            prevVz = vz
            prevAlt = alt
            prevPhi = phi
            prevTheta = theta
            t2 = t1
            vx = nav[0]["vx"]
            vy = nav[0]["vy"]
            t1 = nav["timestamp"]
            alt = nav[0]["altitude"]
            phi = nav[0]["phi"]
            theta = nav[0]["theta"]
            vz = (alt - prevAlt) / (t1 - t2)

    while True:
        new, nav = drone.getNavData()
        if new:
            prevVx = vx
            prevVy = vy
            prevVz = vz
            prevAlt = alt
            prevPhi = phi
            prevTheta = theta
            t2 = t1
            vx = nav[0]["vx"]
            vy = nav[0]["vy"]
            t1 = nav["timestamp"]
            alt = nav[0]["altitude"]
            phi = nav[0]["phi"]
            theta = nav[0]["theta"]
            vz = (alt - prevAlt) / (t1 - t2)

            vxArr.append(vx)
            vyArr.append(vy)
            #if(len(vxArr) == 5):
            #    avgVx = (vxArr[0] + vxArr[1] + vxArr[2] + vxArr[3] + vxArr[4])/5
            #    avgVy = (vyArr[0] + vyArr[1] + vyArr[2] + vyArr[3] + vyArr[4])/5
            #    vxArr = []
            #    vyArr = []
                #print avgVx ," ", avgVy
        ret , frame = drone.readVideo()
        if ret:
            result = QReader.findAndReadQR(frame)
            if result is not None:
                print result.data , " Distance " ,result.distance
                print "x: " , result.x , " y: " , result.y
                #xDiff , yDiff = getqrpositionvectorToCenter(result)


                desiredSpeedVx = result.distance*(-0.476190476)+69.04761905
                desiredSpeedVy = mov(result.x , eLR , C , speedlimit)
                desiredSpeedVz = mov(result.y , eUD , C , speedlimit)
                altDiff = math.sin(-theta * 0.01745329251)*result.distance*10
                print "vy: " , desiredSpeedVy , " vx: " , desiredSpeedVx , " vz: " , desiredSpeedVz
                print "alt of qr: " , altDiff
                moveLR = 0
                moveUD = 0
                moveBF = (distToQR / result.distance - 1) / 4
                if vx > desiredSpeedVx:
                    moveBF + vx/maxSpeed*1.5
                else:
                    moveBF - vx/maxSpeed*1.5
                if vy > desiredSpeedVy:
                    moveLR - vy/maxSpeed*1.5
                else:
                    moveLR + vy/maxSpeed*1.5
                moveUD = moveUD - ((alt - 1200)/1200)/2


                #if  math.fabs(xDiff) < 20 and math.fabs(yDiff) < 20 and math.fabs(moveBF) < 0.002 : ##Do this when drone is reasonably centered
                #    drone.move(-vy/maxSpeed*1.3 , -moveBF , 0.5 , 0)
                #    time.sleep(2)
                #    drone.move(-vy/maxSpeed*1.3 , -0.5 , 0 , 0)
                #    time.sleep(1.5)
                #    drone.hover()
                #    drone.land()
                #else:
                #    drone.move(moveLR , moveBF , moveUD , 0)
                    #drone.asyncCommand(moveLR , moveBF , moveUD , 0, 0.05,0.01)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            #drone.land()
            break

def getqrpositionvectorToCenter(QRCODE):
    x = QRCODE.x
    y = QRCODE.y
    return width/2 - x , y - heigth/2

def mov(position , e , c , max):
    return max/(1+c*math.pow(e , position))-max/2

if __name__ == "__main__":
    main()