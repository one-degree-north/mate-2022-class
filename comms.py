#import RPi.GPIO as GPIO
from dataclasses import dataclass
from serial import *
from serial.tools import list_ports
import threading, struct
import time
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
    def __init__(self, controls=None, outputQueue=None):
        ports = list_ports.comports()
        offshorePort = "/dev/cu.usbmodem142101"
        #onshorePort = "/dev/cu.usbserial-14210"
        """for port in ports:
           if port.description == "USB Serial":
               onshorePort = port.device
           elif port.description == "FT232R USB UART - FT232R USB UART":
               offshorePort = port.device"""

        self.offshoreArduino = Serial(port=f"{offshorePort}", baudrate=115200)
        #self.onshoreArduino = Serial(port=f"{onshorePort}", baudrate=115200)
        self.thrusterPins = [0, 1, 2, 3, 4, 5]  #maps thruster position via index to pins. [midL, midR, frontL, frontR, backL, backR]
        self.thrusterPWMs = []
        self.gyroData = GyroData()
        self.accelData = AccelData()
        self.controls = controls
        #self.HEADER = 0xAB
        self.HEADER = b'\xab'
        #self.FOOTER = 0xB3
        self.FOOTER = b'\xb3'
        self.threadActive = False
        
        #configure GPIO
        """
        #GPIO.setmode(GPIO.board)
        
        for thrusterPin in self.thrusterPins:
            #GPIO.setup(thrusterPin, GPIO.out)
            #pwm = GPIO.PWM(12, 250) #frequency of 250 per second, length of 4000 microseconds
            pwm.start(0.375)
            self.thrusterPWMs.append(pwm)
        """
        self.outputQueue = outputQueue;

    def writePWM(self, thrusterNum, value):
        dc = (value*0.0025+0.375)
        #self.thrusterPWMs[thrusterNum].ChangeDutyCycle(dc)

    def readOffshore(self):
        currByte = self.offshoreArduino.read()
        footerFound = False
        headerFound = False
        while (not headerFound):
            #print(currByte)
            #print(currByte == b'\xAB')
            if (currByte == self.HEADER):
                #print("header found")
                headerFound = True
                returnValue = self.offshoreArduino.read_until(expected=self.FOOTER, size=14) #probably set timeout as well
                #print(returnValue)
                if (returnValue[-1] == int.from_bytes(self.FOOTER, "big")):
                    #print("footer found")
                    footerFound=True
                    break
            currByte = self.offshoreArduino.read()
        if (len(returnValue) != 14):
            #print(len(returnValue))
            return -1
        structValue = struct.unpack("=cfffc", returnValue)
        if (headerFound):
            if (footerFound):
                return structValue
            else:
                return -1

    def writeOutput(self, output):
        #print(output)
        if (output[0] == 0):
            self.offshoreArduino.write(self.HEADER)
            for value in output[1]:
                print(value)
                self.offshoreArduino.write(value)
            self.offshoreArduino.write(self.FOOTER)
        else:
            self.onshoreArduino.write(self.HEADER)
            self.onshoreArduino.write(output[1][0])
            """for value in output[0][1]:
                print(value)
                self.onshoreArduino.write(value)"""
            for value in output[1][1]:
                print(value)
                self.onshoreArduino.write(value)
            self.onshoreArduino.write(self.FOOTER)

    def readThread(self):
        self.threadActive = True
        while self.threadActive:
            # print("doing this too")
            # print(f"{self.offshoreArduino.in_waiting = }")
            if (self.offshoreArduino.in_waiting >= 15):
                # print("doing this")
                self.controls.handleInput(self.readOffshore())
            #if (not self.outputQueue.empty()):
            #    self.writeOutput(self.outputQueue.get())

            # time.sleep(1)

    def startThread(self):
        currThread = threading.Thread(target=self.readThread)
        currThread.start()
    
    def endThread(self):
        self.threadActive = False

