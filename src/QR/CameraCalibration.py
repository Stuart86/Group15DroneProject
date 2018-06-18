import cv2
import numpy as np
import glob
import time

objP = np.zeros( (6*7 , 3) , np.float32 )
objP[: , :2] = np.mgrid[0 : 7 , 0:6].T.reshape(-1 , 2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER , 40 , 0.001)
objPoints = []
imgPoints = []


def collectGoodImages(cap):

    h , w = frame.shape[:2]
    i = 0
    while True and i < 50:
        ret , img = cap.read()
        if ret:
            cv2.imshow("img", img)
            gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
            ret , corners = cv2.findChessboardCorners(gray , (7,6) , None)
            if ret:
                corners2 = cv2.cornerSubPix(gray , corners, (11,11) , (-1 , -1) , criteria)
                #cv2.drawChessboardCorners(img , (7,6) , corners2, ret)
                cv2.imshow("img", img)
                k = cv2.waitKey(0)
                if ord("s") == k:
                    print "Saved img#", i
                    cv2.imwrite("images/img_%d.png" % (i), img)
                    i += 1
                else:
                    continue
            else:
                cv2.waitKey(1)

def calibrateCamera(cap):
    images = glob.glob("images/*.png")
    objPoints = []
    imgPoints = []
    gray = 0
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret , corners = cv2.findChessboardCorners(gray , (7,6) , None)
        if ret:
            objPoints.append(objP)
            corners2 = cv2.cornerSubPix(gray , corners , (11 , 11) , (-1 , -1) , criteria)
            imgPoints.append(corners)
            print "processed ", fname
    ret , mtx , dist , rvecs , tvecs = cv2.calibrateCamera(objPoints , imgPoints , gray.shape[::-1] , None , None)
    np.savez("calibration" , mtx=mtx , dist = dist)
if __name__ == "__main__":
    cap = cv2.VideoCapture("tcp://192.168.1.1:5555")
    #cap = cv2.VideoCapture(0)
    npz = np.load("calibration.npz")
    mtx , dist = npz["mtx"] , npz["dist"]
    newcammtx = 0
    roi = 0


    if cap.isOpened() == False:
        cap.open("tcp://192.168.1.1:5555")
        #cap = cv2.VideoCapture(0)
    #calibrateCamera(cap)
    while True:
        ret , frame = cap.read()

        if ret:
            h , w = frame.shape[:2]
            newcammtx , roi = cv2.getOptimalNewCameraMatrix(mtx , dist , (w,h) , 0.8 , (w,h))
            break
    #collectGoodImages(cap)
    while True:
        ret , frame = cap.read()

        if ret:
            t0 = time.time()
            dst = cv2.undistort(frame.copy() , mtx , dist , None , newcammtx)
            x , y , w , h = roi
            dst = dst[y:y+h , x:x+w]
            t1 = time.time()
            #print (t1 - t0)*1000


            cv2.imshow("CALIB" , dst)
            cv2.imshow("ORIG" , frame)
            cv2.waitKey(1)



