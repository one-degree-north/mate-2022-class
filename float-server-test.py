import socket
HEADER = b'\xAB'
FOOTER = b'\xB3'
openClients = [True, True, True, True]
connectedClients = [None, None, None, None]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind("198.168.0.1", 1122)
server.listen()