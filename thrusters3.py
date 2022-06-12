import time

class Thruster():
    multiplier = 1
    thrusters = []
    # searchTypeZ = None
    # searchTypeY = None
    x, y, z = 0, 1, 2

    def __init__(self, pin, power, position):
        self.pin = pin
        self.power = power
        self.axis = 0
        for axis, value in enumerate(power):
            if value != 0:
                self.axis = axis

        self.invertedPower = (
            -(self.power[0] - 1),
            -(self.power[1] - 1),
            -(self.power[2] - 1)
        )

        self.position = (position[0], position[1], position[0])
        self.sendToManager(self)

    @classmethod
    def sendToManager(cls, thrusterObject):
        cls.thrusters.append(thrusterObject)

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
    def getSpeeds(cls, reqMotion, reqRotation, normalizeZ=True, normalizeY=True):
        if reqMotion[2] == 0:
            normalizeZ = False
        if reqMotion[1] == 0:
            normalizeY = False

        output = {}
        # each axis' dict is thruster.pin: value_from_findForRotation()
        #              x   y   z
        toNormalize = [{}, {}, {}]

        for thruster in cls.thrusters:
            if (normalizeY and thruster.axis == cls.y) or (normalizeZ and thruster.axis == cls.z):
                toNormalize[thruster.axis][thruster.pin] = thruster.findForRotation(reqRotation)

            else:
                speeds = (thruster.findForMotion(reqMotion), thruster.findForRotation(reqRotation))
                # print(f"{speeds = }")
                divisor = 0
                for speed in speeds:
                    if speed != 0:
                        divisor += 1
                try:
                    output[thruster.pin] = cls.multiplier * sum(speeds) / divisor
                except ZeroDivisionError:
                    output[thruster.pin] = divisor

        # print(f"{toNormalize = }")
        
        for axis, axisDict in enumerate(toNormalize):
            searchType = None
            if reqMotion[axis] > 0:
                searchType = max
            elif reqMotion[axis] < 0:
                searchType = min

            if searchType != None and axisDict: # axisDict part checks if dictionary has content
                bump = (1 - abs(searchType(list(axisDict.values())))) * reqMotion[axis]
            else:
                bump = 0
            
            for pin, value in axisDict.items():
                output[pin] = cls.multiplier * (value + bump)

        return output

    def showSpeeds(speeds):
        for pin in sorted(list(speeds.keys()), reverse=False):
            print(f"{pin=} -> {round(speeds[pin], 5)}")




if __name__ == "__main__":     

    start = time.time()

    # frontL = Thruster(pin=0, power=(0, 0, 1), position=(-1, 1))
    # frontR = Thruster(pin=1, power=(0, 0, 1), position=( 1, 1))
    # backL  = Thruster(pin=2, power=(0, 0, 1), position=(-1,-1))
    # backR  = Thruster(pin=3, power=(0, 0, 1), position=( 1,-1))
    # sideL  = Thruster(pin=4, power=(1, 1, 0), position=(-1, 0))
    # sideR  = Thruster(pin=5, power=(1, 1, 0), position=( 1, 0))

    Thruster(pin=0, power=(0, 0, 1), position=(-1, 1))
    Thruster(pin=1, power=(0, 0, 1), position=( 1, 1))
    Thruster(pin=2, power=(0, 0, 1), position=(-1,-1))
    Thruster(pin=3, power=(0, 0, 1), position=( 1,-1))
    Thruster(pin=4, power=(1, 1, 0), position=(-1, 0))
    Thruster(pin=5, power=(1, 1, 0), position=( 1, 0))

    Thruster.setMultiplier(100)

    for i in range(1000):
        Thruster.showSpeeds(Thruster.getSpeeds((0, 1, -1), (0, 0, 0)))
        print("\n" * 3)

    end = time.time()

    totalTime = end - start
    print("\n" + str(totalTime))



