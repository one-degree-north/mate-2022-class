import socket, time
ESP_LOCAL_IP = "192.168.1.22"
PORT = 1122
BUFSIZE = 4096
HEADER = b'\xAB'
FOOTER = b'\xB3'

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
        else:
            print("AAAA")
    sock.sendall(FOOTER)

def readData():
    pass

def stopPump(sock):
    writeData(sock, [0x10, 0, 0])

def startPump(sock, seconds, speed):
    writeData(sock, [0x15, seconds, speed])

def setPressureAutoreport(sock, milliseconds):
    writeData(sock, [0x23, int.to_bytes(milliseconds, 2, "big")])

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ESP_LOCAL_IP, PORT))
    setPressureAutoreport(sock, 6969);
    while True:
        print(sock.recv(BUFSIZE))

if __name__ == "__main__":
    main()