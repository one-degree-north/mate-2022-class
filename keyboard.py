from dataclasses import *
from pynput import keyboard
from comms import Comms

@dataclass
class Thruster:
    pinNum = 0
    writtenValue = 0

@dataclass
class Thrusters:
    frontL = 0
    frontR = 1
    midL = 2    #thrusters that move horizontaly
    midR = 3    #thrusters that move horizontaly
    backL = 4
    backR = 5

@dataclass
class Servos:
    claw = 2
    # Not in use
    # claw_rotate = 1
    # camera = 2

@dataclass
class MovementKey:
    key: chr
    movementModify: list[int]   #front_left, front_right, mid_left, mid_right, back_left, back_right
    horizontal: bool            #horizontal or vertical, modifies how the average is calculated
    keydown: bool = False

"""
@dataclass
class MovementKey:
    key = 'w'
    movementModify = []   #front_left, front_right, mid_left, mid_right, back_left, back_right
    horizontal = False     #horizontal or vertical, modifies how the average is calculated
    keydown = False
"""

class Keyboard:
    def __init__(self, comms):
        self.comms = comms
        self.movementModifier = 1.0
        self.keys = [
            MovementKey(key='w', movementModify=[50, 50], horizontal=True),      # all forward
            MovementKey(key='s', movementModify=[-50, -50], horizontal=True),    # all back
        ]
        self.thrusterValues = [0, 0, 0, 0, 0 ,0]
    
    def setThrusterMovement(self):
        #calculate total movement by iterating through all movement keys
        horizontalThrusters = [0, 0]
        verticalThrusters = [0, 0, 0, 0]
        horizontalNum = 0
        verticalNum = 0
        for movementKey in self.keys:
            if (movementKey.horizontal):
                horizontalNum += 1
                for i in range(2):
                    horizontalThrusters[i] += movementKey.movementModify[i]
            else:
                verticalNum += 1
                for i in range(4):
                    verticalThrusters[i] += movementKey.movementModify[i]
        print()
        if (horizontalNum != 0):
            for i in range(2):
                horizontalThrusters[i] /= horizontalNum
                horizontalThrusters[i] *= self.movementModifier
                print(f"thruster: {i}, value: {horizontalThrusters[i]}")
                self.comms.writePWM(i, horizontalThrusters[i])
        if (verticalNum != 0):
            for i in range(4):
                verticalThrusters[i] /= verticalNum
                verticalThrusters[i] *= self.movementModifier
                print(f"thruster: {i+2}, value: {verticalThrusters[i]}")
                self.comms.writePWM(i+2, verticalThrusters[i])

    def setThrusterMovement2(self):
        #storing values in rawThrusterValues, taking them out when onRelease. This is probably better for automation
        pass

    def onPress(self, key):
        #working wtih setThrusterMovement right now
        for movementKey in self.keys:
            if movementKey.key == key.char and movementKey.keydown == False:
                print("key found")
                movementKey.keydown = True
                self.setThrusterMovement()

    def onRelease(self, key):
        #working with setThrusterMovement right now
        for movementKey in self.keys:
            if movementKey.key == key.char:
                print("key found")
                movementKey.keydown = False
                self.setThrusterMovement()
        

    def startInputReading(self):
        keyboardListener = keyboard.Listener(on_press=self.onPress, on_release=self.onRelease)
        keyboardListener.start()

def main():
    comms = Comms()
    keyboard = Keyboard(comms)
    keyboard.startInputReading()
    while True:
        pass


if (__name__ == "__main__"):
    main()