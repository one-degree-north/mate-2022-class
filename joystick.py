#TESTING CODE ATM, VERY SCUFFED
import hashlib, hid, time
from struct import unpack


"""def update(inputTest) : ...
joystickInput = open(r"/dev/input/js0", "rb")
def main():
    fileHash = ""
    while True:
        inputTest = joystickInput.read(7)
        newFileHash = hashlib.sha256()
        newFileHash.update(inputTest)
        newFileHashValue = newFileHash.digest()
        if newFileHashValue != fileHash:
            fileHash = newFileHashValue
            update(inputTest)
            # Logic here
    

def update(inputTest):
    #print(inputTest)
    print("Size :" + str(len(inputTest)))
    print(unpack('IBBB', inputTest))
"""

def hidTest():
    deviceNum = 49685
    for device_dict in hid.enumerate():
        keys = list(device_dict.keys())
        keys.sort()
        #for key in keys:
        #    print("%s : %s" % (key, device_dict[key]))
        print(device_dict["product_id"])
        print(device_dict["vendor_id"])
    joy = hid.device()
    joy.open(vendor_id=1133, product_id=49685)
    pastJoyInput = None
    while True:
        readHid2(joy)

def readHid(joy):
    joyInput = joy.read(7)
    #xAxis = (joyInput[0]*4) + (joyInput[1] // 64)
    xAxis = joyInput[0]*16 + joyInput[1]//16
    # xAxis = ((joyInput[1] & 0b11000000) << 2) + joyInput[0]
    yAxis = ((joyInput[1] << 4) + (joyInput[2] >> 4)) & 1023
    hat = (joyInput[2])&15
    print(joyInput)
    print(f"hat: {hat}")
    #print(joyInput[0] << 2)
    #print(joyInput[1] >> 6)
    print(f"xAxis: {xAxis}")

    #print((joyInput[1] << 4)&1023)
    #print(joyInput[2] >> 4)
    print(f"yAxis: {yAxis}")
    time.sleep(0.01)

def readHid2(joy):
    joyInput = joy.read(7)
    test = joyInput[0]*256+joyInput[1]
    print(str(bin(test))[2:].zfill(16))

if(__name__ == "__main__"):
    hidTest()