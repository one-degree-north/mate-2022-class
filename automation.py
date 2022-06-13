
import threading
import time

class Axis():
    def __init__(self, interval):
        self.interval = interval
        self.kp = 0.01
        self.ki = 0.01
        self.kd = 0.01
        self.errorHistory = [0, 0, 0] # test values only

    def force(self):
        p = self.kp * self.errorHistory[-1]
        d = self.kd * (self.errorHistory[-1] - self.errorHistory[-2]) / self.interval
        # d = self.kd * (self.errorHistory[-2] - self.errorHistory[-1]) / self.interval
        
        return p + d

    def update(self, error):
        self.errorHistory.append(error)
        while len(self.errorHistory) > 2:
            self.errorHistory.remove(self.errorHistory[0])


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
            except AttributeError:
                data = (0, 0, 0)
            if data != lastReading:
                # add data manager here

                self.updateErrors(errors=data)
                self.q.put(["a", self.calcForces()])
            
            lastReading = data
            time.sleep(self.interval * 0.001)

    def calcForces(self):
        print("Calculating")
        return (
            self.roll.force(),
            self.pitch.force(),
            self.yaw.force(),
        )

    def startListening(self):
        self.bnoEar = threading.Thread(target=self.collectData)
        self.bnoEar.start()



if __name__ == "__main__":
    pidC = PIDController(10)
    pidC.startListening()


