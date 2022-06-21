import socket, time, struct

from numpy import byte
ESP_LOCAL_IP = "192.168.1.22"
PORT = 1122
BUFSIZE = 4096
HEADER = b'\xAB'
FOOTER = b'\xB3'

bufferData = bytearray()
def writeData(sock, values):
    sock.sendall(HEADER)
    print(HEADER)
    print(int.from_bytes(HEADER, "big"))
    for value in values:
        print(value)
        if type(value) == bytes or type(value) == bytearray:
            sock.sendall(value)
        elif type(value) == int:
            sock.sendall(int.to_bytes(value, 1, "big"))
        elif type(value) == str:
            for i in len(value):
                sock.sendall(int.to_bytes(ord(value[i]), 1, "big"))
        else:
            print("AAAA")
    sock.sendall(FOOTER)

def recvData(sock):
    dataRcv = sock.recv(BUFSIZE)
    bufferData.extend(dataRcv)
    headerIndexes = []
    i = 0
    while i < len(bufferData):
        byte = bufferData[i]
        if byte == HEADER and bufferData[i+7] == FOOTER:    #this may be error prone? What if header is dropped for some reason (TCP RELIABILITY LELELLELELELELE NVM RESIGN),
            processInput(sock, dataRcv[i:i+7])
            headerIndexes.append(i)
            i += 6
        i += 1
    for i in headerIndexes: #delete read packets
        del dataRcv[i:i+7]
    #print(bufferData)   #for debugging
    #if the buffer doesn't start with a header for some reason, remove it until the last header. Actually tcp may be reliable enough, not going to bother with this as more errors could be introduced

def processInput(sock, inputBytes):
    if inputBytes[1] == b'\x18': #water pressure data
        inputStruct = struct.unpack("=ccfc", inputBytes)
        print(f"water pressure: {inputStruct[2]}")
    elif inputBytes[1] == b'\x41':
        inputStruct = struct.unpack("=ccccccc", inputBytes) #I probably don't need this but who cares, nobody reads these comments so you don't exist.
        echoValues = inputStruct[2:6].decode("ascii")
        print(f"echo values: {echoValues}")

def plotWaterPressure():
    pass

def echo(sock, chars):
    writeData(sock, chars)

def stopPump(sock):
    writeData(sock, [0x10, 0, 0])

def startPump(sock, seconds, speed):
    writeData(sock, [0x15, seconds, speed])

def startPumpNoStop(sock, speed):
    writeData(sock, [0x36, speed])

def setPressureAutoreport(sock, milliseconds):
    writeData(sock, [0x23, int.to_bytes(milliseconds, 2, "big")])

def disconnect(sock):
    sock.shutdown()
    sock.close()

def handleInput(sock, inputStr):
    delinIndexs = []
    for i in len(inputStr):
        char = inputStr[i]
        if char == ' ':
            delinIndexs.append(i)
    command = ""
    params = []
    if len(delinIndexs) == 0:
        pass
    else:
        lastIndex = 0
        for i in range(len(delinIndexs)):
            if i == 0:
                command = inputStr[0:i]
            else:
                params.append(inputStr[lastIndex:i])
            lastIndex = i
        params.append(inputStr[lastIndex+1:])
    if command == "halt":
        stopPump(sock)
    elif command == "spd":  #start pump with delay
        if len(params) == 2:
            startPump(sock, params[0], int(params[1]))
    elif command == "spi'": #start pump indefinetly
        if len(params) >= 1:
            startPumpNoStop(sock, int(params[0]))
    elif command == "auto":  #set autoreport
        if len(params) == 1:
            setPressureAutoreport(sock, int(params[0]))
    elif command == "dc":   #disconnect
        disconnect(sock)
    elif command == "echo":
        if len(params) == 1:
            echo(sock, params[0])

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ESP_LOCAL_IP, PORT))
    while True:
        print(sock.recv(BUFSIZE))

if __name__ == "__main__":
    main()