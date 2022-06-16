
import threading
import time

from dataclasses import dataclass

@dataclass
class Influence:
    override = 1
    partial = 0.5
    dearth = 0


class Axis():
    def __init__(self, interval):
        self.interval = interval
        self.kp = -0.005
        self.ki = -0.01
        self.kd = -0.005
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
        self.offset = (self.offset + extent) % 360
        
    def shiftTargetRight(self):
        self.shiftTarget(90)

    def shiftTargetLeft(self):
        self.shiftTarget(-90)

    def tare(self):
        self.offset = self.errorHistory[-1]

class PIDController():
    def __init__(self, interval, controls=None, q=None):
        self.interval = interval
        self.controls = controls
        if controls == None:
            print("\nPIDController: Controls not connected\nUsing default value (0, 0, 0)\n")

        self.q = q
        

        self.pitch = Axis(interval)
        self.roll = Axis(interval)
        self.yaw = Axis(interval)

    def updateErrors(self, errors):
        self.yaw.update(errors[0])
        self.pitch.update(errors[1])
        self.roll.update(errors[2])

    def tareAll(self):
        try:
            self.updateErrors(self.controls.orientationData)
            print("Taring")
        except AttributeError:
            print("Tare failed. Controls likely not initialized")

        self.roll.tare()
        self.pitch.tare()
        self.yaw.tare()
        


    def collectData(self):
        self.lastReading = (0, 0, 0)
        while True:
            if self.controls != None:
                data = self.controls.orientationData
            else:
                data = (0, 0, 0)


            # self.q.put(["a", self.calcForces()])
            if data != self.lastReading:
                print(data)
                self.updateErrors(errors=data)
                self.q.put(["a", self.calcForces()])

                self.lastReading = (data[0], data[1], data[2])

            time.sleep(self.interval * 0.001)

    def calcForces(self):
        return (
            round(self.roll.force(), 5),
            round(self.pitch.force(), 5),
            round(self.yaw.force(), 5),
        )

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
    pidC.startListening()
