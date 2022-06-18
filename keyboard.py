
from pynput import keyboard

from dataclasses import dataclass
from message import Message

@dataclass
class Action:
    motion = 0
    rotation = 1

class Key():
    def __init__(self, actionType, action):
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
        }

    def updateKeyState(self, keyString, isDown):
        if keyString in self.keys.keys() and self.keys[keyString].isDown != isDown:
            self.keys[keyString].isDown = isDown
            self.sendRequest()

    def sendRequest(self):
        reqMotion = [0, 0, 0]
        reqRotation = [0, 0, 0]


        payload = {
            "reqMotion": (),
            "reqRotation": (),
        }
        for keyString, key in self.keys.items():
            if key.isDown:
                if key.actionType == Action.motion:
                    reqMotion[key.actionAxis] += key.action[key.actionAxis]
                elif key.actionType == Action.rotation:
                    reqRotation[key.actionAxis] += key.action[key.actionAxis]

        payload["reqMotion"] = reqMotion
        payload["reqRotation"] = reqRotation

        # print(payload)
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
