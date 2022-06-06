from dataclasses import dataclass
from math import sin, cos, tanh, degrees, radians


# from thrusters import *
from time import sleep

class Automation():
    

    class Axis():
        axes = []
        def __init__(self, interval, type=None):
            self.interval = interval
            self.type = type # may not be needed
            self.kp = 0.01
            self.ki = 0.01
            self.kd = 0.01
            self.errorHistory = [50, 25, 15, 10] # test values only
            self.axes.append(self)
            

        def force(self):
            p = self.kp * self.errorHistory[-1]
            d = self.kd * (self.errorHistory[-1] + self.errorHistory[-2]) / self.interval
            return p + d

        def update(self, error):
            self.errorHistory.append(error)
            # while len(self.errorHistory) > 2:
            #     self.errorHistory.remove(self.errorHistory[0])
            # ^ may conserve memory

        @classmethod
        def updateErrors(cls, error: tuple):
            for axis in cls.axes:
                axis.update()

        @classmethod
        def send(self):
            """
            send to thrusters
            """
            pass


    def __init__(self, interval):
        self.pitch = self.Axis(interval)
        self.roll = self.Axis(interval)
        self.yaw = self.Axis(interval)

        print(self.pitch.force())

    def collectErrors(self):
        errors = getStuffFromControls.py
        self.Axis.updateErrors(errors)
        self.Axis.send()

        sleep(0.010)

        self.collectErrors()


test = Automation(10)


