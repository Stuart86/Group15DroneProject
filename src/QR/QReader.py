

import math
import time

import cv2
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode

import numpy as np


NORTH_ORIENTATION  = 0
SOUTH_ORIENTATION = 1
EAST_ORIENTATION = 2
WEST_ORIENTATION = 3
#QRSide = 11.55 ##For small A4 QR
#Pixels = 314.344413374 #For small qr and webcam
#PixelPerCm = Pixels/QRSide ##For webcam
#distanceCm = 30 #for small qr
QRSide = 19.6 #For A3 QR
Pixels = 224.75 #For Drone camera
PixelPerCm = Pixels/QRSide
distanceCm = 45 #For drone camera
FocalLength = 709.107575363 #In pixels for drone cam (different than Focal)
horizontalAngleOfView = 84.1352126
verticalAngleOfView = 53.8320221
Focal = PixelPerCm*distanceCm*QRSide
dict = {"P.00" : 102 , "P.01":101 , "P.02": 90.5 , "P.03":90 , "P.04":120 , "P.05" : 0 , "P.06":81.5}

class Point():
    def __init__(self , x , y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(%d,%d)" % (self.x , self.y)
class QRresult():
    def __init__(self , data , (x,y) , distance , circleWidth):
        self.x = x
        self.y = y
        self.data = data
        self.distance = distance
        self.circleWidth = circleWidth
    def __str__(self):
        return "data=%s" % (self.data)


def determinant(x1 , x2 , y1 , y2):
    return x1*y2-x2*y1
def rotateCorners(corners , orientation):
    newCorners = [[] , [], [] , []]
    if orientation == NORTH_ORIENTATION:
        newCorners = corners
    elif orientation == WEST_ORIENTATION:
        newCorners[0] = corners[3]
        newCorners[1] = corners[0]
        newCorners[2] = corners[1]
        newCorners[3] = corners[2]
    elif orientation == EAST_ORIENTATION:
        newCorners[0] = corners[1]
        newCorners[1] = corners[2]
        newCorners[2] = corners[3]
        newCorners[3] = corners[0]
    else:
        newCorners[0] = corners[2]
        newCorners[1] = corners[3]
        newCorners[2] = corners[0]
        newCorners[3] = corners[1]

    return newCorners
def traverseHeiarchy(heiarchy , index , contours):
    triplets = []
    finderPatterns = []
    if len(heiarchy) < 3:
        return None
    for i in range(0 , len(heiarchy)-2 , 1):
        first = heiarchy[i]
        second = heiarchy[i+1]
        third = heiarchy[i+2]
        if(first[2] > -1):
            if(second[0] > -1):
                continue
            elif second[2] >-1:
                if(third[0]>-1):
                    i+=1
                    continue
                elif third[2]>-1:
                    i+=1
                    continue
                else:
                    i+=2
                    a1 = cv2.contourArea(contours[second[3]])/49
                    a2 = cv2.contourArea(contours[first[2]])/25
                    a3 = cv2.contourArea(contours[second[2]])/9
                    lowerBound = a1*0.80
                    upperBound = a1*1.20
                    if (a2 >= lowerBound and a2 <=upperBound) and (a3 >= lowerBound and a3 <=upperBound):
                        triplets.append(contours[second[3]])
                    nextI = heiarchy[first[3]][0]
                    if len(triplets)==3:
                        finderPatterns.append(triplets)
                        triplets = []
                        if nextI is not -1:
                            i = nextI
                        else:
                            return finderPatterns
    return finderPatterns
def distSq(pointA , pointB):
    x = (pointA.x-pointB.x)**2
    y = (pointA.y-pointB.y)**2
    return x+y
def distFromPointToLine(a, b, c, point):
    return (a * point.x + b * point.y + c) / math.sqrt(a * a + b * b)
def linearEquation(A , B):
    a = A.y-B.y
    b = B.x-A.x
    c = -b*B.y-a*B.x
    return a , b , c
def distFromPointToLine2(point1 , point2 , point0):
    a , b , c = linearEquation(point1 , point2)
    return distFromPointToLine(a , b , c , point0)
def directionVector(x0 , y0 , x1 , y1):
    return x1-x0 , y1-y0
def lineIntersection(A1 , A2 , B1 , B2):
    a1 , b1 , c1 = linearEquation(A1 , A2)
    a2 , b2 , c2 = linearEquation(B1 , B2)
    det = determinant(a1 , a2 , b1 , b2);
    if det == 0:
        return Point(-1 , -1)
    xdet = determinant(b1, b2 , c1 , c2)
    ydet = determinant(c1 , c2 , a1 , a2)
    x = xdet/det
    y = ydet/det

    return Point(x, y)
def getVertices(contour , slope):
    x,y,w,h = cv2.boundingRect(contour)
    middleY = y+h/2
    middleX = x+w/2
    rightX = x+w
    lowerY = y+h
    upperMiddle = Point(middleX , y)
    rightMiddle = Point(rightX , middleY)
    leftMiddle = Point(x , middleY)
    lowerMiddle = Point(middleX , lowerY)
    middle = Point(middleX , middleY)
    maxDist = [0 , 0, 0 , 0]
    verticies = [0 ,0 ,0 ,0 ]
    for point in contour:
        p = Point(point[0 , 0] , point[0 , 1])
        #Distance from point to vertical line in the middle of the rectangle
        distToVert = distFromPointToLine2(upperMiddle , lowerMiddle, p)
        #Distance from point to horizontal line in the middle of the rectangle
        distToHoriz = distFromPointToLine2(leftMiddle , rightMiddle, p)
        #Distance from point to middle of rectangle
        distToMiddle = distSq(p , middle)
        if distToVert > 0.0 and distToHoriz <= 0.0:
            if distToMiddle > maxDist[0]:
                maxDist[0]=distToMiddle
                verticies[0] = p
        elif distToVert <=0.0 and distToHoriz<= 0:
            if distToMiddle > maxDist[1]:
                maxDist[1]=distToMiddle
                verticies[1] = p
        elif distToVert <= 0.0 and distToHoriz > 0.0:
            if distToMiddle > maxDist[2]:
                maxDist[2]=distToMiddle
                verticies[2] = p
        elif distToVert > 0.0 and distToHoriz > 0.0:
            if distToMiddle > maxDist[3]:
                maxDist[3]=distToMiddle
                verticies[3] = p
    return verticies
def convertToPoints(contour):
    result = []
    for p in contour:
        result.append(Point(p[0][0] , p[0][1]))
    return result
def findAndReadQR(img):
    #cv2.imshow("Window" , img)
    results = decode(img, [ZBarSymbol.QRCODE])
    #cv2.imshow("Window" , img)
    closestQR = None
    for result in results:
        p1 = result[3][0]
        p2 = result[3][1]
        p3 = result[3][2]
        p4 = result[3][3]
        side1 = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
        side2 = math.sqrt((p1.x - p4.x) ** 2 + (p1.y - p4.y) ** 2)
        side3 = math.sqrt((p2.x - p3.x) ** 2 + (p2.y - p3.y) ** 2)
        side4 = math.sqrt((p3.x - p4.x) ** 2 + (p3.y - p4.y) ** 2)
        sideAvg = (side1 + side2 + side3 + side4)/4
        distance = Focal/sideAvg
        centerX = (p1.x + p2.x + p3.x + p4.x)/4
        centerY = (p1.y + p2.y + p3.y + p4.y)/4
        #ctr = np.array([centerX , centerY]).reshape((-1, 1, 2)).astype(np.int32)
        #corners = [[p1.x , p1.y], [p2.x , p2.y] , [p3.x , p3.y] , [p4.x , p4.y]]
        #corn2 = np.array(corners).reshape((-1, 1, 2)).astype(np.int32)
        #cv2.drawContours(img , [corn2] , 0 , (0 , 255 , 0) , 5)
        #cv2.drawContours(img , ctr , 0, (255 , 0 , 0) , 5)
        #cv2.putText(img, '1', (p1.x, p1.y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
        #cv2.putText(img, '2', (p2.x, p2.y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
        #cv2.putText(img, '3', (p3.x, p3.y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
        #cv2.putText(img, '4', (p4.x, p4.y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
        #cv2.imshow("Window" , img)
        print result[0]
        if result[0] not in dict:
            continue
        if closestQR == None:
            closestQR = QRresult(result[0] , (centerX , centerY) , distance, dict[result[0]])
        elif closestQR.distance > distance:
            closestQR = QRresult(result[0], (centerX, centerY), distance, dict[result[0]])
    #cv2.imshow("Window" , img)
    return closestQR
    grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(grayScale , (5,5) ,1)
    #blurred = cv2.medianBlur(grayScale , 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    grayScale = clahe.apply(grayScale)
    thresh = cv2.adaptiveThreshold(grayScale , 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 23, 4)
    cv2.imshow("Gray" , thresh)
    _ , cnts , heiarchy = cv2.findContours(thresh , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img , cnts, -1, (0, 255, 0), 3)
    qrResults = []
    if heiarchy is not None:
        #Go through contour heiarchy and find the 3 squares(Finder patterns) in the QR code
        allPatterns = traverseHeiarchy(heiarchy[0] , 0 , cnts)
        if allPatterns:#allPatterns contains sets of 3 finder patterns
            for patterns in allPatterns:
                bottom = 0
                right = 0
                orientation = -1
                #Use image moments to calculate the centers of the finder patterns and then figure out
                #which two of them are part of the longest side in the triangle
                M = [cv2.moments(patterns[0]), cv2.moments(patterns[1]) , cv2.moments(patterns[2])]
                centers = [Point(M[0]['m10']/M[0]['m00'] , M[0]['m01']/M[0]['m00']) ,
                            Point(M[1]['m10'] / M[1]['m00'], M[1]['m01']/M[1]['m00']),
                            Point(M[2]['m10'] / M[2]['m00'], M[2]['m01']/M[2]['m00'])]
                len1 = distSq(centers[0] , centers[1])
                len2 = distSq(centers[0] ,centers[2])
                len3 = distSq(centers[1] , centers[2])
                patternPoints = []
                for c in patterns:
                   patternPoints.append(convertToPoints(c))
                max = len1 if len1> len2 else len2
                max = len3 if len3 > max else max
                top = 1
                #Time to figure out the indice of the pattern that's top
                rm = [0,2]
                if max == len1:
                    top = 2
                    rm =[0,1]
                elif max == len2:
                    top = 1
                    rm = [0,2]
                elif max == len3:
                    top = 0
                    rm = [1,2]
                sideCenters = [centers[rm[0]] , centers[rm[1]]]

                #We'll use the equation for the line ax+by+c=0 to figure out how the qr code is oriented
                #Once we've figured that out we know which finder pattern is the "bottom" and the "right"
                a , b , c = linearEquation(sideCenters[0] , sideCenters[1])
                if b == 0:
                    continue
                dist = distFromPointToLine(a, b, c , centers[top])

                a = a/b
                if a > 0 and dist < 0:
                    orientation = NORTH_ORIENTATION
                    bottom = rm[0]
                    right = rm[1]
                elif a > 0 and dist > 0:
                    orientation = SOUTH_ORIENTATION
                    bottom = rm[1]
                    right = rm[0]
                elif a < 0 and dist > 0:
                    orientation = EAST_ORIENTATION
                    right = rm[0]
                    bottom = rm[1]
                elif a < 0 and dist < 0:
                    orientation = WEST_ORIENTATION
                    bottom = rm[0]
                    right = rm[1]

                #Now we want to find the 4 point in the finder pattern like if it was a square
                bottomVerticies = getVertices(patterns[bottom] , -a)
                rightVerticies = getVertices(patterns[right],-a)
                topVerticies = getVertices(patterns[top] , -a)
                #We'll rotate the points with respect to the orientation
                bottomVerticies = rotateCorners(bottomVerticies , orientation)
                rightVerticies = rotateCorners(rightVerticies, orientation)
                topVerticies = rotateCorners(topVerticies, orientation)

                lastCorner = lineIntersection(rightVerticies[1], rightVerticies[2], bottomVerticies[3],bottomVerticies[2])
                maxX = len(img[0])
                maxY = len(img)
                #This would mean that the entire qr code is not in the picture, so we can't read it
                if lastCorner.x < 0 or lastCorner.x >= maxX or lastCorner.y < 0 or lastCorner.y >= maxY:
                    #print "Possible QR Found"
                    continue

                qrCorners = [[topVerticies[0].x  , topVerticies[0].y], [rightVerticies[1].x , rightVerticies[1].y] ,
                             [bottomVerticies[3].x , bottomVerticies[3].y] , [lastCorner.x , lastCorner.y]]
                qrX = (qrCorners[0][0] + qrCorners[1][0] + qrCorners[2][0] + qrCorners[3][0]) / 4
                qrY = (qrCorners[0][1] + qrCorners[1][1] + qrCorners[2][1] + qrCorners[3][1]) / 4


                src = np.float32(qrCorners)
                dst = np.float32([[0,0],[300 , 0],[0 , 300],[300, 300]])
                ##We have to transform the part of the image where the qr code is, to something our qr reader can read
                matrix = cv2.getPerspectiveTransform(src, dst)

                final = cv2.warpPerspective(thresh , matrix , (300, 300))
                #cv2.imshow("Gray" , final)
                qrResult = decode(final , [ZBarSymbol.QRCODE])
                if len(qrResult) is not 0:
                    #circleWidthArray = [102, 101, 90.5, 90, 120, 0, 81.5]


                    #print "Width %d" % dict[text]

                    side1 = ((qrCorners[0][0]-qrCorners[1][0])**2 + (qrCorners[0][1]-qrCorners[1][1])**2)
                    side2 = (qrCorners[0][0]-qrCorners[2][0])**2 + (qrCorners[0][1]-qrCorners[2][1])**2
                    side3 = (qrCorners[1][0]-qrCorners[3][0])**2 + (qrCorners[1][1]-qrCorners[3][1])**2
                    side4 = (qrCorners[2][0] - qrCorners[3][0]) ** 2 + (qrCorners[2][1] - qrCorners[3][1]) ** 2
                    side1 = math.sqrt(side1)
                    side2 = math.sqrt(side2)
                    side3 = math.sqrt(side3)
                    side4 = math.sqrt(side4)
                    dist = Focal/((side1+side2+side3+side4)/4)
                    #nv = [np.array([[qrX, qrY], [qrX+normVec[0], qrY+normVec[1]]], dtype=np.int32)]
                    #cv2.drawContours(img, nv, -1, (0, 255, 0), 3)

                    text = qrResult[0][0]
                    if text in dict:
                        qrResults.append(QRresult(text, (qrX, qrY), dist, dict[text]))

                    #print "Circle width: ",dict[text], "cm"
                else:
                    #qrX = (qrCorners[0][0] + qrCorners[1][0] + qrCorners[2][0] + qrCorners[3][0]) / 4
                    #qrY = (qrCorners[0][1] + qrCorners[1][1] + qrCorners[2][1] + qrCorners[3][1]) / 4
                    #side1 = ((qrCorners[0][0] - qrCorners[1][0]) ** 2 + (qrCorners[0][1] - qrCorners[1][1]) ** 2)
                    #side2 = (qrCorners[0][0] - qrCorners[2][0]) ** 2 + (qrCorners[0][1] - qrCorners[2][1]) ** 2
                    #side1 = math.sqrt(side1)
                    #side2 = math.sqrt(side2)
                    #dist = Focal / ((side1 + side2) / 2)
                    #text = "CAN'T READ"
                    #qrResults.append(QRresult(text, (qrX, qrY), dist))
                    continue
    return qrResults
##This main is just for testing
def doStuff(img):
    res = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    h , s, v = cv2.split(res)
    res = clahe.apply(s)
    res = cv2.merge((h , res, v))
    res = cv2.cvtColor(res , cv2.COLOR_HSV2BGR)
    return np.hstack((img , res))


if __name__ == "__main__":
    cap = cv2.VideoCapture("tcp://192.168.1.1:5555")
    #cap = cv2.VideoCapture(0)
    cv2.namedWindow("Window" , cv2.WINDOW_AUTOSIZE)
    #cv2.namedWindow("Gray" , cv2.WINDOW_NORMAL)
    n = 0
    lastDistance = 50
    lastTime = time.time()
    if cap.isOpened() == False:
        cap.open("tcp://192.168.1.1:5555")
    while 1:

        ret , frame = cap.read()

        if ret:
            print len(frame[0])
            print len(frame)
            tBefore = time.time()
            #hsv = doStuff(frame)
            cv2.imshow("Window" , frame)
            #cv2.imshow("Window", hsv)
            results = findAndReadQR(frame)
            if results is not None:
                print results.x , " " , results.y

            tPassed = time.time() - tBefore
        cv2.waitKey(1)
    cap.release()


