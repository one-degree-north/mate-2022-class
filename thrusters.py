
class ThrustManager():
    def __init__(self, controls=None, multiplier=1):
        self.thrusters = [
            Thruster(pin=0, power=(0, 0, 1), position=(-1, 1)),
            Thruster(pin=1, power=(0, 0, 1), position=( 1, 1)),
            Thruster(pin=2, power=(0, 0, 1), position=(-1,-1)),
            Thruster(pin=3, power=(0, 0, 1), position=( 1,-1)),
            Thruster(pin=4, power=(1, 1, 0), position=(-1, 0)),
            Thruster(pin=5, power=(1, 1, 0), position=( 1, 0)),
        ]

        self.controls = controls
        self.multiplier = multiplier
        self.x, self.y, self.z = 0, 1, 2

    def getTSpeeds(self, reqMotion, reqRotation, normalizeZ=True, normalizeY=True):
        if reqMotion[2] == 0:
            normalizeZ = False
        if reqMotion[1] == 0:
            normalizeY = False

        output = {}
        # each axis' dict is thruster.pin: value_from_findForRotation()
        #              x   y   z
        toNormalize = [{}, {}, {}]

        for thruster in self.thrusters:
            if (normalizeY and thruster.axis == self.y) or (normalizeZ and thruster.axis == self.z):
                toNormalize[thruster.axis][thruster.pin] = thruster.findForRotation(reqRotation)

            else:
                speeds = (thruster.findForMotion(reqMotion), thruster.findForRotation(reqRotation))
                divisor = 0
                for speed in speeds:
                    if speed != 0:
                        divisor += 1
                try:
                    output[thruster.pin] = self.multiplier * sum(speeds) / divisor
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
                output[pin] = self.multiplier * (value + bump)


        thrusterSpeeds = []
        for pin in sorted(list(output.keys()), reverse=False):
            thrusterSpeeds.append(output[pin])

        if self.controls != None:
            self.controls.writeAllThrusters(thrusterSpeeds)
        else:
            print("Controls not connected...")

        return output

class Thruster():
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

def displayTSpeeds(speeds):
    for pin in sorted(list(speeds.keys()), reverse=False):
        print(f"{pin=} -> {round(speeds[pin], 5)}")


if __name__ == "__main__":
    TManager = ThrustManager()
    displayTSpeeds(TManager.getTSpeeds((0,1,1), (0,0,0)))
    
