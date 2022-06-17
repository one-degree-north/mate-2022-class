
import queue
import threading
import time

from controls import Controls

from thrusters import ThrustManager, displayTSpeeds
from keyboard import KeyManager, KeyMessage
from automation import PIDController

class Unifier():
    def __init__(self, q, KrishnaQ, interval, controls=None):
        self.TManager = ThrustManager(controls=controls)
        self.KManager = KeyManager(q=q)
        self.pidC = PIDController(interval, q=q, controls=controls)
        
        self.q = q
        self.KrishnaQ: queue.Queue() = KrishnaQ
        self.interval = interval
        
        self.readLasts = False

        self.lastFromKeyboard = KeyMessage()
        
        self.lastFromAutomation = [0,0,0]

        # allows/disallows automation to affect thruster speed calculations
        self.allowAutoInfluence = True

        self.combineType = self.getAverage

    def delegateFromQ(self):
        commandsReceived = 0
        while True:
            while self.q.qsize() != 0:




                commandsReceived += 1
                command = self.q.get()
                payload: KeyMessage = command[1]
                if command[0] == "k" and self.lastFromKeyboard != payload:

                    tare = payload.tare
                    if tare:
                        # print("\n\n\n\n\n\n\n")
                        self.pidC.tareAll()

                    command = payload.command
                    if command:
                        self.pidC.shiftTargetLeft()

                    self.lastFromKeyboard = payload
                    self.allowAutoInfluence = payload.allowAutoInfluence
                    self.pidC.isActive = self.allowAutoInfluence

        
                    self.readLasts = True
                elif command[0] == "a" and self.lastFromAutomation != payload:
                    # print("Delegating to automation")
                    self.lastFromAutomation = payload
                    self.readLasts = True

                if self.readLasts:
                    print(f"\n{self.lastFromKeyboard = }")
                    print(f"{self.lastFromAutomation = }")
                    print(f"{self.allowAutoInfluence = }")

                    reqMotion = self.lastFromKeyboard.reqMotion

                    reqRotation = self.lastFromKeyboard.reqRotation
                    if self.allowAutoInfluence:
                        reqRotation = self.combineType(reqRotation, self.lastFromAutomation)

                    displayTSpeeds(self.TManager.getTSpeeds(
                        reqMotion,
                        reqRotation,
                        self.lastFromKeyboard.thrustScale
                    ))

                    self.KrishnaQ.put(self.TManager.getTSpeeds(
                        reqMotion,
                        reqRotation,
                        self.lastFromKeyboard.thrustScale
                    ))



            time.sleep(self.interval * 0.001)  


    def getKrishnaQ(self):
        return self.KrishnaQ

    def initiateWrangling(self):
        self.KManager.startPolling()
        self.pidC.startListening()

        self.delegateThread = threading.Thread(target=self.delegateFromQ)
        self.delegateThread.start()

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
    controls = Controls()
    controls.setOrientationAutoreport(1)
    controls.comms.startThread()

    q = queue.Queue()
    kq = queue.Queue()
    unit = Unifier(q, kq, 10, controls=controls)
    unit.initiateWrangling()
