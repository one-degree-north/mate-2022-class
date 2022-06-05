from dataclasses import dataclass
from math import sin, cos, tanh, degrees, radians


from thrusters import *
from time import sleep

class Automation():

    class Axis():
        def __init__(self, interval):
            self.interval = interval
            self.kp = 0.01
            self.ki = 0.01
            self.kd = 0.01
            self.errorHistory = [50, 25, 15, 10] # test values only

        def force(self):
            p = self.kp * self.errorHistory[-1]
            d = self.kd * (self.errorHistory[-1] + self.errorHistory[-2]) / self.interval
            return p + d


    def __init__(self, interval):
        self.pitch = self.Axis(interval)
        self.roll = self.Axis(interval)

        print(self.pitch.force())


test = Automation(10)


