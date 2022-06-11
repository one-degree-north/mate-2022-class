import time

class Thruster():
    multiplier = 1
    thrusters = []
    searchType = None

    def __init__(self, pin, power, position):
        self.pin = pin
        self.power = power
        self.invertedPower = (
            -(self.power[0] - 1),
            -(self.power[1] - 1),
            -(self.power[2] - 1)
        )

        self.position = (position[0], position[1], position[0])
        self.thrusters.append(self)

    def findForMotion(self, reqMotion):
        forMotion = (reqMotion[0] * self.power[0] +
                     reqMotion[1] * self.power[1] +
                     reqMotion[2] * self.power[2])
        return forMotion

    def findForRotation(self, reqRotation):
        nonZeroNum = 0
        usedAxes = (
            reqRotation[0] * self.invertedPower[0],
            reqRotation[1] * self.invertedPower[1],
            reqRotation[2] * self.invertedPower[2]
        )

        for axisValue in usedAxes:
            if axisValue != 0:
                nonZeroNum += 1

        forRotation = 0
        if nonZeroNum != 0:
            forRotation = -(reqRotation[0] * self.position[0] * self.invertedPower[0] + 
                            reqRotation[1] * self.position[1] * self.invertedPower[1] + 
                            reqRotation[2] * self.position[2] * self.invertedPower[2]) / nonZeroNum
        
        return forRotation

    @classmethod
    def setMultiplier(cls, m):
        cls.multiplier = m

    @classmethod
    def getSpeeds(cls, reqMotion, reqRotation, normalize=True):
        if reqMotion[2] > 0:
            cls.searchType = max
        elif reqMotion[2] < 0:
            cls.searchType = min
        else:
            cls.searchType = None
            normalize = False

        output = {}
        toNormalize = {}

        for thruster in cls.thrusters:
            if normalize and thruster.power[2] == 1:
                forRotation = thruster.findForRotation(reqRotation)
                toNormalize[thruster.pin] = forRotation
            else:
                speeds = (thruster.findForMotion(reqMotion), thruster.findForRotation(reqRotation))
                # print(f"{speeds = }")
                divisor = 0
                for speed in speeds:
                    if speed != 0:
                        divisor += 1
                try:
                    output[thruster.pin] = sum(speeds) / divisor
                except ZeroDivisionError:
                    output[thruster.pin] = divisor
        
        # print(f"{toNormalize = }")
        if normalize:
            bump = (1 - abs(cls.searchType(list(toNormalize.values())))) * reqMotion[2]
            print(f"{bump = }")
            for pin, value in toNormalize.items():
                output[pin] = value + bump

        return output

    def showSpeeds(speeds):
        for pin in sorted(list(speeds.keys()), reverse=False):
            print(f"{pin=} -> {round(speeds[pin], 5)}")


start = time.time()

if __name__ == "__main__":     

    frontL = Thruster(pin=0, power=(0, 0, 1), position=(-1, 1))
    frontR = Thruster(pin=1, power=(0, 0, 1), position=( 1, 1))
    backL  = Thruster(pin=2, power=(0, 0, 1), position=(-1,-1))
    backR  = Thruster(pin=3, power=(0, 0, 1), position=( 1,-1))
    sideL  = Thruster(pin=4, power=(1, 1, 0), position=(-1, 0))
    sideR  = Thruster(pin=5, power=(1, 1, 0), position=( 1, 0))

    for i in range(1000):
        Thruster.showSpeeds(Thruster.getSpeeds((0, 1, 0.75), (0.1, 0.1, 0.1), normalize=True))

end = time.time()

totalTime = end - start
print("\n" + str(totalTime))

# end = time.time()
# totalTime = end - start

# print("\n" + str(totalTime))

