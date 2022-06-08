from dataclasses import dataclass, field
import hashlib, hid, time, copy, threading
from struct import unpack
from controls import Controls, Movements
#from thrusters import Thruster

@dataclass
class JoystickData:
    xAxis:float = 0
    yAxis:float = 0
    hat:int = 0
    twist:float = 0
    throttle:float = 0
    buttons:list = field(default_factory=list)

class Joystick:
    def __init__(self, controls=None, callbackMethod=None):
        self.joy = hid.device()
        self.joy.open(vendor_id=1133, product_id=49685)
        self.pastInput = 0
        self.joyData = JoystickData()
        self.pastJoyData = copy.copy(self.joyData)
        self.controls = controls
        self.currReadingThread = None
        self.threadActive = False
        self.callbackMethod = callbackMethod

    def sendJoyData(self):  #translate data into movement
        
        if (self.pastJoyData != self.joyData):
            #print(self.joyData)
            #self.thruster.getJoyData(self.joyData)
            self.callbackMethod(self.joyData)
            #return self.joyData
            # self.controls.applyJoystickOutput(self.joyData)

    def readJoyData(self):
        self.pastJoyData = copy.copy(self.joyData)
        joyInput = self.joy.read(7)

        #I'm SORRY! JOYSTICK AXIS
        self.joyData.xAxis = joyInput[0] + ((joyInput[1]&0b11)<<8)
        self.joyData.yAxis = (joyInput[1]>>2) + ((joyInput[2]&0b1111)<<6)
        self.joyData.xAxis -= 511.5
        self.joyData.yAxis -= 511.5
        if -11.5<self.joyData.yAxis and self.joyData.yAxis<11.5: #joystick is abit weird on middle position
            self.joyData.yAxis = 0
        if -11.5<self.joyData.xAxis and self.joyData.xAxis<11.5: #joystick is a bit weird on middle position
            self.joyData.xAxis = 0
        if self.joyData.yAxis > 0:
            self.joyData.yAxis -= 11.5
        elif self.joyData.yAxis < 0:
            self.joyData.yAxis += 11.5
        if self.joyData.xAxis > 0:
            self.joyData.xAxis -= 11.5
        elif self.joyData.xAxis < 0:
            self.joyData.xAxis += 11.5
        self.joyData.yAxis/=500
        self.joyData.xAxis/=500
        
        #JOYSTICK HAT
        self.joyData.hat = joyInput[2]>>4

        #JOYSTICK TWIST
        self.joyData.twist = joyInput[3]
        #print(f"twist: {self.joyData.twist}")
        self.joyData.twist -= 127.5
        #115 - 145 or so, 17.5 offset
        if -17.5 < self.joyData.twist and self.joyData.twist < 17.5:
            self.joyData.twist = 0
        if self.joyData.twist > 0:
            self.joyData.twist -= 17.5
        elif self.joyData.twist < 0:
            self.joyData.twist += 17.5
        self.joyData.twist/=110

        #JOYSTICK THROTTLE
        self.joyData.throttle = -1*(joyInput[5] - 255)

        #BUTTONS
        self.joyData.buttons = []
        for i in range(8):
            if i in [1, 8]:
                continue
            self.joyData.buttons.append((joyInput[4]>>i)&0b1)
        for i in range(8):
            if i in [4, 5, 6, 7, 8]:
                continue
            self.joyData.buttons.append((joyInput[6]>>i)&0b1)

    def readingThread(self):
        self.threadActive = True
        while self.threadActive:
            self.readJoyData()
            self.sendJoyData()
            #self.controls.applyJoystickOutput(self.joyData)

    def startReadingThread(self):
        self.currReadingThread = threading.Thread(target=self.readingThread)
        self.currReadingThread.start()

    def stopReadingThread(self):
        self.threadActive = False

    def readHid2(self):
        joyInput = self.joy.read(7)
        print(joyInput)
        print(joyInput[0] + 0xFF * (joyInput[1] & 0b11))
        print((joyInput[1] >> 2) + (joyInput[2] & 0b1111) * 0b111111)
        print(bin(joyInput[2] >> 4)[2:].zfill(4))

    @staticmethod
    def printHidDevices():
        for device_dict in hid.enumerate():
            keys = list(device_dict.keys())
            keys.sort()
            #for key in keys:
            #    print("%s : %s" % (key, device_dict[key]))
            print(device_dict["product_id"])
            print(device_dict["vendor_id"])

if __name__ == "__main__":
    controls = Controls()
    joystick = Joystick(controls)
    joystick.readingThread()
    #while True:
    #    joystick.readHid2()
