#import RPi.GPIO as GPIO
from dataclasses import dataclass
from serial import *
from serial.tools import list_ports
import threading, struct, queue, time

class VerificationPacket:
    def __init__(self, packetData, verificationQueue):
        self.packetData = packetData
        self.verificationQueue = verificationQueue
        self.timeout = 150 #in ms
        self.timeout *= 1000000 #in ns
        self.startTime = time.perf_counter_ns()

    def checkConfirmation(self, recvPacket):    #not going to use checksum, instead just compare all values
        if recvPacket != self.packetData:
            #is not good, resend
            self.resendPacket()

    def checkTime(self):
        if self.startTime - time.perf_counter_ns() > self.timeout:
            self.resendPacket()

    def resendPacket(self):
        pass

class Comms:    #COMMENTING THINGS OUT FOR TEST ON LAPTOP
    def __init__(self, controls=None, outputQueue=None, onshoreEnabled=True, offshoreEnabled=True, verificationPacket=False):
        self.onshoreEnabled = onshoreEnabled
        self.offshoreEnabled= offshoreEnabled
        ports = list_ports.comports()
        offshorePort = "/dev/cu.usbmodem142101"
        onshorePort = "/dev/cu.usbserial-142101"
        for port in ports:
            print(f"product: {port.product}")
            print(f"device: {port.device}")
            if port.product == "QT Py M0" or port.product == "FT232R USB UART":
                print(f"QT Py found")
                offshorePort = port.device
            #elif port.description == "FT232R USB UART - FT232R USB UART":
            #    print(f"serial connection found")
            #    offshorePort = port.device
            if port.product == "USB Serial":
                print(f"arduino nano found")
                onshorePort = port.device
            #elif port.description == "USB Serial":
            #    onshorePort = port.device
        self.offshoreArduino = None
        self.onshoreArduino = None
        if self.offshoreEnabled:
            self.offshoreArduino = Serial(port=f"{offshorePort}", baudrate=115200)
        if self.onshoreEnabled:
            self.onshoreArduino = Serial(port=f"{onshorePort}", baudrate=115200)
        self.controls = controls
        self.HEADER = b'\xab'
        self.FOOTER = b'\xb3'
        self.threadActive = False
        self.outputQueue = outputQueue;
        self.onshoreVerificationQueue = queue.Queue()
        self.offshoreVerificationQueue = queue.Queue()

    def readOffshore(self):
        currByte = self.offshoreArduino.read()
        footerFound = False
        headerFound = False
        while (not headerFound):
            if (currByte == self.HEADER):
                headerFound = True
                returnValue = self.offshoreArduino.read_until(expected=self.FOOTER, size=14) #probably set timeout as well
                if (returnValue[-1] == int.from_bytes(self.FOOTER, "big")):
                    footerFound=True
                    break
            currByte = self.offshoreArduino.read()
        if (len(returnValue) != 14):
            return -1
        structValue = struct.unpack("=cfffc", returnValue)
        if (headerFound):
            if (footerFound):
                return structValue
            else:
                return -1

    def writeOutput(self, output):
        #print(output)
        if output[0] == 0 and self.offshoreEnabled:
            self.offshoreArduino.write(self.HEADER)
            for value in output[1]:
                self.offshoreArduino.write(value)
            self.offshoreArduino.write(self.FOOTER)
        elif self.onshoreEnabled:
            self.onshoreArduino.write(self.HEADER)
            self.onshoreArduino.write(output[1][0])
            for value in output[1][1]:
                self.onshoreArduino.write(value)
            self.onshoreArduino.write(self.FOOTER)

    def readThread(self):
        self.threadActive = True
        while self.threadActive:
            # print("doing this too")
            # print(f"{self.offshoreArduino.in_waiting = }")
            if self.offshoreEnabled and self.offshoreArduino.in_waiting >= 15:
               self.controls.handleInput(self.readOffshore())
            if not self.outputQueue.empty():
                self.writeOutput(self.outputQueue.get())

    def startThread(self):
        currThread = threading.Thread(target=self.readThread)
        currThread.start()
    
    def endThread(self):
        self.threadActive = False