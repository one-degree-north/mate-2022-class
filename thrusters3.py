import time

class Thruster():
    multiplier = 1
    thrusters = []

    def __init__(self, pin, power, position):
        self.pin = pin
        self.power = power
        self.position = (position[0], position[1], position[0])
        self.thrusters.append(self)

    def findSpeed(self, reqMotion, reqRotation):
        divisor = 0
        forMotion = (reqMotion[0] * self.power[0] +
            reqMotion[1] * self.power[1] +
            reqMotion[2] * self.power[2])
        if forMotion != 0:
            divisor = 1

        nonZeroNum = 0
        for axisValue in reqRotation:
            if axisValue != 0:
                nonZeroNum += 1

        # print(nonZeroNum)
        if nonZeroNum != 0:
            forRotation = -(
                reqRotation[0] * self.position[0] * -(self.power[0] - 1) + 
                reqRotation[1] * self.position[1] * -(self.power[1] - 1) + 
                reqRotation[2] * self.position[2] * -(self.power[2] - 1)
            )
            divisor += nonZeroNum
        else:
            forRotation = 0

        if divisor == 0:
            divisor = 1

        # print(forRotation)
        # print(forMotion)

        return round(self.multiplier * (forMotion + forRotation) / divisor, 7)

    @classmethod
    def setMultiplier(cls, m):
        cls.multiplier = m

    @classmethod
    def getSpeeds(cls, reqMotion, reqRotation):
        output = {}
        for thruster in cls.thrusters:
            output[thruster.pin] = thruster.findSpeed(reqMotion, reqRotation)
        return output

    @classmethod
    def showSpeeds(cls, speeds):
        for pin, value in speeds.items():
            print(f"{pin = } , {value}")


start = time.time()

if __name__ == "__main__":     
       
    frontL = Thruster(pin=0, power=(0, 0, 1), position=(-1, 1))
    frontR = Thruster(pin=1, power=(0, 0, 1), position=( 1, 1))
    backL  = Thruster(pin=2, power=(0, 0, 1), position=(-1,-1))
    backR  = Thruster(pin=3, power=(0, 0, 1), position=( 1,-1))
    sideL  = Thruster(pin=4, power=(1, 1, 0), position=(-1, 0))
    sideR  = Thruster(pin=5, power=(1, 1, 0), position=( 1, 0))
    for i in range(100):
        Thruster.showSpeeds(Thruster.getSpeeds((0, 0, 0), (0.5, 0.25, 0)))

end = time.time()

totalTime = end - start
print("\n" + str(totalTime))

