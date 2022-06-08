


# from thrusters import *
from time import sleep
from controls import Controls

class Automator():
    

    class Axis():
        axes = []
        def __init__(self, interval, type=None):
            self.interval = interval
            self.type = type # may not be needed
            self.kp = 0.01
            self.ki = 0.01
            self.kd = 0.01
            self.errorHistory = [0, 0, 0] # test values only
            self.axes.append(self)
            

        def force(self):
            p = self.kp * self.errorHistory[-1]
            d = self.kd * (self.errorHistory[-1] + self.errorHistory[-2]) / self.interval
            return p + d

        def update(self, error):
            self.errorHistory.append(error)
            while len(self.errorHistory) > 2:
                self.errorHistory.remove(self.errorHistory[0])
            # ^ may conserve memory

        # @classmethod
        # def updateErrors(cls, error: tuple):
        #     for axis in cls.axes:
        #         axis.update()

        # @classmethod
        # def send(self):
        #     """
        #     send to thrusters
        #     """
        #     pass


    def __init__(self, interval, dataGetter):
        self.interval = interval
        self.dataGetter = dataGetter
        # self.dataGetter = Controls()
        # self.dataGetter.setOrientationAutoreport(self.interval * 0.1)
        # self.dataGetter.comms.startThread()

        self.pitch = self.Axis(interval)
        self.roll = self.Axis(interval)
        self.yaw = self.Axis(interval)

    def collectErrors(self):
        errors = self.dataGetter.orientationData
        self.yaw.update(errors[0])
        self.pitch.update(errors[1])
        self.roll.update(errors[2])
        # sleep(self.interval * 0.001)

        # self.collectErrors()

    def forces(self):
        return (self.roll.force(), self.pitch.force(), self.yaw.force)

# control = Controls()
# control.setOrientationAutoreport(1)
# control.comms.startThread()
# while True:
#     print(control.orientationData)


# test = Automation(10)


