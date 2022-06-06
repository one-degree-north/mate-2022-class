from dataclasses import dataclass
import hashlib, hid, time, copy
from struct import unpack


"""def update(inputTest) : ...
joystickInput = open(r"/dev/input/js0", "rb")
def main():
    fileHash = ""
    while True:
        inputTest = joystickInput.read(7)
        newFileHash = hashlib.sha256()
        newFileHash.update(inputTest)
        newFileHashValue = newFileHash.digest()
        if newFileHashValue != fileHash:
            fileHash = newFileHashValue
            update(inputTest)
            # Logic here
    

def update(inputTest):
    #print(inputTest)
    print("Size :" + str(len(inputTest)))
    print(unpack('IBBB', inputTest))
"""
@dataclass
class JoystickData:
    xAxis:float = 0
    yAxis:float = 0
    hat:int = 0
    twist:float = 0
    throtle:float = 0
    buttons:list = []

class Joystick:
    def __init__(self, controls):
        self.joy = hid.device()
        self.joy.open(vendor_id=1133, product_id=49685)
        self.pastInput = 0
        self.joyData = JoystickData()
        self.pastJoyData = copy.copy(self.joyData)
        self.controls = controls

    def sendJoyData(self):
        if 511.5<self.joyData.yAxis<523:
            pass

    def readJoyData(self):
        self.pastJoyData = copy.copy(self.joyData)
        joyInput = self.joy.read(7)
        self.joyData.xAxis = joyInput[0] + ((joyInput[1]&0b11)<<8)
        self.joyData.yAxis = (joyInput[1]>>2) + ((joyInput[2]&0b1111)<<6)
        if 511.5<self.joyData.yAxis and self.joyData.yAxis<523:
            self.joyData.yAxis = 0
        if 511.5<self.joyData.xAxis and self.joyData.xAxis<523:
            self.joyData.xAxis = 0
        self.joyData.yAxis/=5
        self.joyData.xAxis/=5

        #give middle some leeway, resting is not exactly at middle sometimes

    def readJoystickThread(self):
        while True:
            self.readJoyData()
            if self.joyData != self.pastJoyData:
                print("new values")


    def startReadingThread(self):
        pass

    def stopReadingThread(self):
        pass

    @staticmethod
    def printHidDevices():
        for device_dict in hid.enumerate():
            keys = list(device_dict.keys())
            keys.sort()
            #for key in keys:
            #    print("%s : %s" % (key, device_dict[key]))
            print(device_dict["product_id"])
            print(device_dict["vendor_id"])

def readHid(joy):
    joyInput = joy.read(7)
    #xAxis = (joyInput[0]*4) + (joyInput[1] // 64)
    xAxis = joyInput[0]*16 + joyInput[1]//16
    # xAxis = ((joyInput[1] & 0b11000000) << 2) + joyInput[0]
    yAxis = ((joyInput[1] << 4) + (joyInput[2] >> 4)) & 1023
    hat = (joyInput[2])&15
    print(joyInput)
    print(f"hat: {hat}")
    #print(joyInput[0] << 2)
    #print(joyInput[1] >> 6)
    print(f"xAxis: {xAxis}")

    #print((joyInput[1] << 4)&1023)
    #print(joyInput[2] >> 4)
    print(f"yAxis: {yAxis}")
    time.sleep(0.01)

def readHid2(joy):
    joyInput = joy.read(7)
    print(joyInput)
    print(joyInput[0] + 0xFF * (joyInput[1] & 0b11))
    print((joyInput[1] >> 2) + (joyInput[2] & 0b1111) * 0b111111)
    print(bin(joyInput[2] >> 4)[2:].zfill(4))
    #test = (joyInput[0]<<24)+(joyInput[1]<<16)+(joyInput[2]<<8)+joyInput[3]
    #print(str(bin(test))[2:].zfill(32))
    #test = joyInput[0]*256+joyInput[1]
    #print(str(bin(test))[2:].zfill(16))