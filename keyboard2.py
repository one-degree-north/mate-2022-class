
from dataclasses import dataclass
from pynput import keyboard


@dataclass
class Move:
    motion: int = 0
    rotation: int = 1
    killswtich: int = 'q'
    toggle: int = 3
    bumpUp: int = 4
    bumpDown: int = 5

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

# print(findAngle(30, None, (0, 90), Move.toggle))


class Key():
    acceptedChars = {}
    currClawAngle = 0
    keys = [] # deprecated already lol

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

        self.sendToManager(self)

    @classmethod
    def sendToManager(cls, key):
        cls.keys.append(key)
        cls.acceptedChars[key.keyStr] = key

    def setState(self, isDown):
        if isDown != self.isDown:
            self.isDown = isDown
            print(Key.findNets())
        
    @classmethod
    def findNets(cls):
        netMotion = [0, 0, 0]
        netRotation = [0, 0, 0]
        clawAngle = cls.currClawAngle


        for key in cls.acceptedChars.values():
            if key.isDown:
                # Adding is okay since there aren't any conflicting values
                # And each thruster acts along only one axis
                if key.mType == Move.motion:
                    # print("Adding to motion")
                    netMotion[key.effectAxis] += key.effect[key.effectAxis]
                elif key.mType == Move.rotation:
                    netRotation[key.effectAxis] += key.effect[key.effectAxis]
                elif key.mType == Move.killswtich:
                    return ([0, 0, 0], [0, 0, 0])
                elif key.mType == Move.toggle:

                    clawAngle = key.effect[0](currValue=cls.currClawAngle, 
                                              changeAmount=None,
                                              minMax=key.effect[1],
                                              changeType=Move.toggle)

                    cls.currClawAngle = clawAngle

        return (netMotion, netRotation, clawAngle)

    @classmethod
    def updateKey(cls, keyStr, isDown):
        if keyStr in cls.acceptedChars.keys():
            cls.acceptedChars[keyStr].setState(isDown)
        else:
            print("Key not recognized")


    def onPress(key):
        try:
            char = key.char
        except AttributeError:
            print(f"Special key {key} pressed")
            return

        Key.updateKey(char, isDown=True)
        

    def onRelease(key):
        try:
            char = key.char
        except AttributeError:
            print(f"Special key {key} pressed")
            return

        Key.updateKey(char, isDown=False)


    @classmethod
    def startPolling(cls):
        cls.keyboardListener = keyboard.Listener(on_press=cls.onPress, on_release=cls.onRelease)
        cls.keyboardListener.start()
        

if __name__ == "__main__":


    w = Key('w', Move.motion, (0, 1, 0), False)
    s = Key('s', Move.motion, (0,-1, 0), False)

    i = Key('i', Move.motion, (0, 0, 1), False)
    k = Key('k', Move.motion, (0, 0,-1), False)

    a = Key('a', Move.rotation, (0, 0,-1), False)
    d = Key('d', Move.rotation, (0, 0, 1), False)

    u = Key('u', Move.rotation, (0, 1, 0), False)
    j = Key('j', Move.rotation, (0,-1, 0), False)

    q = Key('q', Move.killswtich, None, False)
    e = Key('e', Move.toggle, [findAngle, (0, 90), 0], False)

    Key.startPolling()
    Key.keyboardListener.join()







