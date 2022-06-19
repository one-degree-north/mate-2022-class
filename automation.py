
from math import sqrt
import threading
import time

from message import Message


class RotationAxis():
    def __init__(self, interval, kp=-0.005, ki=-0.005, kd=-0.005):
        self.interval = interval
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.errorHistory = [0, 0] # test values only
        self.offset = 0 # positive value shifts the target rightward, negative leftward

    def force(self):
        p = self.kp * (self.errorHistory[-1] - self.offset)
        d = self.kd * (self.errorHistory[-1] - self.errorHistory[-2]) / self.interval
        return p + d

    def update(self, error):
        self.errorHistory.append(error)
        while len(self.errorHistory) > 2:
            self.errorHistory.remove(self.errorHistory[0])

    def shiftTarget(self, extent):
        """
        ABOUT YAW ONLY:
        extent < 0 for leftward shift
        extent > 0 for rightward shift
        """
        print(f"offset changed from {self.offset} to", end=" ")
        self.offset = (self.offset + extent) % 360
        print(f"{self.offset}")
        
    def tare(self):
        self.offset = self.errorHistory[-1]

class TranslationAxis():
    """
    at every given interval, append the accel data into a list
    when that list reaches an arbitrary length, say 100,
    the displacement is calculated and stored in an attribute. 
    the list is then cleared
    """

    def __init__(self, interval):
        self.interval = interval # in milliseconds

        self.accelHistory = []
        self.displacement = 0 # in meters

    def update(self, value):
        self.accelHistory.append(value)
        self.updateDisplacement()
        # print(self.displacement)

    def updateDisplacement(self):
        for value in self.accelHistory:
            self.displacement += 0.5 * value * (self.interval / 1000) * (self.interval / 1000)

class PIDController():
    def __init__(self, interval, controls=None, requestQueue=None):
        self.interval = interval
        self.controls = controls
        self.controlsConnected = controls != None
        if controls == None:
            print("\nMessage from PID Controller:\n\tControls not connected\n")

        self.requestQueue = requestQueue

        self.pitch = RotationAxis(interval)
        self.roll = RotationAxis(interval)
        self.yaw = RotationAxis(interval)


        self.lastOrientationReading = [0, 0, 0]
        # self.lastAccelReading       = [0, 0, 0]

        self.sendNewRequest = False
        self.isActive = True
        self.fullAuto = False

    def updateOrientation(self, orientationData=None):
        if self.controlsConnected:
            orientationData = self.controls.orientationData
        else:
            orientationData = [0, 0, 0]

        if orientationData != self.lastOrientationReading:
            self.yaw.update(orientationData[0])
            self.pitch.update(orientationData[1])
            self.roll.update(orientationData[2])

            self.lastOrientationReading = [orientationData[0], orientationData[1], orientationData[2]]
            self.sendNewRequest = True

    def updateDisplacements(self, accelData=None):
        if self.controlsConnected:
            accelData = self.controls.accelData
        else:
            accelData = [0, 0, 0]

        self.x.update(accelData[0])
        self.y.update(accelData[1])
        self.z.update(accelData[2])

        self.lastAccelReading = [accelData[0], accelData[1], accelData[2]]

    def planarDisplacement(self):
        return sqrt(self.x.displacement * self.x.displacement + self.y.displacement * self.y.displacement)

    def tareAll(self):
        self.roll.tare()
        self.pitch.tare()
        self.yaw.tare()

    def startReadingBNO(self):
        def updateInternalvalues():
            while True:
                self.updateOrientation()
                time.sleep(self.interval * 0.001)

        self.internalUpdateThread = threading.Thread(target=updateInternalvalues, daemon=True)
        self.internalUpdateThread.start()

    def startSendingRequests(self):
        def sendRequests():
            while True:

                if self.sendNewRequest and self.isActive:
                    self.requestQueue.put(
                        Message("automation", {"reqMotion": self.calcForces()})
                    )
                    self.sendNewRequest = False
                time.sleep(self.interval * 0.001)

        self.sendRequestsThread = threading.Thread(target=sendRequests, daemon=True)
        self.sendRequestsThread.start()

    def calcForces(self):
        return (
            round(self.roll.force(), 5),
            round(self.pitch.force(), 5),
            round(self.yaw.force(), 5),
        )

    def shiftTargetRight(self):
        self.yaw.shiftTarget(90)
        self.sendNewRequest = True

    def shiftTargetLeft(self):
        self.yaw.shiftTarget(-90)
        self.sendNewRequest = True

    def start(self):
        self.startReadingBNO()
        self.startSendingRequests()
        pass


if __name__ == "__main__":
    # from controls import Controls
    import queue
    
    pidC = PIDController(10, controls=None, requestQueue=queue.Queue())
    pidC.start()
