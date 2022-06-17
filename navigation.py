import time

def time_delay(distance, acceleration):
    # d = 0.5at^2
    delay = sqrt(d * 2.0 / a)
    return delay
    

def move_forward(distance: float):
    # Kevin: Start thrusters to go forward
    length_of_packet = 9
    baud_rate = 115200 # or whatever it is
    delay = (length_of_packet + 2) / baud_rate
    time.sleep(delay)
    # Kevin/Alan: Get BNO Acceleration
    delay = time_delay(distance, accel)
    time.sleep(delay)
    # Kevin: Stop thrusters from going forward