
from thrusters import Thruster
from joystick import Joystick
from automation import Automator

from controls import Controls

import threading
from time import sleep

import datetime


sampInterval = 10 # in milliseconds
thrustMultiplier = 1 


controls = Controls()
#controls.setOrientationAutoreport(sampInterval * 0.1)
controls.comms.startThread()

balancer = Automator(sampInterval, controls)

joystick = Joystick()

frontL = Thruster(pin=0, powerMatrix=(0, 0, 1), position=(-1, 1))
frontR = Thruster(pin=1, powerMatrix=(0, 0, 1), position=( 1, 1))
backL  = Thruster(pin=2, powerMatrix=(0, 0, 1), position=(-1,-1))
backR  = Thruster(pin=3, powerMatrix=(0, 0, 1), position=( 1,-1))
sideL  = Thruster(pin=4, powerMatrix=(0, 1, 0), position=(-1, 0))
sideR  = Thruster(pin=5, powerMatrix=(0, 1, 0), position=( 1, 0))

def doMath(controls, balancer: Automator, joystick: Joystick):
    intendedRotation = balancer.forces()

    joystick.readJoyData()
    intendedMotion = (
        0,
        joystick.joyData.yAxis,
        0
    )

    thrusterSpeeds = Thruster.determine(
        intendedMotion=intendedMotion,
        intendedRotation=intendedRotation,
        multiplier=1
    )

    return thrusterSpeeds

def main(interval):
    # startTime = datetime.datetime.now()
    while True:
        # currTime = datetime.datetime.now()
        # timeDiff = currTime - startTime
        # timeElapsed = timeDiff.total_seconds() * 1000 # in milliseconds
        thrusterSpeeds = doMath(controls=controls, balancer=balancer, joystick=joystick)
        print(f"thrusterSpeed: {thrusterSpeeds}")
        controls.writeAllThrusters(thrusterSpeeds)
        sleep(sampInterval * 0.001)

if __name__ == "__main__":
    main(sampInterval)