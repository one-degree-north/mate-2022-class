
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
            "reqMotion": (),
            "reqRotation": (),
            "thrustScale": 1,
            "toggleRotater": False,
            "toggleOpenner": False,
            "toggleAutomationMode": False,
            "targetShiftAmount": 0,
            "temp": False
        }
        self.lastPayloadFromAutomation = {"reqRotation": (0, 0, 0), "reqMotion": None,}

        # allows/disallows automation to affect thruster speed calculations
        # no longer in use...
        self.allowAutoInfluence = True
        # either "balancing", "full", or "off"
        # balancing excludes yaw, full includes it
        self.automationMode = "off"

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

                    # move servos 
                    # set automation mode
                    # set thrust scale
                    # set shift amount
                    if self.lastPayloadFromKeyboard["toggleOpenner"]:
                        self.SManager.openner.toggle()

                    if self.lastPayloadFromKeyboard["toggleRotater"]:
                        self.SManager.rotater.toggle()

                    if self.lastPayloadFromKeyboard["toggleAutomationMode"]:
                        # print("changing automation mode")
                        if self.automationMode == "balancing":
                            self.automationMode = "full"
                        elif self.automationMode == "full":
                            self.automationMode = "off"
                        else:
                            self.automationMode = "balancing"

                    if self.lastPayloadFromKeyboard["targetShiftAmount"] != 0:
                        print("Something.............................")
                        self.pidC.shiftTargetBy(self.lastPayloadFromKeyboard["targetShiftAmount"])

                    if self.lastPayloadFromKeyboard["temp"]:
                        self.pidC.override = False
                    
                    if self.lastPayloadFromKeyboard["temp2"]:
                        self.pidC.override = True

                    thrustScale = self.lastPayloadFromKeyboard["thrustScale"]


                    # calculate reqMotion and reqRotation based on automation mode

                    print(f"Automation mode: {self.automationMode}")
                    if self.lastPayloadFromAutomation["reqMotion"] == None:
                        reqMotion = self.lastPayloadFromKeyboard["reqMotion"]
                    else:
                        reqMotion = self.lastPayloadFromAutomation["reqMotion"]

                    if self.automationMode == "off":
                        reqRotation = self.lastPayloadFromKeyboard["reqRotation"]
                    elif self.automationMode == "balancing":
                        reqRotation = (self.lastPayloadFromAutomation["reqRotation"][0], 
                                       self.lastPayloadFromAutomation["reqRotation"][1], 
                                       self.lastPayloadFromKeyboard["reqRotation"][2])
                    elif self.automationMode == "full":
                        reqRotation = self.lastPayloadFromAutomation["reqRotation"]

                    # print(f"{reqRotation = }")



                    thrusterSpeeds = self.TManager.getTSpeeds(reqMotion, reqRotation, thrustScale)

                    displayTSpeeds(thrusterSpeeds)

                    self.guiQueue.put([thrusterSpeeds, reqRotation])

                    self.readLasts = False

            time.sleep(self.interval * 0.001)  


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
    # controls = None
    controls = Controls(offshoreEnabled=False)


    requestQueue = queue.Queue()
    guiQueue = queue.Queue()
    u = Unify(requestQueue=requestQueue, guiQueue=guiQueue, interval=10, controls=controls)
    u.start()
