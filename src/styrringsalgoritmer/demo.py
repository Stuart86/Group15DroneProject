#!/usr/bin/env python

# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Demo app for the AR.Drone.

This simple application allows to control the drone and see the drone's video
stream.
"""


import pygame
import cv2
import libardrone
from QR.QReader import findAndReadQR
import time

#video_capture = cv2.VideoCapture()
#video_capture.open('tcp://192.168.1.1:5555')
qFound = False
running = True
takeoff = False
leftRightFix = 0.0201
backwardsForwardsFix = 0.0119

def qrRoutine(drone):
    global takeoff
    global qFound
    t1  = time.time()
    drone.move(leftRightFix , backwardsForwardsFix , drone.speed , 0)
    while (time.time() - t1) < 5:
        #video_capture.read()
        time.sleep(0.05)
    t1 = time.time()
    drone.move(leftRightFix , backwardsForwardsFix-drone.speed , 0 ,0)
    while (time.time() - t1) < 2:
        #video_capture.read()
        time.sleep(0.05)
    drone.land()
    takeoff = False
    qFound = False

def move_vertically(millimeters , drone):
    n = drone.navdata

def map(value, inMin, inMax, outMin, outMax):
    # Figure out how 'wide' each range is
    leftSpan = inMax - inMin
    rightSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - inMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return outMin + (valueScaled * rightSpan)
def stable_hover(drone):
    n = drone.navdata
    expectedVx = 0
    expectedVy = 0
    correctedVxSpeed = 0
    correctedVySpeed = 0
    threshold = 20
    maxSpeed = float(11110)
    t1 = time.time()

    while (time.time() - t1) < 5:
        ret , n = drone.getNavData()
        if ret:
            vx = n[0]['vx']
            vy = n[0]['vy']
            differenceX = 0
            differenceY = 0
            differenceX = (expectedVx - vx) / maxSpeed
            differenceY = (expectedVy - vy) / maxSpeed
            #if vx > threshold or vx < -threshold:
            #    differenceX = (expectedVx - vx)/maxSpeed
            #
            #if vy > threshold or vy < -threshold:
            #    differenceY = (expectedVy - vy)/maxSpeed
            print "PreviousCorrectX: " , correctedVxSpeed , " PreviousCorrectY: " , correctedVySpeed
            correctedVxSpeed = (float(4)/float(8))*correctedVxSpeed +(float(4)/float(8))*differenceX
            correctedVySpeed = (float(4)/float(8))*correctedVySpeed + (float(4)/float(8))*differenceY
            print "CorrectVX: " , correctedVxSpeed , "CorrectedVY: ", correctedVySpeed
            print "diffx: " , differenceX , " diffY: " , differenceY
            print "vx " , vx , " vy ", vy, "\n"

            drone.move(correctedVySpeed*2 , -(correctedVxSpeed*2) , 0 , 0)
            time.sleep(0.1)
            drone.move(0 , 0 , 0, 0)
            time.sleep(0.3)
    drone.move(0 , 0 ,0 ,0)

def stable_move(drone , eLR , eBF , eUD , eTURN):
    RAD2DEG = 57.2957795131
    euler_max = 0.20943952*RAD2DEG
    vx = 0 ,
    vy = 0
    theta = 0
    phi = 0
    t1 = 0

    lastvx = 0
    lastvy = 0
    movedX = 0 #in millimeters
    movedY = 0 #in millimeters
    a = 0
    ts = time.time()
    t2 = -1
    while (time.time() - ts ) < 6:
        ret , n = drone.getNavData()
        if t2 == -1:
            lastvx = n[0]["vx"]
            lastvy = n[0]["vy"]
            t2 = n["timestamp"] - ts
            continue
        if ret:
            vx = n[0]["vx"]
            vy = n[0]["vy"]
            theta = n[0]["theta"]
            phi = n[0]["phi"]
            t1 = n["timestamp"] - ts
            dt = t1 - t2
            ax = (vx - lastvx) / dt
            ay = (vy - lastvy) / dt
            movedX += 0.5*ax*(t1**2) - 0.5*ax*(t2**2)
            movedY += 0.5 * ay * (t1 ** 2) - 0.5* ay * (t2 ** 2)
            offsetLR = eLR - phi / euler_max*0.5
            offsetBF = eBF - theta / euler_max*0.5
            offsetUD = 0
            offsetTURN = 0
            lastvy = vy
            lastvx = vx
            t2 = t1
            drone.move(eLR + offsetLR, eBF + offsetBF, eUD + offsetUD, eTURN + offsetTURN)
    print "moved in x direction " , -movedX/float(1000)
    print "moved in y direction " , movedY/float(1000)
    drone.land()



def main():
    global qFound
    global running
    global takeoff
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    running = True
    n = 0
    takeoff = False
    t1 = time.time()
    i = 0
    while running:

        # Capture frame-by-frame
        #ret, frame = video_capture.read()

        # Our operations on the frame come here

        ret , frame = drone.readVideo()
        if ret == True:
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('frame', frame)
            n = (n+1)%2
            if n == 0:
                None
                #res = findAndReadQR(frame)

                #if len(res) > 0 and qFound == False:
                    #qFound = True
                #    print i , " " ,res[0].data
                #    i += 1
        #            qrRoutine(drone)


        # Display the resulting frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYUP:
                drone.hover()
                drone.isCollectingData = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.reset()
                    running = False
                # takeoff / land
                elif event.key == pygame.K_k:
                    drone.calibrate(0)
                elif event.key == pygame.K_h:
                    #stable_move(drone , 0, 0, 0, 0)
                    drone.calibrate(1)
                elif event.key == pygame.K_j:
                    drone.calibrate(2)
                elif event.key == pygame.K_l:
                    drone.calibrate(3)
                elif event.key == pygame.K_o:
                    drone.getConfigurationInfo()
                elif event.key == pygame.K_RETURN:
                    t1 = time.time()
                    drone.takeoff()
                    takeoff = True
                elif event.key == pygame.K_SPACE:
                    drone.land()
                    drone.isCollectingData = False
                    libardrone.saveToCSV()
                    takeoff = False
                # emergency
                elif event.key == pygame.K_BACKSPACE:
                    drone.reset()
                # forward / backward
                elif event.key == pygame.K_w:
                    drone.move_forward()
                elif event.key == pygame.K_s:
                    drone.move_backward()
                # left / right
                elif event.key == pygame.K_a:
                    drone.move_left()
                elif event.key == pygame.K_d:
                    drone.move_right()
                # up / down
                elif event.key == pygame.K_UP:
                    drone.move_up()
                elif event.key == pygame.K_DOWN:
                    drone.move_down()
                # turn left / turn right
                elif event.key == pygame.K_LEFT:
                    drone.turn_left()
                elif event.key == pygame.K_RIGHT:
                    drone.turn_right()
                # speed
                elif event.key == pygame.K_1:
                    drone.speed = 0.1
                elif event.key == pygame.K_2:
                    drone.speed = 0.2
                elif event.key == pygame.K_3:
                    drone.speed = 0.3
                elif event.key == pygame.K_4:
                    drone.speed = 0.4
                elif event.key == pygame.K_5:
                    drone.speed = 0.5
                elif event.key == pygame.K_6:
                    drone.speed = 0.6
                elif event.key == pygame.K_7:
                    drone.speed = 0.7
                elif event.key == pygame.K_8:
                    drone.speed = 0.8
                elif event.key == pygame.K_9:
                    drone.speed = 0.9
                elif event.key == pygame.K_0:
                    drone.speed = 1.0
        if (takeoff and (time.time() - t1) > 2):
            None
            #leftRight = 0.0201
            #backwardsForward = 0.0119
            #drone.move(leftRight , backwardsForward ,0 ,0)
        try:
            surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
            # battery status
            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(surface, (0, 0))
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."

if __name__ == '__main__':
    main()
