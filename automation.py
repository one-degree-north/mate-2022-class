
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
        self.yaw = RotationAxis(interval)

        self.y = TranslationAxis(interval)




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
        # orientationData = self.controls.orientationData
        if orientationData != self.lastOrientationReading:
            # print("updateding")
            self.yaw.update(orientationData[0])
            self.pitch.update(orientationData[1])
            self.roll.update(orientationData[2])

            self.lastOrientationReading = [orientationData[0], orientationData[1], orientationData[2]]
            self.sendNewRequest = True
        # print(f"{self.lastOrientationReading = }")

    def updateDisplacement(self, accelData=None):
        # if self.controlsConnected:
        #     accelData = self.controls.accelData
        # else:
        #     accelData = [0, 0, 0]
        accelData = self.controls.accelData

        self.y.update(accelData[1])

        # self.lastAccelReading = [accelData[0], accelData[1], accelData[2]]
        print(f"{accelData = }")
        print(f"{self.y.displacement = }")

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
                self.updateDisplacement()

                time.sleep(self.interval * 0.001)

        self.internalUpdateThread = threading.Thread(target=updateInternalvalues, daemon=False)
        self.internalUpdateThread.start()

    def startSendingRequests(self):
        def sendRequests():
            while True:

                if self.sendNewRequest and self.isActive:
                    # print("sending")
                    self.requestQueue.put(
                        Message("automation", {"reqRotation": self.calcForces()})
                    )
                    self.sendNewRequest = False
                time.sleep(self.interval * 0.001)

        self.sendRequestsThread = threading.Thread(target=sendRequests, daemon=False)
        self.sendRequestsThread.start()

    def calcForces(self):
        return (
            round(self.roll.force(), 5),
            round(self.pitch.force(), 5),
            round(self.yaw.force(), 5),
        )

    def moveForward(self, reqDistance):
        self.initialDisplacement = self.y.displacement
        while (self.y.displacement - self.initialDisplacement) < reqDistance:
            # print("doing this")
            power = (reqDistance - 50 * abs(self.y.displacement - self.initialDisplacement)) / reqDistance
            # print(f"Difference: {power}")
            
            self.requestQueue.put(
                        Message("automation", {"reqRotation": (0, round(power, 2), 0)})
                    )
            time.sleep(self.interval * 0.001)
        self.requestQueue.put(
                        Message("automation", {"reqRotation": (0, 0, 0)})
                    )

    def shiftTargetRight(self):
        self.yaw.shiftTarget(90)
        self.sendNewRequest = True

    def shiftTargetLeft(self):
        self.yaw.shiftTarget(-90)
        self.sendNewRequest = True

    def start(self):
        self.startReadingBNO()
        time.sleep(1)
        moveThread = threading.Thread(target=self.moveForward, args=(1, ))
        moveThread.start()
        # self.startSendingRequests()
        pass


if __name__ == "__main__":
    from controls import Controls
    import queue
    # controls = None
    controls = Controls(onshoreEnabled=False)
    # controls.comms.startThread()
    
    pidC = PIDController(10, controls=controls, requestQueue=queue.Queue())
    pidC.start()
