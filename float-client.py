import socket, time, struct, asyncio, curses

from numpy import byte
ESP_LOCAL_IP = "192.168.1.22"
PORT = 1122
BUFSIZE = 4096
HEADER = b'\xAB'
FOOTER = b'\xB3'

class Client:
    def __init__(self):
        self.bufferData = bytearray()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ESP_LOCAL_IP, PORT))

    def writeData(self, values):
        self.sock.sendall(HEADER)
        print(HEADER)
        print(int.from_bytes(HEADER, "big"))
        sentParams = 0
        for value in values:
            print(value)
            if type(value) == bytes or type(value) == bytearray:
                sentParams += len(value)
                self.sock.sendall(value)
            elif type(value) == int:
                sentParams += 1
                self.sock.sendall(int.to_bytes(value, 1, "big"))
            elif type(value) == str:
                for i in len(value):
                    sentParams += 1
                    self.sock.sendall(int.to_bytes(ord(value[i]), 1, "big"))
            else:
                print("AAAA")
        if sentParams < 3:
            print(f"sendParams: {sentParams}, sending {3-sentParams}")
            for i in (3 - sentParams):
                self.sock.sendall(b'\x00')
        self.sock.sendall(FOOTER)

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
        #print(bufferData)   #for debugging
        #if the buffer doesn't start with a header for some reason, remove it until the last header. Actually tcp may be reliable enough, not going to bother with this as more errors could be introduced

    def processInput(self, inputBytes):
        if inputBytes[1] == b'\x18': #water pressure data
            inputStruct = struct.unpack("=ccfc", inputBytes)
            print(f"water pressure: {inputStruct[2]}")
        elif inputBytes[1] == b'\x41':
            inputStruct = struct.unpack("=ccccccc", inputBytes) #I probably don't need this but who cares, nobody reads these comments so you don't exist.
            echoValues = inputStruct[2:6].decode("ascii")
            print(f"echo values: {echoValues}")

    def plotWaterPressure():
        pass

    def echo(self, chars):
        self.writeData(chars)

    def stopPump(self):
        self.writeData([0x10, 0, 0])

    def startPump(self, milliseconds, speed):
        self.writeData([0x15, int.to_bytes(milliseconds, 2, "big"), speed])

    def startPumpNoStop(self, speed):
        self.writeData([0x36, speed, 0, 0])

    def setPressureAutoreport(self, milliseconds):
        self.writeData([0x23, int.to_bytes(milliseconds, 2, "big"), 0])

    def disconnect(self):
        self.sock.shutdown()
        self.sock.close()
            #terminate gui

class InputWin:
    def __init__(self, stdscr, height, width, y, x):
        self.stdscr = stdscr
        self.win = curses.newwin(height, width, y, x)
        #curses.echo()
        stdscr.refresh()
    def getInput(self):
        inputVal = (self.win.getstr(0, 0, 15)).decode("ascii")
        return inputVal

class ScrollingScreen:
    def __init__(self, stdscr, height, width, y, x):
        self.win = curses.newwin(height, width, y, x)
        self.height = height
        self.width = width
        stdscr.refresh()
        self.strings = []
    
    def addStr(self, string):
        self.strings.append(string)
        self.win.erase()
        if len(self.strings) < self.height:
            for i in range(len(self.strings)):
                self.win.addstr(i, 0, self.strings[i])
        else:
            for i in range(self.height):
                self.win.addstr(i, 0, self.strings[len(self.strings)-self.height + i])
        self.win.refresh()

class UI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        stdscr.keypad(True)
        self.inputWin = InputWin(stdscr, curses.LINES-1, curses.COLS-1, 0, 0)
        self.infoWin = curses.newwin(6, 57, 2, curses.COLS-59)
        stdscr.refresh()
        self.infoWin.addstr(0, 0, "halt: no param: stops thrusters from spinning")
        self.infoWin.addstr(1, 0, "spd: duration in ms, duty cycle: start pump with duration")
        self.infoWin.addstr(2, 0, "spi: duty cycle: starts pump indefinetly")
        self.infoWin.addstr(3, 0, "auto: milliseconds: set autoreport")
        self.infoWin.addstr(4, 0, "dc no param: disconnect")
        self.infoWin.addstr(5, 0, "echo: 4 chars: echos characters back")
        self.infoWin.refresh()
        self.dataWin = ScrollingScreen(stdscr, curses.LINES-3, curses.COLS-59, 2, 0)
        self.reportWin = ScrollingScreen(stdscr, curses.LINES-12, 57, 11, curses.COLS-59)
        stdscr.refresh()

class InputHandler:
    def __init__(self, client=None):
        self.client = client
    
    def getInput(self):
        print("AAAA")
        #yield from input("eee")
        inputStr = yield from input("input here> ")
        print(inputStr)
        #self.handleInput(inputStr)
        print("BBB")

    def handleInput(self, inputStr):
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
            self.client.stopPump()
        elif command == "spd":  #start pump with delay
            if len(params) == 2:
                try:
                    self.client.startPump(int(params[0]), int(params[1]))
                except:
                    print("param does not match int")
        elif command == "spi'": #start pump indefinetly
            if len(params) >= 1:
                try:
                    self.client.startPumpNoStop(int(params[0]))
                except:
                    print("param does not match int")
        elif command == "auto":  #set autoreport
            if len(params) == 1:
                try:
                    self.client.setPressureAutoreport(int(params[0]))
                except:
                    print("param does not match int")
        elif command == "dc":   #disconnect
            self.client.disconnect()
        elif command == "echo":
            if len(params) == 1:
                self.client.echo(params[0])

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ESP_LOCAL_IP, PORT))
    while True:
        print(sock.recv(BUFSIZE))

def cursesTest(stdscr):
    """stdscr.keypad(True)

    infoWin = curses.newwin(15, 50, 0, 25)
    stdscr.refresh()
    infoWin.addstr(0, 0, "halt: no param: stops thrusters from spinning")
    infoWin.addstr(1, 0, "spd: duration in ms, duty cycle: start pump with duration")
    infoWin.addstr(2, 0, "spi: duty cycle: starts pump indefinetly")
    infoWin.addstr(3, 0, "auto: milliseconds: set autoreport")
    infoWin.addstr(4, 0, "dc no param: disconnect")
    infoWin.addstr(5, 0, "echo: 4 chars: echos characters back")
    infoWin.refresh()
    #statusWin = curses.newwin(curses.COLS, curses.LINES, 0, 0)
    #inputWin = curses.newwin()
    while True:
        continue"""
    ui = UI(stdscr)
    i = 0
    while True:
        i += 1
        time.sleep(0.01)
        ui.dataWin.addStr(f"{i}")
        ui.reportWin.addStr(f"ddd{i}")

if __name__ == "__main__":
   #asyncio.run(testAsync())
   curses.wrapper(cursesTest)