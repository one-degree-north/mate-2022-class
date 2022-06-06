"""
import this if thruster pin number is needed
don't need to keep making the same
variables in each file
"""

# from math import cos, sin, radians



class Thruster:
    createdThrusters = []

    def __init__(self, pin, powerMatrix, position):
        self.pin = pin
        self.powerMatrix = powerMatrix
        self.position = (position[0], position[1], position[0])
        self.createdThrusters.append(self)

    def normalize(self, thrusterSpeeds: dict, reach):
        """
        the reach is the maximum power that any one of the vertical thrusters can reach
        """
        greatest = max(list(thrusterSpeeds.values())[0:3])
        multiplier = reach / greatest

        for pin in thrusterSpeeds.keys():
            if pin in (4, 5): # a very ugly way of doing things, will correct later
                continue
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
    def determine(cls, intendedMotion: tuple, intendedRotation: tuple):
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

        for thruster in cls.createdThrusters:
            speeds = thrusterSpeeds[thruster.pin]
            try:
                avg = sum(speeds) / len(speeds)
            except ZeroDivisionError:
                avg = sum(speeds) / 1
            thrusterSpeeds[thruster.pin] = round(avg, 3)
        
        thrusterSpeeds = cls.normalize(cls, thrusterSpeeds, intendedMotion[-1])

        return thrusterSpeeds



    
frontL = Thruster(pin=0, powerMatrix=(0, 0, 1), position=(-1, 1))
frontR = Thruster(pin=1, powerMatrix=(0, 0, 1), position=( 1, 1))
backL  = Thruster(pin=2, powerMatrix=(0, 0, 1), position=(-1,-1))
backR  = Thruster(pin=3, powerMatrix=(0, 0, 1), position=( 1,-1))
sideL  = Thruster(pin=4, powerMatrix=(0, 1, 0), position=(-1, 0))
sideR  = Thruster(pin=5, powerMatrix=(0, 1, 0), position=( 1, 0))

for thrusterPin, k, in Thruster.determine((0, 0, 1), (0.5, 0.5, 0.5)).items():
    print(f"{thrusterPin=} ->", k)
    pass



