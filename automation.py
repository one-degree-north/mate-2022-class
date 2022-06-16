
import threading
import time

from dataclasses import dataclass

@dataclass
class Influence:
    override = 1
    partial = 0.5
    dearth = 0


class Axis():
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
        # print(f"{p = }")
        # print(f"{d = }")
        return p + d
        # return p

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

class PIDController():
    def __init__(self, interval, controls=None, q=None):
        self.interval = interval
        self.controls = controls
        if controls == None:
            print("\nPIDController: Controls not connected\nUsing default value (0, 0, 0)\n")

        self.q = q
        self.recalculate = False

        self.pitch = Axis(interval, kp=-0.1)
        self.roll = Axis(interval, kp=-0.1)
        self.yaw = Axis(interval)

    def updateErrors(self, errors):
        self.yaw.update(errors[0])
        self.pitch.update(errors[1])
        self.roll.update(errors[2])

    def tareAll(self):
        try:
            self.updateErrors(self.controls.orientationData)
        except AttributeError:
            print("\nTare failed. Controls likely not initialized\n")

        self.roll.tare()
        self.pitch.tare()
        self.yaw.tare()

    def collectData(self):
        self.lastReading = [0, 0, 0]
        while True:
            if self.controls != None:
                data = self.controls.orientationData
            else:
                data = [0, 0, 0]
            # print(self.calcForces())
            # print(f"{data = }")
            # print(f"{self.lastReading = }\n")

            # self.q.put(["a", self.calcForces()])
            if data != self.lastReading or self.recalculate:
                # print("a", data)
                self.updateErrors(errors=data)
                self.q.put(["a", self.calcForces()])
                self.lastReading = [data[0], data[1], data[2]]
                self.recalculate = False
            time.sleep(self.interval * 0.001)

    def calcForces(self):
        return (
            round(self.roll.force(), 5),
            round(self.pitch.force(), 5),
            round(self.yaw.force(), 5),
        )

    def shiftTargetRight(self):
        self.recalculate = True
        self.yaw.shiftTarget(90)

    def shiftTargetLeft(self):
        self.recalculate = True
        self.yaw.shiftTarget(-90)


    def startListening(self):
        self.bnoEar = threading.Thread(target=self.collectData)
        self.bnoEar.start()




if __name__ == "__main__":
    from controls import Controls
    import queue
    
    # controls = Controls()
    # controls.setOrientationAutoreport(1)
    # controls.comms.startThread()
    
    pidC = PIDController(10, controls=None, q=queue.Queue())
    # pidC.updateErrors([0, 0, 0])
    # pidC.updateErrors([0, 0, 0])

    pidC.shiftTargetLeft()
    # print(pidC.yaw.offset)
    # print(pidC.yaw.force())

    # pidC.startListening()

    # t = Axis(10)
    # print(t.force())
