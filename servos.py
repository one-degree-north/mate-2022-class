
class Servo():
    def __init__(self, minmax, controls):
        self.minmax = minmax
        self.controls = controls
        self.currState = 0

    def toggle(self):
        newState: int
        if (self.currState - self.minmax[0]) < (self.minmax[1] - self.currState):
            newState = self.minmax[1]
        else:
            newState = self.minmax[0]
        self.currState = newState

        if self.controls != None:
            self.controls.moveClaw(newState)

        print(newState)
        return newState

class ServoManager():
    def __init__(self, controls=None):
        self.controls = controls
        self.rotater = Servo(minmax=(0, 90), controls=controls)
        self.openner = Servo(minmax=(0, 1), controls=controls)
        
        if self.controls == None:
            print("\nFrom Servo Manager:\n\tControls not connected\n")


if __name__ == "__main__":
    from controls import Controls
    controls = Controls()
    controls.comms.startThread()

    s = ServoManager(controls=controls)
    s.openner.toggle()
            




