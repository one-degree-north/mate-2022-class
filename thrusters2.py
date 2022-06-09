
import numpy as np

class Thruster():
    multiplier = 1
    thrusters = []

    def __init__(self, pin, power, position):
        self.pin = pin
        self.power = np.array(
            [[power[0]],
             [power[1]],
             [power[2]]]) 
        self.position = np.array(
            [[position[0], 0, 0],
             [0, position[1], 0],
             [0, 0, position[0]]]
        )

        self.thrusters.append(self)

    def findSpeed(self, reqMotion, reqRotation):
        divisor = 0
        forMotion = (reqMotion @ self.power).item(0)
        if forMotion != 0:
            divisor = 1

        nonZeroNum = len(reqRotation[np.nonzero(reqRotation)])
        if nonZeroNum != 0:
            forRotation = ((-reqRotation @ self.position @ (-self.power + np.array([[1, 1, 1]]))) / nonZeroNum).item(0)
            divisor += nonZeroNum
        else:
            forRotation = 0

        if divisor == 0:
            divisor = 1
        # print(divisor)

        return round(self.multiplier * (forMotion + forRotation) / divisor, 7)
    
    @classmethod
    def setMultiplier(cls, multiplier):
        cls.mutiplier = multiplier
    
    def convertInput(req: tuple) -> np.array:
        return np.asarray(req)

    @classmethod
    def getSpeeds(cls, reqMotion, reqRotation):
        reqMotion = cls.convertInput(reqMotion)
        reqRotation = cls.convertInput(reqRotation)

        output = {}
        for thruster in cls.thrusters:
            output[thruster.pin] = thruster.findSpeed(reqMotion, reqRotation)
        return output

    @classmethod
    def showSpeeds(cls, speeds):
        for pin, value in speeds.items():
            print(f"{pin = }, {value}")

        
frontL = Thruster(pin=0, power=(0, 0, 1), position=(-1, 1))
frontR = Thruster(pin=1, power=(0, 0, 1), position=( 1, 1))
backL  = Thruster(pin=2, power=(0, 0, 1), position=(-1,-1))
backR  = Thruster(pin=3, power=(0, 0, 1), position=( 1,-1))
sideL  = Thruster(pin=4, power=(1, 1, 0), position=(-1, 0))
sideR  = Thruster(pin=5, power=(1, 1, 0), position=( 1, 0))


Thruster.showSpeeds(
    Thruster.getSpeeds((0, 0, 1), (0.5, 0.25, 0)))