
from comms import Comms
import queue

# @dataclass
# class GyroData:
#     xOrientation:float = 0
#     yOrientation:float = 0
#     zOrientation:float = 0

# @dataclass
# class AccelData:
#     xAccel:float = 0
#     yAccel:float = 0
#     zAccel:float = 0

class Controls:
    def __init__(self):
        #self.movements = Movements()
        #self.gyroData = GyroData()
        #self.accelData = AccelData()
        self.reversed = [0, 2, 3, 4, 5]
        self.gyroData = [0, 0, 0] #rad/s
        self.orientationData = [0, 0, 0] #EULER: yaw (0-360), pitch (values are a bit weird, -90 to 90), roll (-180 to 180), may try using gyro instead of euler later
        self.accelData = [0, 0, 0] #m/s^2
        self.outputQueue = queue.Queue()
        self.comms = Comms(controls=self, outputQueue=self.outputQueue)
        #self.thrusterValues = [0, 0, 0, 0, 0, 0]

    #def applyMovements(self):
    #    thrusterValues = [0, 0, 0, 0, 0, 0]

    def handleInput(self, input):
        # print("This is being run")
        #print(input)
        if (input == -1):
            return -1
        if (input[0] == b'\x20'):   #GYRO output (degrees)
            for i in range(3):
                self.gyroData[i] = input[i+1]
            #print(f"gyro data: {self.gyroData}")
        elif (input[0] == b'\x10'):   #ACCEL output (m/s^2)
            for i in range(3):
                self.accelData[i] = input[i+1]
            # print(f"accel data: {self.accelData}")
        else:
            for i in range(3):
                if (i == 0):
                    self.orientationData[i] = input[i+1] - 180
                else:
                    self.orientationData[i] = input[i+1]
            # print(f"orientation data: {self.orientationData[0]}\n{self.orientationData[1]}\n{self.orientationData[2]}\n")
        return 1

    def applyJoystickOutput(self, joyData):
        print(joyData)

    """def writeThruster(self, thrusterNum, value): #DEPRECIATED, DO NOT USE!!!
        #value is between -50 and 50
        #dc is between 0.25 and 0.5
        dc = (value*0.0025+0.375)"""

    def writeAllThrusters(self, thrusterValues): #assuming thrusterValues is between -1 and 1
        modifiedThrusters = []
        for i in range(6):
            #print(thrusterValues[i])
            if i in self.reversed:
                thrusterValues[i] *= -1
            modifiedThrusterValue = int(thrusterValues[i]*50 + 150) #passed thruster values are between 100 and 200 (translates into 1000 and 2000 microseconds)
            #print(int(thrusterValues[i]*50 + 150))
            if (modifiedThrusterValue > 200):
                modifiedThrusterValue = 200
            if (modifiedThrusterValue < 100):
                modifiedThrusterValue = 100
            # print(modifiedThrusterValue)
            modifiedThrusters.append(int.to_bytes(modifiedThrusterValue, 1, "big"))
        # print(modifiedThrusters)
        self.outputQueue.put((1, (int.to_bytes(0x14, 1, "big"), modifiedThrusters)))

    def rotateClaw(self, deg):  #input values between 0 and 90 (0 is horizontal, 90 is vertical)
        #values between 90-160
        if deg < 0:
            deg = 0
        if deg > 90:
            deg = 90
        outputVal = int((deg*7/9)+90)
        print("BBB")
        print(outputVal)
        self.outputQueue.put((1, (int.to_bytes(0x5A, 1, "big"), [int.to_bytes(outputVal, 1, "big")])))

    def moveClaw(self, deg):    #input values between 0 and 1 (0 is fully closed, 1 is fully open)
        #match to values between 180-117
        if deg < 0:
            deg = 0
        if deg > 1:
            deg = 1
        outputVal = int((deg*63)+117)
        print(outputVal)
        self.outputQueue.put((1, (int.to_bytes(0x1C, 1, "big"), [int.to_bytes(outputVal, 1, "big")])))

    def getAccelValue(self):
        self.outputQueue.put((0, (int.to_bytes(0x10, 1, "big"), int.to_bytes(0, 1, "big"))))

    def getGyroValue(self):
        self.outputQueue.put((0, (int.to_bytes(0x20, 1, "big"), int.to_bytes(0, 1, "big"))))

    def getOrientationValue(self):
        self.outputQueue.put((0, (int.to_bytes(0x30, 1, "big"), int.to_bytes(0, 1, "big"))))

    def setAccelAutoreport(self, delay):
        self.outputQueue.put((0, (int.to_bytes(0x12, 1, "big"), int.to_bytes(delay, 1, "big"))))

    def setGyroAutoreport(self, delay):
        self.outputQueue.put((0, (int.to_bytes(0x23, 1, "big"), int.to_bytes(delay, 1, "big")))) #delay is in milliseconds/10

    def setOrientationAutoreport(self, delay):
        self.outputQueue.put((0, (int.to_bytes(0x35, 1, "big"), int.to_bytes(delay, 1, "big"))))

    def resetOffshore(self):
        self.outputQueue.put((0, (int.to_bytes(0x40, 1, "big"), int.to_bytes(0, 1, "big"))))

if __name__ == "__main__":
    controls = Controls()
    controls.comms.startThread()
    #controls.setOrientationAutoreport(1)
    # controls.resetOffshore()
    #controls.resetOffshore()
    """inputNum = 0
    inputs = [0, 0, 0, 0, 0, 0]
    while True:
        print("index")
        index = int(input())
        print("value")
        value = float(input())
        inputs[index] = value
        print(inputs)
        controls.writeAllThrusters(inputs)
        inputs = [0, 0, 0, 0, 0,0]"""
    
    """while True:
        print(f"thrusterNum: {inputNum}")
        inputs[inputNum] = float(input())
        if inputNum >= 5:
            print(inputs)
            controls.writeAllThrusters(inputs)
            inputNum = 0
        inputNum += 1"""
    
    """while True:
        servo = int(input("servoNum"))
        deg = float(input("deg\n"))
        if (servo == 0):
            print("moveClaw")
            controls.moveClaw(deg)
        else:
            print("rotateClaw")
            controls.rotateClaw(deg)"""
        #controls.rotateClaw(deg)
    #controls.setAccelAutoreport(100)
    #controls.comms.readThread()
    while True:
        pass
