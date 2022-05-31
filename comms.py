import RPi.GPIO as GPIO
from serial import *
#assuming only RPi, onboard electronics communicating via serial

class Comms:
    def __init__(self, inputQueue, outputQueue):
        self.serialComs = Serial()
        self.thrusterPins = [0, 1, 2, 3, 4, 5]
        self.thrusterPWMs = []
        for thrusterPin in self.thrusterPins:
            GPIO.setup(thrusterPin, GPIO.out)
            pwm = GPIO.PWM(12, 250) #frequency of 250 per second, length of 4000 microseconds
            pwm.start(0.375)
            self.thrusterPWMs.append(pwm)
        self.inputQueue = inputQueue;
        self.outputQueue = outputQueue;

    def configureGpio(self):
        GPIO.setmode(GPIO.board)

    def writePWM(self, thrusterNum, value):
        dc = (value*0.0025+0.375)
        self.thrusterPWMs[thrusterNum].ChangeDutyCycle(dc)

    def readThread(self):
        pass

    def startThread(self):
        pass