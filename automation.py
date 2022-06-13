


# from thrusters import *
from queue import Queue
from time import sleep

class Automator():

    controls = None
    q: Queue = None
    
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
            d = self.kd * (self.errorHistory[-1] - self.errorHistory[-2]) / self.interval
            # d = self.kd * (self.errorHistory[-2] - self.errorHistory[-1]) / self.interval
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


    def __init__(self, interval, dataGetter=None):
        self.interval = interval
        # self.dataGetter = dataGetter
        # self.dataGetter = Controls()
        # self.dataGetter.setOrientationAutoreport(self.interval * 0.1)
        # self.dataGetter.comms.startThread()

        self.pitch = self.Axis(interval)
        self.roll = self.Axis(interval)
        self.yaw = self.Axis(interval)

        self.forces()

    def collectErrors(self, errors):
        errors = self.controls.orientationData
        self.yaw.update(errors[0])
        self.pitch.update(errors[1])
        self.roll.update(errors[2])
        # sleep(self.interval * 0.001)

        # self.collectErrors()

    @classmethod
    def addToQ(cls, stuff):
        cls.q.put(stuff)

    def forces(self, errors):
        while True:
            self.collectErrors(errors)
            # return (self.roll.force(), self.pitch.force(), self.yaw.force())
            self.addToQ(
                (self.roll.force(), self.pitch.force(), self.yaw.force()),
            )
            print(self.q.get())
            

            sleep(1)



# control = Controls()
# control.setOrientationAutoreport(1)
# control.comms.startThread()
# while True:
#     print(control.orientationData)


test = Automator(10)


