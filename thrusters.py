"""
import this if thruster pin number is needed
don't need to keep making the same
variables in each file
"""

# from math import cos, sin, radians
import numpy as np
from joystick import Joystick, JoystickData
from time import sleep

import time


class Thruster:
    createdThrusters = []

    def __init__(self, pin, powerMatrix, position):
        self.pin = pin
        self.powerMatrix = powerMatrix
        self.position = (position[0], position[1], position[0])
        self.createdThrusters.append(self)

    def normalize(self, thrusterSpeeds: dict, reach):
        """
        reach is the maximum power that any one of the vertical thrusters can reach
        """
        # print(list(thrusterSpeeds.values())[0:3])
        greatest = max(list(thrusterSpeeds.values())[0:3])

        try:
            multiplier = reach / greatest
        except ZeroDivisionError:
            multiplier = 1

        for pin in thrusterSpeeds.keys():
            if pin in (4, 5): # a very ugly way of doing things, will correct later
                continue
            speed = thrusterSpeeds[pin]
            thrusterSpeeds[pin] = round(speed * multiplier, 3)

        return thrusterSpeeds

    def averager(self, speeds: list):
        if len(speeds) != 0:
            return round(sum(speeds) / len(speeds), 8)
        return 0

    def scale(self, thrusterSpeeds, multiplier):
        for pin in thrusterSpeeds.keys():
            speed = thrusterSpeeds[pin]
            thrusterSpeeds[pin] = round(speed * multiplier, 3)
        return thrusterSpeeds

    @property
    def axis(self) -> int:
        if sorted(self.powerMatrix)[-1] == 1 and sorted(self.powerMatrix)[-2] == 0:
            return self.powerMatrix.index(1)

    @property
    def isUp(self):
        return self.axis == 2
    
    @property
    def isSide(self):
        return self.axis == 0

    @property
    def isForward(self):
        return self.axis == 1

    @classmethod
    def determine(cls, intendedMotion: tuple, intendedRotation: tuple, multiplier: float):
        """
        intendedMotion -> [x, y, z]
        intendedRotation -> [roll, pitch, yaw]
            ordered this way so that attribute 'position' matches 
        """
        thrusterSpeeds = {}
        for thruster in cls.createdThrusters:
            thrusterSpeeds[thruster.pin] = []
        
        for thruster in cls.createdThrusters:
            # print(f"{thruster.position = }")
            # print(f"Appending {intendedMotion[thruster.axis]}")

            for axis, axisMotion in enumerate(intendedMotion):
                result = axisMotion * thruster.powerMatrix[axis]
                if result != 0:
                    thrusterSpeeds[thruster.pin].append(result)

            if thruster.isUp:
                for i in (0, 1):
                    result = -thruster.position[i] * thruster.powerMatrix[thruster.axis] * intendedRotation[i]
                    if result != 0:
                        thrusterSpeeds[thruster.pin].append(result)

            elif thruster.isForward:
                i = 2
                result = -thruster.position[i] * thruster.powerMatrix[thruster.axis] * intendedRotation[i]
                if result != 0:
                    thrusterSpeeds[thruster.pin].append(result)

            elif thruster.isSide:
                pass

        for pin in thrusterSpeeds.keys():
            speed = thrusterSpeeds[pin]
            thrusterSpeeds[pin] = cls.averager(cls, speed)

        # thrusterSpeeds = cls.scale(cls,cls.normalize(cls, thrusterSpeeds=thrusterSpeeds, reach=intendedMotion[-1]), multiplier)
        # thrusterSpeeds = cls.normalize(cls, thrusterSpeeds=thrusterSpeeds, reach=intendedMotion[-1])
        return thrusterSpeeds
    
    @classmethod
    def showSpeeds(self, intendedMotion, intendedRotation, multiplier):
        for pin, value in self.determine(intendedMotion, intendedRotation, multiplier).items():
            print(f"{pin = }, {value}")


start = time.time()

if __name__ == "__main__":
    
    frontL = Thruster(pin=0, powerMatrix=(0, 0, 1), position=(-1, 1))
    frontR = Thruster(pin=1, powerMatrix=(0, 0, 1), position=( 1, 1))
    backL  = Thruster(pin=2, powerMatrix=(0, 0, 1), position=(-1,-1))
    backR  = Thruster(pin=3, powerMatrix=(0, 0, 1), position=( 1,-1))
    sideL  = Thruster(pin=4, powerMatrix=(0, 1, 0), position=(-1, 0))
    sideR  = Thruster(pin=5, powerMatrix=(0, 1, 0), position=( 1, 0))
    for i in range(1000):
        Thruster.determine((0,0,1), (0.5, 0.25, 0), 1)

end = time.time()

totalTime = end - start
print("\n" + str(totalTime))


# if __name__ == "__main__":
#     joystick = Joystick()
#     while True:
#         joystick.readJoyData()
#         Thruster.showSpeeds((0, -joystick.joyData.yAxis, 0), (0, 0, 0), 1)








