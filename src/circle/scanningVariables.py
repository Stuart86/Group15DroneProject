'''
Created on 16. jun. 2018

@author: Lasse Alexander Jensen
'''



class HSVValues:
    def __init__(self, lowMaskLowHue, lowMaskHighHue, lowMaskLowSat, lowMaskHighSat, lowMaskLowVal, lowMaskHighVal, \
                       highMaskLowHue, highMaskHighHue, highMaskLowSat, highMaskHighSat, highMaskLowVal, highMaskHighVal):
        self.lowMaskLowHue = lowMaskLowHue
        self.lowMaskHighHue = lowMaskHighHue
        self.lowMaskLowSat = lowMaskLowSat
        self.lowMaskHighSat = lowMaskHighSat
        self.lowMaskLowVal = lowMaskLowVal
        self.lowMaskHighVal = lowMaskHighVal
        
        self.highMaskLowHue = highMaskLowHue
        self.highMaskHighHue = highMaskHighHue
        self.highMaskLowSat = highMaskLowSat
        self.highMaskHighSat = highMaskHighSat
        self.highMaskLowVal = highMaskLowVal
        self.highMaskHighVal = highMaskHighVal

class LAPValues:
    def __init__(self, labLMin, labLMax, labAMin, labAMax, labBMin, labBMax):
        self.labLMin = labLMin
        self.labLMax = labLMax
        self.labAMin = labAMin
        self.labAMax = labAMax
        self.labBMin = labBMin
        self.labBMax = labBMax



class CircleSettings:
    def __init__(self, dp, minDist, param1, param2, minRadius, maxRadius, blur):
        self.dp = dp
        self.minDist = minDist
        self.param1 = param1
        self.param2 = param2
        self.minRadius = minRadius
        self.maxRadius = maxRadius
        self.blur = blur

class PILSettings:
    def __init__(self, cutoff, radius, percent, threshold):
        self.cutoff = cutoff
        self.radius = radius
        self.percent = percent
        self.threshold = threshold
        

# Normal circleScanning settings
normalDP = 20
normalMinDistance = 200
normalParam1 = 10
normalParam2 = 10
normalMinRadius = 40
normalMaxRadius = 1000
normalBlur = 5


#Circle 1
#HSV values
circle1lowMaskLowHue = 0
circle1lowMaskHighHue = 10
circle1lowMaskLowSat = 255
circle1lowMaskHighSat = 255
circle1lowMaskLowVal = 105
circle1lowMaskHighVal = 255

circle1highMaskLowHue = 150
circle1highMaskHighHue = 180
circle1highMaskLowSat = 75
circle1highMaskHighSat = 155
circle1highMaskLowVal = 175
circle1highMaskHighVal = 255

#LAP values   
circle1labLMin = 0
circle1labLMax = 135
circle1labAMin = 25
circle1labAMax = 125
circle1labBMin = 0
circle1labBMax = 255

#ImageSettings
circle1Cutoff = 20
circle1SRadius = 165
circle1SPercent = 1000
circle1SThresh = 15

#CircleSettingns
circle1Blur = 5
circle1DP = 10
circle1MinDist = 325





#Circle 2
#HSV values
circle2lowMaskLowHue = 0
circle2lowMaskHighHue = 10
circle2lowMaskLowSat = 0
circle2lowMaskHighSat = 255
circle2lowMaskLowVal = 0
circle2lowMaskHighVal = 255

circle2highMaskLowHue = 170
circle2highMaskHighHue = 180
circle2highMaskLowSat = 0
circle2highMaskHighSat = 255
circle2highMaskLowVal = 0
circle2highMaskHighVal = 255


#LAP values
circle2labLMin = 0
circle2labLMax = 0
circle2labAMin = 0
circle2labAMax = 0
circle2labBMin = 0
circle2labBMax = 0 

#ImageSettings
circle2Cutoff = 20
circle2SRadius = 165
circle2SPercent = 1000
circle2SThresh = 15

#CircleSettingns
circle2Blur = 5
circle2DP = 10
circle2MinDist = 325

#Circle 3
#HSV values
circle3lowMaskLowHue = 0
circle3lowMaskHighHue = 10
circle3lowMaskLowSat = 0
circle3lowMaskHighSat = 255
circle3lowMaskLowVal = 0
circle3lowMaskHighVal = 255

circle3highMaskLowHue = 170
circle3highMaskHighHue = 180
circle3highMaskLowSat = 0
circle3highMaskHighSat = 255
circle3highMaskLowVal = 0
circle3highMaskHighVal = 255
#LAP values
circle3labLMin = 0
circle3labLMax = 0
circle3labAMin = 0
circle3labAMax = 0
circle3labBMin = 0
circle3labBMax = 0 

#ImageSettings
circle3Cutoff = 20
circle3SRadius = 165
circle3SPercent = 1000
circle3SThresh = 15

#CircleSettingns
circle3Blur = 5
circle3DP = 10
circle3MinDist = 325


#Circle 4
#HSV values
circle4lowMaskLowHue = 0
circle4lowMaskHighHue = 10
circle4lowMaskLowSat = 0
circle4lowMaskHighSat = 255
circle4lowMaskLowVal = 0
circle4lowMaskHighVal = 255

circle4highMaskLowHue = 170
circle4highMaskHighHue = 180
circle4highMaskLowSat = 0
circle4highMaskHighSat = 255
circle4highMaskLowVal = 0
circle4highMaskHighVal = 255
#LAP values
circle4labLMin = 0
circle4labLMax = 0
circle4labAMin = 0
circle4labAMax = 0
circle4labBMin = 0
circle4labBMax = 0 

#ImageSettings
circle4Cutoff = 20
circle4SRadius = 165
circle4SPercent = 1000
circle4SThresh = 15

#CircleSettingns
circle4Blur = 5
circle4DP = 10
circle4MinDist = 325




#Circle 5
#HSV values
circle5lowMaskLowHue = 0
circle5lowMaskHighHue = 10
circle5lowMaskLowSat = 0
circle5lowMaskHighSat = 255
circle5lowMaskLowVal = 0
circle5lowMaskHighVal = 255

circle5highMaskLowHue = 170
circle5highMaskHighHue = 180
circle5highMaskLowSat = 0
circle5highMaskHighSat = 255
circle5highMaskLowVal = 0
circle5highMaskHighVal = 255
#LAP values
circle5labLMin = 0
circle5labLMax = 0
circle5labAMin = 0
circle5labAMax = 0
circle5labBMin = 0
circle5labBMax = 0 


#ImageSettings
circle5Cutoff = 20
circle5SRadius = 165
circle5SPercent = 1000
circle5SThresh = 15

#CircleSettingns
circle5Blur = 5
circle5DP = 10
circle5MinDist = 325


#Circle 6
#HSV values
circle6lowMaskLowHue = 0
circle6lowMaskHighHue = 10
circle6lowMaskLowSat = 0
circle6lowMaskHighSat = 255
circle6lowMaskLowVal = 0
circle6lowMaskHighVal = 255

circle6highMaskLowHue = 170
circle6highMaskHighHue = 180
circle6highMaskLowSat = 0
circle6highMaskHighSat = 255
circle6highMaskLowVal = 0
circle6highMaskHighVal = 255
#LAP values
circle6labLMin = 0
circle6labLMax = 0
circle6labAMin = 0
circle6labAMax = 0
circle6labBMin = 0
circle6labBMax = 0 

#ImageSettings
circle6Cutoff = 20
circle6SRadius = 165
circle6SPercent = 1000
circle6SThresh = 15

#CircleSettingns
circle6Blur = 5
circle6DP = 10
circle6MinDist = 325


def getCircle1HSVValues():
    values = HSVValues(circle1lowMaskLowHue, circle1lowMaskHighHue, circle1lowMaskLowSat, circle1lowMaskHighSat, circle1lowMaskLowVal, circle1lowMaskHighVal, \
                 circle1highMaskLowHue, circle1highMaskHighHue, circle1highMaskLowSat, circle1highMaskHighSat, circle1highMaskLowVal, circle1highMaskHighVal)
    return values
    
    
def getCircle2HSVValues():
    values = HSVValues(circle2lowMaskLowHue, circle2lowMaskHighHue, circle2lowMaskLowSat, circle2lowMaskHighSat, circle2lowMaskLowVal, circle2lowMaskHighVal, \
                 circle2highMaskLowHue, circle2highMaskHighHue, circle2highMaskLowSat, circle2highMaskHighSat, circle2highMaskLowVal, circle2highMaskHighVal)
    return values
    
def getCircle3HSVValues():
    values = HSVValues(circle3lowMaskLowHue, circle3lowMaskHighHue, circle3lowMaskLowSat, circle3lowMaskHighSat, circle3lowMaskLowVal, circle3lowMaskHighVal, \
                 circle3highMaskLowHue, circle3highMaskHighHue, circle3highMaskLowSat, circle3highMaskHighSat, circle3highMaskLowVal, circle3highMaskHighVal)
    return values
    
def getCircle4HSVValues():
    values = HSVValues(circle4lowMaskLowHue, circle4lowMaskHighHue, circle4lowMaskLowSat, circle4lowMaskHighSat, circle4lowMaskLowVal, circle4lowMaskHighVal, \
                 circle4highMaskLowHue, circle4highMaskHighHue, circle4highMaskLowSat, circle4highMaskHighSat, circle4highMaskLowVal, circle4highMaskHighVal)
    return values
    
def getCircle5HSVValues():
    values = HSVValues(circle5lowMaskLowHue, circle5lowMaskHighHue, circle5lowMaskLowSat, circle5lowMaskHighSat, circle5lowMaskLowVal, circle5lowMaskHighVal, \
                 circle5highMaskLowHue, circle5highMaskHighHue, circle5highMaskLowSat, circle5highMaskHighSat, circle5highMaskLowVal, circle5highMaskHighVal)
    return values
    
def getCircle6HSVValues():
    values = HSVValues(circle6lowMaskLowHue, circle6lowMaskHighHue, circle6lowMaskLowSat, circle6lowMaskHighSat, circle6lowMaskLowVal, circle6lowMaskHighVal, \
                 circle6highMaskLowHue, circle6highMaskHighHue, circle6highMaskLowSat, circle6highMaskHighSat, circle6highMaskLowVal, circle6highMaskHighVal)
    return values
    
    
def getHSVValues(circleIndex):
    if circleIndex == 1:
        return getCircle1HSVValues()
    elif circleIndex == 2:
        return getCircle2HSVValues()
    elif circleIndex == 3:
        return getCircle3HSVValues()
    elif circleIndex == 4:
        return getCircle4HSVValues()
    elif circleIndex == 5:
        return getCircle5HSVValues()
    elif circleIndex == 6:
        return getCircle6HSVValues()
    


def getCircle1LAPValues():
    values = LAPValues(circle1labLMin, circle1labLMax, circle1labAMin, circle1labAMax, circle1labBMin, circle1labBMax)
    
    return values
def getCircle2LAPValues():
    values = LAPValues(circle2labLMin, circle2labLMax, circle2labAMin, circle2labAMax, circle2labBMin, circle2labBMax)
    
    return values
def getCircle3LAPValues():
    values = LAPValues(circle3labLMin, circle3labLMax, circle3labAMin, circle3labAMax, circle3labBMin, circle3labBMax)
    
    return values
def getCircle4LAPValues():
    values = LAPValues(circle4labLMin, circle4labLMax, circle4labAMin, circle4labAMax, circle4labBMin, circle4labBMax)
    
    return values
def getCircle5LAPValues():
    values = LAPValues(circle5labLMin, circle5labLMax, circle5labAMin, circle5labAMax, circle5labBMin, circle5labBMax)
    
    return values
def getCircle6LAPValues():
    values = LAPValues(circle6labLMin, circle6labLMax, circle6labAMin, circle6labAMax, circle6labBMin, circle6labBMax)
    
    return values

def getLAPValues(circleIndex):
    if circleIndex == 1:
        return getCircle1LAPValues()
    elif circleIndex == 2:
        return getCircle2LAPValues()
    elif circleIndex == 3:
        return getCircle3LAPValues()
    elif circleIndex == 4:
        return getCircle4LAPValues()
    elif circleIndex == 5:
        return getCircle5LAPValues()
    elif circleIndex == 6:
        return getCircle6LAPValues()



def getCircle1PILSettings():
    values = PILSettings(circle1Cutoff, circle1SRadius, circle1SPercent, circle1SThresh)
    return values
def getCircle2PILSettings():
    values = PILSettings(circle2Cutoff, circle2SRadius, circle2SPercent, circle2SThresh)
    return values
def getCircle3PILSettings():
    values = PILSettings(circle3Cutoff, circle3SRadius, circle3SPercent, circle3SThresh)
    return values
def getCircle4PILSettings():
    values = PILSettings(circle4Cutoff, circle4SRadius, circle4SPercent, circle4SThresh)
    return values
def getCircle5PILSettings():
    values = PILSettings(circle5Cutoff, circle5SRadius, circle5SPercent, circle5SThresh)
    return values
def getCircle6PILSettings():
    values = PILSettings(circle6Cutoff, circle6SRadius, circle6SPercent, circle6SThresh)
    return values


def getPILValues(circleIndex):
    if circleIndex == 1:
        return getCircle1PILSettings()
    elif circleIndex == 2:
        return getCircle2PILSettings()
    elif circleIndex == 3:
        return getCircle3PILSettings()
    elif circleIndex == 4:
        return getCircle4PILSettings()
    elif circleIndex == 5:
        return getCircle5PILSettings()
    elif circleIndex == 6:
        return getCircle6PILSettings()


    #def __init__(self, dp, minDist, param1, param2, minRadius, maxRadius, blur):

def getCircle1CircleSettings():
    values = CircleSettings(circle1DP, circle1MinDist, normalParam1, normalParam2, normalMinRadius, normalMaxRadius, circle1Blur)
    return values
def getCircle2CircleSettings():
    values = CircleSettings(circle2DP, circle2MinDist, normalParam1, normalParam2, normalMinRadius, normalMaxRadius, circle2Blur)
    return values
def getCircle3CircleSettings():
    values = CircleSettings(circle3DP, circle3MinDist, normalParam1, normalParam2, normalMinRadius, normalMaxRadius, circle3Blur)
    return values
def getCircle4CircleSettings():
    values = CircleSettings(circle4DP, circle4MinDist, normalParam1, normalParam2, normalMinRadius, normalMaxRadius, circle4Blur)
    return values
def getCircle5CircleSettings():
    values = CircleSettings(circle5DP, circle5MinDist, normalParam1, normalParam2, normalMinRadius, normalMaxRadius, circle5Blur)
    return values
def getCircle6CircleSettings():
    values = CircleSettings(circle6DP, circle6MinDist, normalParam1, normalParam2, normalMinRadius, normalMaxRadius, circle6Blur)
    return values



def getCircleValues(circleIndex):
    if circleIndex == 1:
        return getCircle1CircleSettings()
    elif circleIndex == 2:
        return getCircle2CircleSettings()
    elif circleIndex == 3:
        return getCircle3CircleSettings()
    elif circleIndex == 4:
        return getCircle4CircleSettings()
    elif circleIndex == 5:
        return getCircle5CircleSettings()
    elif circleIndex == 6:
        return getCircle6CircleSettings()


    
    
    