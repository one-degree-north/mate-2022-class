from dataclasses import dataclass
from pynput import keyboard

@dataclass
class KeyMessage:
    reqMotion: tuple
    reqRotation: tuple
    clawAngle: float
    thrustScale: float
    allowAutoInfluence: bool
    tare: bool

@dataclass
class Move:
    motion: int = 0
    rotation: int = 1
    pauseAuto: int = 2
    toggle: int = 3
    bumpUp: int = 4
    bumpDown: int = 5
    scale: int = 6
    tare: int = 7

def findAngle(currValue, changeAmount, minMax, changeType):
    if changeType == Move.bumpUp:
        currValue += changeAmount
    elif changeType == Move.bumpDown:
        currValue -= changeAmount
    elif changeType == Move.toggle:
        if (currValue - minMax[0]) >= (minMax[1] - currValue):
            currValue = minMax[0]
        else:
            currValue = minMax[1]

    if currValue < minMax[0]:
        currValue = minMax[0]
    elif currValue > minMax[1]:
        currValue = minMax[1]

    return currValue

def findFlipVal(currValue):
    if currValue:
        return False
    return True

def speakMovement(reqMotion, reqRotation=None):
    output = "\n---------------\n"

    if reqMotion[1] != 0:
        if reqMotion[1] > 0:
            output += "Moving Forward!\n"
        else:
            output += "Moving Backward!\n"
    if reqMotion[2] != 0:
        if reqMotion[2] > 0:
            output += "Moving Up!\n"
        else:
            output += "Moving Down!\n"

    if reqRotation[0] != 0:
        if reqRotation[0] > 0:
            output += "Tilting Rightward!\n"
        else:
            output += "Tilting Leftward!\n"
    if reqRotation[1] != 0:
        if reqRotation[1] > 0:
            output += "Tilting Forward!\n"
        else:
            output += "Tilting Backward!\n"
    if reqRotation[2] != 0:
        if reqRotation[2] > 0:
            output += "Turning right!\n"
        else:
            output += "Turning left!\n"

    print(output)

class KeyManager():
    def __init__(self, q=None):
        self.q = q
        self.acceptedChars = {}
        self.keys = [
            Key('w', Move.motion, (0, 1, 0), False),
            Key('s', Move.motion, (0,-1, 0), False),

            Key('i', Move.motion, (0, 0, 1), False),
            Key('k', Move.motion, (0, 0,-1), False),

            Key('a', Move.rotation, (0, 0,-1), False),
            Key('d', Move.rotation, (0, 0, 1), False),

            Key('u', Move.rotation, (0, 1, 0), False),
            Key('j', Move.rotation, (0,-1, 0), False),

            Key('l', Move.rotation, (-1, 0, 0), False),
            Key(';', Move.rotation, (1, 0, 0), False),

            Key('q', Move.pauseAuto, None, False),
            Key('e', Move.toggle, [findAngle, (0, 90), 0], False),

            Key('1', Move.scale, None, False),
            Key('2', Move.scale, None, False),
            Key('3', Move.scale, None, False),
            Key('4', Move.scale, None, False),
            Key('5', Move.scale, None, False),
            Key('0', Move.scale, None, False),

            Key('t', Move.tare, None, False),
        ]

        self.currClawAngle = 0
        self.thrustScale = 1
        self.allowAutoInfluence = True

        for key in self.keys:
            self.acceptedChars[key.keyStr] = key

    def findNets(self):
        netMotion = [0, 0, 0]
        netRotation = [0, 0, 0]
        clawAngle = self.currClawAngle
        tare = False

        for key in self.acceptedChars.values():
            if key.isDown:
                # Adding is okay since there aren't any conflicting values
                # And each thruster acts along only one axis
                if key.mType == Move.motion:
                    # print("Adding to motion")
                    netMotion[key.effectAxis] += key.effect[key.effectAxis]
                elif key.mType == Move.rotation:
                    netRotation[key.effectAxis] += key.effect[key.effectAxis]
                # elif key.mType == Move.killswtich:
                #     return ([0, 0, 0], [0, 0, 0], 0)
                elif key.mType == Move.toggle:

                    clawAngle = key.effect[0](currValue=self.currClawAngle, 
                                              changeAmount=None,
                                              minMax=key.effect[1],
                                              changeType=Move.toggle)

                    self.currClawAngle = clawAngle

                elif key.mType == Move.scale:
                    self.thrustScale = int(key.keyStr) * 0.2
                
                elif key.mType == Move.pauseAuto:
                    self.allowAutoInfluence = findFlipVal(self.allowAutoInfluence)

                elif key.mType == Move.tare:
                    tare = True


        output = KeyMessage(
            reqMotion          = netMotion,
            reqRotation        = netRotation,
            clawAngle          = clawAngle,
            thrustScale        = self.thrustScale,
            allowAutoInfluence = self.allowAutoInfluence,
            tare               = tare
        )

        self.q.put(["k", output])

    def updateKeyState(self, keyStr, isDown):
        if keyStr in self.acceptedChars.keys() and self.acceptedChars[keyStr].isDown != isDown:
            self.acceptedChars[keyStr].isDown = isDown
            self.findNets()

    def onPress(self, key):
        try:
            char = key.char
        except AttributeError:
            print(f"Special key {key} pressed")
            return

        self.updateKeyState(char, isDown=True)
        # print(self.findNets())

    def onRelease(self, key):
        try:
            char = key.char
        except AttributeError:
            print(f"Special key {key} pressed")
            return

        self.updateKeyState(char, isDown=False)
        # print(self.findNets())

    def startPolling(self):
        self.keyboardListener = keyboard.Listener(on_press=self.onPress, on_release=self.onRelease)
        self.keyboardListener.start()


class Key():
    def __init__(self, keyStr, mType, effect, isDown=False):
        self.keyStr = keyStr
        self.mType = mType
        self.effect = effect
        
        self.effectAxis = 0 
        if self.mType == Move.motion or self.mType == Move.rotation:
            for axis, m in enumerate(effect):
                if m != 0:
                    self.effectAxis = axis

        self.isDown = isDown


if __name__ == "__main__":
    KManager = KeyManager()
    KManager.startPolling()
    KManager.keyboardListener.join()