class Servo():
    def __init__(self, minmax, controls, servoType, incrementAmount):
        self.minmax = minmax
        self.controls = controls
        self.currState = minmax[0]
        self.servoType = servoType
        self.incrementAmount = incrementAmount

    def toggle(self):
        newState: int
        if (self.currState - self.minmax[0]) < (self.minmax[1] - self.currState):
            newState = self.minmax[1]
        else:
            newState = self.minmax[0]
        self.currState = newState

        if self.controls != None:
            if self.servoType == "claw":
                self.controls.moveClaw(newState)
            else:
                self.controls.rotateClaw(newState)
        print(newState)
        return newState
    
    def increment(self):
        self.currState += self.incrementAmount
        if self.controls != None:
            if self.servoType == "claw":
                self.controls.moveClaw(self.currState)
            else:
                self.controls.rotateClaw(self.currState)
        
class ServoManager():
    def __init__(self, controls=None):
        self.controls = controls
        self.rotater = Servo(minmax=(0, 90), controls=controls, servoType="rotate", incrementAmount=5)
        self.openner = Servo(minmax=(0, 1), controls=controls, servoType="claw", incrementAmount=0.1)
        
        if self.controls == None:
            print("\nMessage from Servos:\n\tControls not connected\n")


if __name__ == "__main__":
    from controls import Controls
    controls = Controls()
    controls.comms.startThread()

    s = ServoManager(controls=controls)
    while True:
        test = input(">\n")
        s.rotater.toggle()
    s.openner.toggle()