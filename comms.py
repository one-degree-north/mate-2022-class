#import RPi.GPIO as GPIO
from dataclasses import dataclass
from serial import *
import threading, struct
#assuming only RPi, onboard electronics communicating via serial

@dataclass
class GyroData:
    xOrientation: float = 0
    yOrientation: float = 0
    zOrientation: float = 0

@dataclass
class AccelData:
    xAccel: float = 0
    yAccel: float = 0
    zAccel: float = 0

class Comms:    #COMMENTING THINGS OUT FOR TEST ON LAPTOP
    def __init__(self, inputQueue=None, outputQueue=None):
        self.serialInput = Serial(port=f"/dev/cu.usbserial-1420", baudrate=115200)
        self.thrusterPins = [0, 1, 2, 3, 4, 5]  #maps thruster position via index to pins. [midL, midR, frontL, frontR, backL, backR]
        self.thrusterPWMs = []
        self.gyroData = GyroData()
        self.accelData = AccelData()
        
        #configure GPIO
        """
        #GPIO.setmode(GPIO.board)
        
        for thrusterPin in self.thrusterPins:
            #GPIO.setup(thrusterPin, GPIO.out)
            #pwm = GPIO.PWM(12, 250) #frequency of 250 per second, length of 4000 microseconds
            pwm.start(0.375)
            self.thrusterPWMs.append(pwm)
        """

        self.inputQueue = inputQueue;
        self.outputQueue = outputQueue;

    def writePWM(self, thrusterNum, value):
        dc = (value*0.0025+0.375)
        #self.thrusterPWMs[thrusterNum].ChangeDutyCycle(dc)

    def read(self):
        currByte = self.serialInput.read()
        footerFound = False
        headerFound = False
        while (not headerFound):
            if (currByte == self.HEADER):
                headerFound = True
                returnValue = self.serialInput.read_until(expected=self.FOOTER, size=7)
                if (returnValue[-1] == self.INTFOOTER):
                    footerFound=True
                    break
            currByte = self.serialInput.read()
        #print(returnValue)
        if (len(returnValue) != 7):
            return -1
        structValue = struct.unpack("=ccfc", returnValue)
        if (headerFound):
            if (footerFound):
                return structValue
            else:
                return -1

    def readThread(self):
        while True:
            if (self.arduinoSerial.in_waiting >= 7):
                #print("reading sensor input")
                self.controls.handleInput(self.read())

    def startThread(self):
        currThread = threading.Thread(target=self.commThread)
        currThread.start()