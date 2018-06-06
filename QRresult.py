class QRresult():
    def __init__(self , data , (x,y) , distance , circleWidth):
        self.x = x
        self.y = y
        self.data = data
        self.distance = distance
        self.circleWidth = circleWidth
    def __str__(self):
        return "data=%s" % (self.data)