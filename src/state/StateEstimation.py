
import numpy as np
import threading
import math
import time
g = 9.816 # mm / s
RAD2DEG = 57.2957795131
DEG2RAD = 0.01745329251
euler_max = 0.20943952 #Radians
yaw_max_speed = 1.7453293 #Radians / second
vz_max = 0.700 #m / second
drone_weight = 0.425 #Kg

class StateEstimator:


    def __init__(self , x , y , z , vx , vy , vz, yaw , pitch , roll, baseTime):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        #self.ax = ax
        #self.ay = ay
        self.t = baseTime #Time of last measurement
        self.yawDriftCoeff = 0.007072266
        self.lock = threading.Lock()
        self.yawDriftObs = []
        self.yawDriftIter = 0

    def time_update(self, lr , bf , ud , rot , dt):
        self.lock.acquire()
        self.t = time.time()
        self.yaw = self.yaw + rot * yaw_max_speed * dt * RAD2DEG - self.yawDriftCoeff * dt
        self.roll = lr*euler_max
        self.pitch = bf*euler_max
        cyaw = math.cos(self.yaw)
        sp = math.sin(self.pitch)
        sr = math.sin(self.roll)
        syaw = math.sin(self.yaw)
        #self.ax = (cyaw*sp + syaw*sr)*g
        #self.ay = (syaw*sp - cyaw*sr)*g
        self.vx = self.vx# + self.ax*dt
        self.vy = self.vy# + self.ay*dt
        self.vz = ud*vz_max
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        self.z = self.z = self.vz*dt
        self.lock.release()

    def measurement_update(self , vx , vy , yaw , pitch, roll , altitude):
        self.lock.acquire()
        t0 = time.time()
        dt = t0 - self.t
        if dt == 0:
            self.lock.release()
            return
        self.t = t0
        vx /= float(1000)
        vy /= float(1000)
        altitude /= float(1000)
        self.pitch = pitch*DEG2RAD
        self.yaw = yaw*DEG2RAD - self.yawDriftCoeff*dt
        self.roll = roll*DEG2RAD
        cyaw = math.cos(self.yaw)
        sp = math.sin(self.pitch)
        sr = math.sin(self.roll)
        syaw = math.sin(self.yaw)
        #self.ax = (cyaw * sp + syaw * sr) * g
        #self.ay = (syaw * sp - cyaw * sr) * g
        self.vx = vx*cyaw + vy*syaw
        self.vy = vx*syaw - vy*cyaw
        self.vz = (altitude - self.z)/dt
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        self.z = altitude
        self.lock.release()

    def getState(self):
        self.lock.acquire()
        data = [self.x , self.y , self.z , self.vx , self.vy , self.vz , self.yaw , self.pitch , self.roll]
        self.lock.release()
        return data

