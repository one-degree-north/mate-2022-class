
import threading
import time

class Axis():
    def __init__(self, interval):
        self.interval = interval
        self.kp = -0.005
        # self.ki = -0.01
        self.kd = -0.005
        self.errorHistory = [0, 90] # test values only
        self.offset = 0 # positive value shifts the target rightward, negative leftward

    def force(self):
        p = self.kp * (self.errorHistory[-1] - self.offset)
        d = self.kd * (self.errorHistory[-1] - self.errorHistory[-2]) / self.interval
        # print(f"{p = }, {d = }")
        # print(f"Without derivative: {p}")
        # print(f"With derivative: {p + d}")
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
        self.offset = (self.offset + extent) % 360
        
    def shiftTargetRight(self):
        self.shiftTarget(90)

    def shiftTargetLeft(self):
        self.shiftTarget(-90)

class PIDController():
    def __init__(self, interval, controls=None, q=None):
        self.interval = interval
        self.controls = controls
        self.q = q

        self.pitch = Axis(interval)
        self.roll = Axis(interval)
        self.yaw = Axis(interval)

    def updateErrors(self, errors):
        self.yaw.update(errors[0])
        self.pitch.update(errors[1])
        self.roll.update(errors[2])


    def collectData(self):
        lastReading = None
        while True:
            try:
                data = self.controls.orientationData
            except AttributeError: # controls still None
                data = (0, 0, 0)
            print(data)
            if data != lastReading:
                # add data manager here

                self.updateErrors(errors=data)
                self.q.put(["a", self.calcForces()])
            
            lastReading = data
            time.sleep(self.interval * 0.001)

    def calcForces(self):
        return (
            self.roll.force(),
            self.pitch.force(),
            self.yaw.force(),
        )

    def startListening(self):
        self.bnoEar = threading.Thread(target=self.collectData)
        self.bnoEar.start()

from controls import Controls
import queue


if __name__ == "__main__":
    controls = Controls()

    pidC = PIDController(10, controls=controls, q=queue.Queue())
    pidC.startListening()

    # yaw = Axis(10)
    # yaw.errorHistory = [20, 50]
    # print(yaw.force())




