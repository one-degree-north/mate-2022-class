#!/usr/bin/env python3
#not secure, client and server chatting program on the terminal
#unreliable due to nature of recv (packet loss)
#changes from v6: Admin added, changes with usernames
import argparse, socket, threading, queue, datetime, time, random, secrets, sys, struct
FOOTER = b'\xB3'
HEADER = b'\xAB'
BUFSIZE = 4096

def manageClient(sock, sockname):
    while True:
        print("sending data")
        time.sleep(0.01)
        sock.sendall(HEADER)
        sock.sendall(b'\x18')
        sock.sendall(struct.pack("=f", 3.21))
        sock.sendall(FOOTER)
    

def manageRecv(sock, sockname):
    pass

def recvData(self):
        dataRcv = self.sock.recv(BUFSIZE)
        self.bufferData.extend(dataRcv)
        headerIndexes = []
        i = 0
        while i < len(self.bufferData):
            byte = self.bufferData[i]
            if byte == HEADER and self.bufferData[i+7] == FOOTER:    #this may be error prone? What if header is dropped for some reason (TCP RELIABILITY LELELLELELELELE NVM RESIGN),
                self.processInput(dataRcv[i:i+7])
                headerIndexes.append(i)
                i += 6
            i += 1
        for i in headerIndexes: #delete read packets
            del dataRcv[i:i+7]

def server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(0)
    print('server set up at', sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print('new user at: ', sc.getpeername())
        messageThread = threading.Thread(target=manageClient,
                                         args=[sc, sockname]).start()
        sendThread = threading.Thread(target=manageRecv,
                                      args=[sc, sockname], name='message').start()

if __name__ == '__main__':
    server("192.168.0.133", 2020)

#possible features to add:
# more secure, get rid of accepting false requests
#sending time (do this for client, as timezones exist)
#
    
    
