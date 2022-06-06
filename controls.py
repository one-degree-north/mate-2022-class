from dataclasses import dataclass

class Movement:
    def __init__(self, thrusterModify):
        self.thrusterModify = thrusterModify #[frontL, frontR, midL, midR, backL, backR]
        self.percentage = 0 #percentage ranges from -100 to 100

@dataclass
class GyroData:
    xOrientation:float = 0
    yOrientation:float = 0
    zOrientation:float = 0

@dataclass
class AccelData:
    xAccel:float = 0
    yAccel:float = 0
    zAccel:float = 0

class Controls:
    def __init__(self):
        self.movements = [
            Movement([0, 0, 1, 1, 0, 0]), #y axis movement
            Movement([0, 0, 0, 1, 0, 0]), #rotate movement
            Movement([0, 0, 0, 0, 1, 1]), #pitch movement
            Movement([1, 0, 0, 0, 1, 0]), #tilt movement
            Movement([1, 1, 0, 0, 1, 1]), #vertical movement
        ]
        self.gyroData = GyroData()
        self.accelData = AccelData()

    def applyMovements(self):
        thrusterValues = [0, 0, 0, 0, 0, 0]

    def handleInput(self, inputType, input):
        pass

    def applyJoystickOutput(self, joyData):
        joyData.xAxis

    def writeThruster(self, thrusterNum, value):
        #value is between -50 and 50
        #dc is between 0.25 and 0.5
        dc = (value*0.0025+0.375)
