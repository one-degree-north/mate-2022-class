
import queue
import threading
import time

from controls import Controls

from thrusters import ThrustManager, displayTSpeeds
from keyboard import KeyManager, KeyMessage
from automation import PIDController

class Unifier():
    def __init__(self, q, interval, controls=None):
        self.TManager = ThrustManager(controls=controls)
        self.KManager = KeyManager(q=q)
        self.pidC = PIDController(interval, q=q, controls=controls)
        self.pidC.roll.kp = 0.01
        self.pidC.roll.kd = 0.01
        
        self.q: queue.Queue() = q
        self.interval = interval
        
        self.readLasts = False

        self.lastFromKeyboard = ((0,0,0), (0,0,0), 0, 1, True, False)
        # [0] -> reqMotion
        # [1] -> reqRotation
        # [2] -> clawAngle
        # [3] -> thrustScale
        # [4] -> influence
        # [5]


        self.lastFromAutomation = (0,0,0)

        # allows/disallows automation to affect thruster speed calculations
        self.allowAutoInfluence = True

        self.combineType = self.getAverage

    def delegateFromQ(self):
        commandsReceived = 0
        while True:
            while self.q.qsize() != 0:
                # commandsReceived += 1
                # print(f"{commandsReceived = }")
                commandsReceived += 1
                command = self.q.get()
                payload: KeyMessage = command[1]
                if command[0] == "k" and self.lastFromKeyboard != payload:

                    tare = payload.tare
                    if tare:
                        self.pidC.tareAll()

                    self.lastFromKeyboard = payload
                    self.allowAutoInfluence = payload.allowAutoInfluence
        
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

            time.sleep(self.interval * 0.001)  


    def initiateWrangling(self):
        self.KManager.startPolling()
        self.pidC.startListening()

        self.delegateThread = threading.Thread(target=self.delegateFromQ)
        self.delegateThread.start()

    def getAverage(self, data1, data2):
        # print(f"{data1 = }")
        output = []
        for indexNo, _ in enumerate(data1):
            output.append((data1[indexNo] + data2[indexNo]) / 2)

        return output

if __name__ == "__main__":    
    q = queue.Queue()
    unit = Unifier(q, 10)
    unit.initiateWrangling()
