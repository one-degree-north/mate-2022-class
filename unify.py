
import queue
import threading
import time

from controls import Controls

from servos import ServoManager
from thrusters import ThrustManager, displayTSpeeds
from keyboard import KeyboardManager
from automation import PIDController

class Unify():
    def __init__(self, requestQueue, guiQueue, interval, controls=None):
        self.TManager = ThrustManager(controls=controls)
        self.KManager = KeyboardManager(requestQueue=requestQueue)
        self.SManager = ServoManager(controls=None)
        self.pidC = PIDController(interval, controls=controls, requestQueue=requestQueue)
        
        self.requestQueue = requestQueue
        self.guiQueue = guiQueue
        self.interval = interval
        
        self.readLasts = False

        self.lastPayloadFromKeyboard = {"reqMotion": [0, 0, 0], "reqRotation": [0, 0, 0]}
        self.lastPayloadFromAutomation = {"reqRotation": (0, 0, 0)}

        # allows/disallows automation to affect thruster speed calculations
        self.allowAutoInfluence = True

        self.combineType = self.getAverage



    def readRequestQueue(self):
        while True:
            # print(self.requestQueue.qsize())

            while self.requestQueue.qsize() != 0:
                message = self.requestQueue.get()
                source, payload = message.source, message.payload
                if source == "keyboard" and self.lastPayloadFromKeyboard != payload:
                    self.lastPayloadFromKeyboard = payload
                    self.readLasts = True
                
                elif source == "automation" and self.lastPayloadFromAutomation != payload:
                    self.lastPayloadFromAutomation = payload
                    self.readLasts = True

                if self.readLasts:
                    # print(f"\n{self.lastPayloadFromKeyboard = }")
                    # print(f"{self.lastPayloadFromAutomation = }")

                    reqMotion = self.lastPayloadFromKeyboard["reqMotion"]
                    reqRotation = self.lastPayloadFromKeyboard["reqRotation"]
                    thrustScale = self.lastPayloadFromKeyboard["thrustScale"]

                    if self.lastPayloadFromKeyboard["toggleOpenner"]:
                        self.SManager.openner.toggle()
                    if self.lastPayloadFromKeyboard["toggleRotater"]:
                        self.SManager.rotater.toggle()

                    thrusterSpeeds = self.TManager.getTSpeeds(reqMotion, reqRotation, thrustScale)

                    displayTSpeeds(thrusterSpeeds)

                    self.guiQueue.put([thrusterSpeeds, reqRotation])

                    self.readLasts = False

            time.sleep(self.interval * 0.001)  


    def getKrishnaQ(self):
        return self.KrishnaQ

    def start(self):
        self.KManager.start()
        self.pidC.start()
        # print("doing this")

        self.readRequestThread = threading.Thread(target=self.readRequestQueue, daemon=True)
        self.readRequestThread.start()

    def getAverage(self, kData, aData):
        output = []
        for indexNo, _ in enumerate(kData):
            output.append((kData[indexNo] + aData[indexNo]) / 2)
        return output

    def averageWithoutYaw(self, kData, aData):
        output = []
        for indexNo, _ in enumerate(kData):
            if indexNo != self.TManager.z:
                output.append((kData[indexNo] + aData[indexNo]) / 2)
            else:
                output.append(kData[self.TManager.z])
        return output

if __name__ == "__main__":  
    controls = None  
    # controls = Controls()
    # controls.setOrientationAutoreport(1)
    # controls.comms.startThread()

    requestQueue = queue.Queue()
    guiQueue = queue.Queue()
    u = Unify(requestQueue=requestQueue, guiQueue=guiQueue, interval=10, controls=controls)
    u.start()
