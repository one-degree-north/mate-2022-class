
from math import sqrt
import threading
import time

from dataclasses import dataclass


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
    def __init__(self, interval, controls=None, q=None):
        self.interval = interval
        self.controls = controls
        self.controlsConnected = controls != None
        self.q = q

        self.pitch = RotationAxis(interval, kp=-0.01)
        self.roll = RotationAxis(interval, kp=-0.01)
        self.yaw = RotationAxis(interval)

        self.x = TranslationAxis(interval)
        self.y = TranslationAxis(interval)
        self.z = TranslationAxis(interval)

        # assumes zero roll and pitch and zero initial velocity
        self.displacement = 0

        self.lastOrientationReading = [0, 0, 0]
        self.lastAccelReading       = [0, 0, 0]

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
        # self.updateOrientation()
        self.roll.tare()
        self.pitch.tare()
        self.yaw.tare()

    def updateEverything(self):
        while True:
            self.updateOrientation()
            self.updateDisplacements()
            # print(self.planarDisplacement())
            time.sleep(self.interval * 0.001)

    def startInternalUpdater(self):
        self.internalUpdater = threading.Thread(target=self.updateEverything, daemon=True)
        self.internalUpdater.start()

    def sendRequests(self):
        while True:
            if self.sendNewRequest and self.isActive:
                # print("changing")
                self.q.put(["a", self.calcForces()])
                self.sendNewRequest = False
            
            time.sleep(self.interval * 0.001)

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

    def startListening(self):
        self.startInternalUpdater()
        self.bnoEar = threading.Thread(target=self.sendRequests, daemon=True)
        self.bnoEar.start()




if __name__ == "__main__":
    from controls import Controls
    import queue
    
    # test = MotionController(1000)
    # test.accelHistory = [10, 9, 8]
    # test.updateDisplacement()
    # print(test.displacement)
    # test.startReadingAccel()

    controls = Controls()
    controls.setOrientationAutoreport(1)
    controls.setAccelAutoreport(1)
    controls.comms.startThread()
    
    pidC = PIDController(10, controls=controls, q=queue.Queue())
    # pidC = PIDController(10, q=queue.Queue())
    # pidC.updateDisplacements()
    # print(pidC.getPlanarDisplacement())
    # pidC.updateOrientation([0, 0, 0])
    # pidC.updateDisplacement([1,1,1])
    # pidC.updateErrors([0, 0, 0])
    # pidC.updateErrors([0, 0, 0])

    # pidC.shiftTargetLeft()
    # print(pidC.yaw.offset)
    # print(pidC.yaw.force())

    pidC.startListening()

    # t = Axis(10)
    # print(t.force())
