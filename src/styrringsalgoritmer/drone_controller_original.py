import libardrone
import time

drone = libardrone.ARDrone()

def main():
    testMethod()

def testMethod():
    drone.set_speed(1)
    drone.takeoff()
    time.sleep(4)
    drone.move_forward()
    time.sleep(2)
    drone.hover()
    drone.move_backward()
    time.sleep(0.8)
    drone.hover()
    time.sleep(2)
    drone.land()
    time.sleep(2)
    drone.halt()

if __name__ == '__main__':
    main()