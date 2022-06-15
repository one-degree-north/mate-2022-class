
import queue
import threading
import time

from thrusters import ThrustManager, displayTSpeeds
from keyboard import KeyManager
from automation import PIDController

class Unifier():
    def __init__(self, TManager: ThrustManager, q, interval):
        self.TManager = TManager
        self.q = q
        self.interval = interval
        
        self.readLasts = False

        self.lastFromKeyboard = ((0,0,0), (0,0,0), 0, 1)
        # [0] -> reqMotion
        # [1] -> reqRotation
        # [2] -> clawAngle
        # [3] -> thrustScale


        self.lastFromAutomation = (0,0,0)

        # allows/disallows automation to affect thruster speed calculations
        self.allowAutoInfluence = True

        self.combineType = self.getAverage

    def delegateFromQ(self):
        while True:
            while self.q.qsize != 0:
                command = self.q.get()
                if command[0] == "k" and self.lastFromKeyboard != command[1]:
                    # print("Delegating to keyboard")
                    self.lastFromKeyboard = command[1][0:4]
                    self.allowAutoInfluence = command[1][4]
                    self.readLasts = True
                elif command[0] == "a" and self.lastFromAutomation != command[1]:
                    # print("Delegating to automation")
                    self.lastFromAutomation = command[1]
                    self.readLasts = True

                if self.readLasts:
                    print(f"\n{self.lastFromKeyboard = }")
                    print(f"{self.lastFromAutomation = }")
                    print(f"{self.allowAutoInfluence = }")



                    reqMotion = self.lastFromKeyboard[0]

                    reqRotation = self.lastFromKeyboard[1]
                    if self.allowAutoInfluence:
                        reqRotation = self.combineType(self.lastFromKeyboard[1], self.lastFromAutomation)


                    # add coalesce code here
                    # print(f"{self.lastFromKeyboard[0] = }")
                    # print(f"{self.lastFromKeyboard[1] = }")
                    # print(f"{self.lastFromKeyboard[2] = }")


                    displayTSpeeds(self.TManager.getTSpeeds(
                        reqMotion,
                        reqRotation,
                        self.lastFromKeyboard[3]
                    ))

            time.sleep(self.interval * 0.001)  


    def initiateWrangling(self):
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
    TManager = ThrustManager()
    KManager = KeyManager(q=q)
    pidC = PIDController(10, q=q)
    unit = Unifier(TManager, q, 10)
    
    KManager.startPolling()
    pidC.startListening()
    unit.initiateWrangling()
