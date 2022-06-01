from dataclasses import *
from pynput import keyboard

@dataclass
class Thruster:
    pinNum = 0
    writtenValue = 0

@dataclass
class Thrusters:
    front_left = 4 
    front_right = 3

    mid_left = 1
    mid_right = 0

    back_left = 5
    back_right = 2

@dataclass
class Servos:
    claw = 2
    # Not in use
    # claw_rotate = 1
    # camera = 2

@dataclass
class MovementKey:
    key: chr
    movementModify: list[int]
    horizontal: bool #horizontal or vertical, modifies how the average is calculated
    keydown: bool = False


class Keyboard:
    def __init__(self):
        self.keys = [
            MovementKey(key='w', movementModify=[], horizontal=True)
        ]

def main():
    keyboard = Keyboard()

if (__name__ == "__main__"):
    main()