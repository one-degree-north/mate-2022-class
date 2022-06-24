
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
        self.targetValue = 0 # positive value shifts the target rightward, negative leftward

    def force(self):
        p = self.kp * (self.errorHistory[-1] - self.targetValue)
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
        print(f"targetValue changed from {self.targetValue} to", end=" ")
        self.targetValue = (self.targetValue + extent) % 360
        print(f"{self.targetValue}")
        time.sleep(0.25) # not ideal, can't find a fix right now...
        
    def tare(self):
        self.targetValue = self.errorHistory[-1]

class TranslationAxis():
    """
    at every given interval, append the accel data into a list
    when that list reaches an arbitrary length, say 100,
    the displacement is calculated and stored in an attribute. 
    the list is then cleared
    """

    def __init__(self, interval):
        self.interval = interval # in milliseconds
        self.displacement = 0 # in meters

    def update(self, value):
        self.displacement += 0.5 * value * (self.interval / 1000) * (self.interval / 1000)
        # print(f"dy: {self.displacement}")


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
        self.yaw = RotationAxis(interval, kp=-0.001)

        self.y = TranslationAxis(interval)




        self.lastOrientationReading = [0, 0, 0]
        # self.lastAccelReading       = [0, 0, 0]

        self.sendNewRequest = False
        self.isActive = True
        self.fullAuto = False
        self.override = False

    def updateOrientation(self, orientationData=None):
        if self.controlsConnected:
            orientationData = self.controls.orientationData
        else:
            orientationData = [0, 0, 0]
        # print("heloooooooooooooooooo\n\n\n\n")
        print(f"Orientation Data from controls: {self.controls.orientationData}")
        # orientationData = self.controls.orientationData
        if orientationData != self.lastOrientationReading:
            # print("updateding")

            # old values
            # self.yaw.update(orientationData[0])
            # self.pitch.update(orientationData[1])
            # self.roll.update(orientationData[2])

            self.yaw.update(orientationData[0])
            self.pitch.update(orientationData[2])
            self.roll.update(-orientationData[1])   

            self.lastOrientationReading = [orientationData[0], orientationData[1], orientationData[2]]
            self.sendNewRequest = True
        # print(f"{self.lastOrientationReading = }")

    def updateDisplacement(self, accelData=None):
        if self.controlsConnected:
            accelData = self.controls.accelData
        else:
            accelData = [0, 1, 0]
        # accelData = self.controls.accelData

        self.y.update(accelData[1])

        # self.lastAccelReading = [accelData[0], accelData[1], accelData[2]]
        # print(f"{accelData = }")
        # print(f"{self.y.displacement = }")

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
                # self.updateDisplacement()

                time.sleep(self.interval * 0.001)

        self.internalUpdateThread = threading.Thread(target=updateInternalvalues, daemon=True)
        self.internalUpdateThread.start()

    def startSendingRequests(self):
        def sendRequests():
            while True:
                if self.override:
                    self.moveForward()

                if self.sendNewRequest and self.isActive:
                    # print("sending")
                    self.requestQueue.put(
                        Message("automation", {"reqRotation": self.calcForces(), "reqMotion": None})
                    )
                    self.sendNewRequest = False
                time.sleep(self.interval * 0.001)

        self.sendRequestsThread = threading.Thread(target=sendRequests, daemon=True)
        self.sendRequestsThread.start()

    def calcForces(self):
        return (self.roll.force(),
                self.pitch.force(),
                self.yaw.force(),)

    def moveForward(self):
        while self.override:
            self.requestQueue.put(Message("automation", {"reqMotion": (0, 1, 0), "reqRotation": self.calcForces()}))
            print("Moving forward")
        print("Finished!\n\n")

    def shiftTargetRight(self):
        self.yaw.shiftTarget(90)
        self.sendNewRequest = True

    def shiftTargetLeft(self):
        self.yaw.shiftTarget(-90)
        self.sendNewRequest = True

    def shiftTargetBy(self, degrees):
        self.yaw.shiftTarget(degrees)
        self.sendNewRequest = True

    def start(self):
        self.startReadingBNO()
        # time.sleep(1)
        # moveThread = threading.Thread(target=self.moveForward, args=(1, ))
        # moveThread.start()
        self.startSendingRequests()
        pass


if __name__ == "__main__":
    from controls import Controls
    import queue
    controls = None
    controls = Controls(onshoreEnabled=False)
    # controls.comms.startThread()
    
    pidC = PIDController(10, controls=controls, requestQueue=queue.Queue())
    pidC.start()
