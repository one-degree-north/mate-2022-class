import socket
ESP_LOCAL_IP = "192.168.1.22"
PORT = 1122
BUFSIZE = 4096
HEADER = b'0xAB'
FOOTER = b'0xB3'

def readData():
    pass

def main():
    sock = socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ESP_LOCAL_IP, PORT))

if __name__ == "__main__":
    main()