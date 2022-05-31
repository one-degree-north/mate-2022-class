from dataclasses import dataclass
from pynput import keyboard

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
    char = 'w'
    movementModify = []


class Keyboard:
    def __init__(self):
        pass