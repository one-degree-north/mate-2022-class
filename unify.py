
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
        self.lastFromKeyboard = ((0,0,0), (0,0,0))
        self.lastFromAutomation = (0,0,0)

    def delegateFromQ(self):
        while True:
            while self.q.qsize != 0:
                command = self.q.get()
                if command[0] == "k" and self.lastFromKeyboard != command[1]:
                    # print("Delegating to keyboard")
                    self.lastFromKeyboard = command[1]
                    self.readLasts = True
                elif command[0] == "a" and self.lastFromAutomation != command[1]:
                    # print("Delegating to automation")
                    self.lastFromAutomation = command[1]
                    self.readLasts = True

                if self.readLasts:
                    print(f"\n{self.lastFromKeyboard = }")
                    print(f"{self.lastFromAutomation = }")

                    # add coalesce code here

                    displayTSpeeds(self.TManager.getTSpeeds(
                        self.lastFromKeyboard[0],
                        self.lastFromKeyboard[1],
                        self.lastFromKeyboard[3]
                    ))

            time.sleep(self.interval * 0.001)  


    def initiateWrangling(self):
        self.delegateThread = threading.Thread(target=self.delegateFromQ)
        self.delegateThread.start()

if __name__ == "__main__":
    
    q = queue.Queue()
    TManager = ThrustManager()
    KManager = KeyManager(q=q)
    pidC = PIDController(10, q=q)
    unit = Unifier(TManager, q, 10)
    
    KManager.startPolling()
    pidC.startListening()
    unit.initiateWrangling()
