
from re import A
from pynput import keyboard

from dataclasses import dataclass
from message import Message

@dataclass
class Action:
    motion = 0
    rotation = 1
    scale = 2
    toggleOpen = 3
    toggleRotate = 4
    toggleAuto = 5
    shiftPIDTarget = 6
    temp = 7
    temp2 = 8

class Key():
    def __init__(self, actionType, action=None):
        self.actionType = actionType
        self.action = action
        self.isDown = False

        if self.actionType == Action.motion or self.actionType == Action.rotation:
            # if action.motion or action.rotation, then self.action is a 3-element tuple
            for axis, value in enumerate(action):
                if value != 0:
                    self.actionAxis = axis


class KeyboardManager():
    def __init__(self, requestQueue):
        self.requestQueue = requestQueue
        self.keys = {
            'w': Key(Action.motion, (0, 1, 0)),
            's': Key(Action.motion, (0, -1, 0)),
            'i': Key(Action.motion, (0, 0, 1)),
            'k': Key(Action.motion, (0, 0,-1)),

            'a': Key(Action.rotation, (0, 0, -1)), 
            'd': Key(Action.rotation, (0, 0, 1)), 
            'u': Key(Action.rotation, (0, 1, 0)),
            'j': Key(Action.rotation, (0, -1, 0)),
            'l': Key(Action.rotation, (-1, 0, 0)),
            ';': Key(Action.rotation, (1, 0, 0)),

            "1": Key(Action.scale),
            "2": Key(Action.scale),
            "3": Key(Action.scale),
            "4": Key(Action.scale),
            "5": Key(Action.scale),
            "0": Key(Action.scale),

            "e": Key(Action.toggleOpen),
            "r": Key(Action.toggleRotate),

            "t": Key(Action.toggleAuto),

            "c": Key(Action.shiftPIDTarget, 15),
            "v": Key(Action.shiftPIDTarget, 90),
            "x": Key(Action.shiftPIDTarget, -15),
            "z": Key(Action.shiftPIDTarget, -90),

            "b": Key(Action.temp),
            "n": Key(Action.temp2),
        }
        

        self.thrustScale = 1

    def updateKeyState(self, keyString, isDown):
        if keyString in self.keys.keys() and self.keys[keyString].isDown != isDown:
            self.keys[keyString].isDown = isDown
            self.sendRequest()

    def sendRequest(self):
        reqMotion = [0, 0, 0]
        reqRotation = [0, 0, 0]
        toggleRotater = False
        toggleOpenner = False
        toggleAutomation = False
        targetShiftAmount = 0
        temp = False
        temp2 = False


        payload = {
            "reqMotion": (),
            "reqRotation": (),
            "thrustScale": 1,
            "toggleRotater": False,
            "toggleOpenner": False,
            "toggleAutomationMode": False,
            "targetShiftAmount": 0,
            "temp": False,
            "temp2": False,
        }
        for keyString, key in self.keys.items():
            if key.isDown:
                if key.actionType == Action.motion:
                    reqMotion[key.actionAxis] += key.action[key.actionAxis]
                elif key.actionType == Action.rotation:
                    reqRotation[key.actionAxis] += key.action[key.actionAxis]
                elif key.actionType == Action.scale:
                    self.thrustScale = int(keyString) * 0.2
                elif key.actionType == Action.toggleOpen:
                    toggleOpenner = True
                elif key.actionType == Action.toggleRotate:
                    toggleRotater = True
                elif key.actionType == Action.toggleAuto:
                    toggleAutomation = True
                elif key.actionType == Action.shiftPIDTarget:
                    targetShiftAmount = key.action
                elif key.actionType == Action.temp:
                    temp = True
                elif key.actionType == Action.temp2:
                    temp2 = True


        payload["reqMotion"] = reqMotion
        payload["reqRotation"] = reqRotation
        payload["thrustScale"] = self.thrustScale
        payload["toggleOpenner"] = toggleOpenner
        payload["toggleRotater"] = toggleRotater
        payload["toggleAutomationMode"] = toggleAutomation
        payload["targetShiftAmount"] = targetShiftAmount
        payload["temp"] = temp
        payload["temp2"] = temp2

        # print(f"{payload = }")
        self.requestQueue.put(Message("keyboard", payload))
        # print("putting")

    def onPress(self, key):
        try:
            char = key.char
        except AttributeError:
            # print(f"Special key {key} pressed")
            return
        self.updateKeyState(char, isDown=True)

    def onRelease(self, key):
        try:
            char = key.char
        except AttributeError:
            # print(f"Special key {key} pressed")
            return
        self.updateKeyState(char, isDown=False)

    def start(self):
        self.keyboardListener = keyboard.Listener(on_press=self.onPress, on_release=self.onRelease)
        self.keyboardListener.start()


if __name__ == "__main__":
    import queue
    
    requestQueue = queue.Queue()
    KManager = KeyboardManager(requestQueue=requestQueue)
    KManager.start()
    KManager.keyboardListener.join()
