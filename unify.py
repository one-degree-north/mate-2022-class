
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
        self.SManager = ServoManager(controls=controls)
        self.pidC = PIDController(interval, controls=controls, requestQueue=requestQueue)
        
        self.requestQueue = requestQueue
        self.guiQueue = guiQueue
        self.interval = interval
        
        self.readLasts = False

        self.lastPayloadFromKeyboard = {
            "reqMotion": (0, 0, 0),
            "reqRotation": (0, 0, 0),
            "thrustScale": 1,
            "toggleRotater": False,
            "toggleOpenner": False,
        }
        self.lastPayloadFromAutomation = {"reqRotation": (0, 0, 0)}

        # allows/disallows automation to affect thruster speed calculations
        self.allowAutoInfluence = True
        # either "balancing", "full", or "off"
        # balancing excludes yaw, full includes it
        self.automationMode = "full"

        self.combineType = self.getAverage



    def readRequestQueue(self):
        while True:
            # print(self.requestQueue.qsize())

            while self.requestQueue.qsize() != 0:
                message = self.requestQueue.get()
                source, payload = message.source, message.payload
                if source == "keyboard" and self.lastPayloadFromKeyboard != payload:
                    # print("doing this")
                    # print(payload)
                    self.lastPayloadFromKeyboard = payload
                    self.readLasts = True
                
                elif source == "automation" and self.lastPayloadFromAutomation != payload and self.automationMode != "off":
                    self.lastPayloadFromAutomation = payload
                    self.readLasts = True

                if self.readLasts:
                    print(f"\nKeyboard: {self.lastPayloadFromKeyboard}")
                    print(f"Automation: {self.lastPayloadFromAutomation}")

                    reqMotion = self.lastPayloadFromKeyboard["reqMotion"]


                    if self.automationMode == "off":
                        reqRotation = self.lastPayloadFromKeyboard["reqRotation"]
                    elif self.automationMode == "balancing":
                        reqRotation = (self.lastPayloadFromAutomation["reqRotation"][0], 
                                       self.lastPayloadFromAutomation["reqRotation"][1], 
                                       self.lastPayloadFromKeyboard["reqRotation"][2])
                    elif self.automationMode == "full":
                        reqRotation = self.lastPayloadFromAutomation["reqRotation"]




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


    def start(self):
        self.KManager.start()
        self.pidC.start()
        # print("doing this")

        self.readRequestThread = threading.Thread(target=self.readRequestQueue, daemon=False)
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
    controls = Controls(offshoreEnabled=True)


    requestQueue = queue.Queue()
    guiQueue = queue.Queue()
    u = Unify(requestQueue=requestQueue, guiQueue=guiQueue, interval=10, controls=controls)
    u.start()
