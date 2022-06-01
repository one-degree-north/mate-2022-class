class Controls:
    def __init__(self):

        pass

    def writeThruster(thrusterNum, value):
        #value is between -50 and 50
        #dc is between 0.25 and 0.5
        dc = (value*0.0025+0.375)
        