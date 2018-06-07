import pygame
import cv2
import libardrone
import time

video_capture = cv2.VideoCapture()
video_capture.open('tcp://192.168.1.1:5555')


def main():
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    drone.takeoff()
    running = True

    while running:

        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)

        time.sleep(3)
        drone.move_forward()
        time.sleep(2)
        drone.halt()


def Takeoff():
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    drone.takeoff()


def Moveforward():

    drone = libardrone.ARDrone()
    FrontOfObject = False

    while not FrontOfObject:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)

        drone.move_forward()

        if FrontOfObject:
            drone.hover()


def MoveLeft():

    drone = libardrone.ARDrone()
    FrontOfObject = False

    while not FrontOfObject:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)

        drone.move_left()

        if FrontOfObject:
            drone.hover()


def MoveRight():

    drone = libardrone.ARDrone()
    FrontOfObject = False

    while not FrontOfObject:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)

        drone.move_right()

        if FrontOfObject:
            drone.hover()

def MoveDown():

    drone = libardrone.ARDrone()
    FrontOfObject = False

    while not FrontOfObject:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)

        drone.move_down()

        if FrontOfObject:
            drone.hover()

def MoveUp():

    drone = libardrone.ARDrone()
    FrontOfObject = False

    while not FrontOfObject:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)

        drone.move_up()

        if FrontOfObject:
            drone.hover()


def GoThroughRing():

    drone = libardrone.ARDrone()
    FrontOfObject = False
    drone.move_forward()



if __name__ == '__main__':
    main()
