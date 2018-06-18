from styrringsalgoritmer import libardrone , arnetwork
from QR import QReader
import cv2
import time
import math
import numpy as np

distToQR = 200 #in cm
width = 640
heigth = 360

speedlimit = 100
C = 99
eLR = math.exp(-0.000127642*speedlimit)
eUD = math.exp(-0.000255284*speedlimit)

g = 9.816 # m / s^2
RAD2DEG = 57.2957795131
DEG2RAD = 0.01745329251
euler_max = 0.20943952 #Radians
yaw_max_speed = 1.7453293 #Radians / second
vz_max = 0.700 #m / second
drone_weight = 0.425 #Kg



def main():
    cv2.namedWindow("CLICK ME" , cv2.WINDOW_NORMAL)
    drone = libardrone.ARDrone()
    while True:
        if cv2.waitKey(1) & 0xFF == ord('w'):
            drone.takeoff()
            time.sleep(1)
            drone.hover()
            time.sleep(4)
            break
    moveUp(drone , 1)
    moveUp(drone , -1)
    #moveForward(drone , 1)
    #moveForward(drone , -1)
    drone.land()
    while True:
        ret , frame = drone.readVideo()

        if ret:
            result = QReader.findAndReadQR(frame)
            if result is not None:
                print result.data , " Distance " ,result.distance
                print "x: " , result.x , " y: " , result.y



        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break

def moveUp(drone , meterUP):
    state = drone.estimator.getState()
    currentZ = state[2]
    targetZ = currentZ+meterUP
    sign = meterUP/math.fabs(meterUP)
    while(currentZ > targetZ*1.05 or currentZ < targetZ*0.95):
        if currentZ > targetZ:
            drone.move(0, 0, -0.5, 0)
        else:
            drone.move(0 , 0 , 0.5 , 0)
        time.sleep(0.033)
        state = drone.estimator.getState()
        currentZ = state[2]
    drone.hover()
def moveForward(drone , metersForward):
    state = drone.estimator.getState()
    currentX = state[0]
    currentY = state[1]
    yaw = state[6]
    targetX = state[0] + math.cos(yaw) * metersForward
    targetY = state[1] + math.sin(yaw) * metersForward
    print targetX
    print targetY
    metersLeft = math.sqrt((currentX - targetX)**2 + (currentY - targetY)**2)
    while metersLeft > 0.01:
        if metersForward < 0:
            drone.move(0 , 0.1 , 0 , 0)
        else:
            drone.move(0 , -0.1 , 0 , 0)
        time.sleep(0.05)
        state = drone.estimator.getState()
        currentX = state[0]
        currentY = state[1]
        newmetersLeft = math.sqrt((currentX - targetX) ** 2 + (currentY - targetY) ** 2)
        if (newmetersLeft+0.1) > metersLeft:
            drone.hover()
            return
        metersLeft = newmetersLeft
        print "meters left " , metersLeft
        print "currentx ", currentX, " currenty " , currentY

    drone.hover()
def move(drone , metersForward , metersUp, metersToRight):
    #DOESN'T WORK
    state = drone.estimator.getState()
    max_speed = 0.5 #m/s
    yaw = state[6]
    targetX = state[0] + math.cos(yaw)*metersForward + math.sin(yaw)*metersToRight
    targetY = state[1] + math.sin(yaw)*metersForward - math.cos(yaw)*metersToRight
    targetZ = state[2] + metersUp
    xvgoal = 0.1
    yvgoal = 0.1
    zvgoal = 0.1
    ax_max = 1
    ay_max = 1
    interval = 0.06
    atX = False
    atY = False
    atZ = False
    print state[0] , " " , state[1] , " " , state[2]
    print targetX , " " , targetY , " " , targetZ
    while not (atX and atY and atZ):
        currentX = state[0]
        currentY = state[1]
        currentZ = state[2]
        currentVX = state[3]
        currentVY = state[4]
        currentVZ = state[5]
        lr = 0
        bf = 0
        ud = 0
        xDiff = targetX - currentX
        yDiff = targetY - currentY
        zDiff = targetZ - currentZ

        if currentX >= targetX*0.95 and currentX <= targetX*1.05:
            atX = True
            xvgoal = 0
        else:
            xvsign = xDiff / math.fabs(xDiff)
            t1 = xDiff/interval
            xvgoal =  max_speed if math.fabs(t1) > max_speed  else (math.fabs(t1) if math.fabs(t1) > 0.002 else 0.002)
            xvgoal *= xvsign
            atX = False

        if currentY >= targetY*0.95 and currentY <= targetY*1.05:
            atY = True
            yvgoal = 0
        else:
            yvsign = yDiff / math.fabs(yDiff)
            t2 = yDiff / interval
            yvgoal = max_speed if math.fabs(t2) > max_speed else (math.fabs(t2) if math.fabs(t2) > 0.002 else 0.002)
            yvgoal *= yvsign
            atY = False

        if currentZ >= targetZ*0.95 and currentZ <= targetZ*1.05:
            atZ = True
            zvgoal = 0
        else:
            zvsign = zDiff / math.fabs(zDiff)
            t3 = zDiff / interval
            zvgoal = max_speed if math.fabs(t3) > max_speed else (math.fabs(t3) if math.fabs(t3) > 0.002 else 0.002)
            zvgoal *= zvsign
            atZ = False
        ax = 0
        ay = 0
        cosy = math.cos(yaw)
        siny = math.sin(yaw)
        if math.fabs(xDiff) > 0.005:
            speedDiffX = xvgoal - currentVX
            ax = speedDiffX / interval
            ax = ax_max if math.fabs(ax) > ay_max else ax

        if math.fabs(yDiff) > 0.005:
            speedDiffY = yvgoal - currentVY
            ay = speedDiffY / interval
            ay = ay_max if math.fabs(ay) > ay_max else ay

        T = np.array([ [cosy , siny] , [siny , -cosy]])
        b = np.array([ax/g , ay/g])
        sol = np.linalg.solve(T , b)
        if math.fabs(zDiff) > 0.005:
            speedDiffZ = zvgoal - currentVZ
            ud = speedDiffZ / vz_max
            zvsign = zDiff / math.fabs(zDiff)
            ud = max_speed if math.fabs(ud) > max_speed else (math.fabs(ud) if math.fabs(ud) < 0.05 else 0.05)
            ud *= zvsign
        bf = math.asin(sol[0])/euler_max
        lr = math.asin(sol[1])/euler_max
        print lr," ", bf , " ",ud
        #drone.move(lr, bf , ud , 0)
        time.sleep(0.03)
        state = drone.estimator.getState()

def centerOnQR(QR_TEXT):
    None

def getqrpositionvectorToCenter(QRCODE):
    x = QRCODE.x
    y = QRCODE.y
    return width/2 - x , y - heigth/2

def mov(position , e , c , max):
    return max/(1+c*math.pow(e , position))-max/2

if __name__ == "__main__":
    main()