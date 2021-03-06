#include <ESP8266WiFi.h>

#define TIMEOUT 600000 //milliseconds before removing socket
#define HEADER 0xAB
#define FOOTER 0xB3
#define PUMP_PIN 13
#define FREQUENCY 25000
#define PACKET_LENGTH 5
#define OFFSET 0.063
IPAddress localIPAdr = IPAddress(192,168,1,22);
IPAddress gateway = IPAddress(192,168,1,9);
IPAddress subnet = IPAddress(255,255,255,0);

WiFiServer server = WiFiServer(1122);
IPAddress espLocalIP;
WiFiClient connectedClients[4]; //maximum of 4 connections
bool openClients[4];
int clientIndex = 0;
int dc = 40;  //percentage, duty cycle is between 20% and 100% (I assume 20% is off)

typedef struct{  //0:Header 1:Command 2:Data 3:Footer
    WiFiClient currClient;
    int clientIndex;
    uint8_t command;
    uint8_t values[2];
}input_t;

typedef struct{
  uint16_t pressureDelay;
  long pressureTime;
} autoreport_t;

autoreport_t autoreportData;

void setup() {
  WiFi.softAPConfig(localIPAdr, gateway, subnet);
  WiFi.softAP("RESIGNMATE!!!", "crimsoncrimson");
  server.begin();
  espLocalIP = WiFi.localIP();
  autoreportData.pressureDelay = 10;
  autoreportData.pressureTime = 0;
  Serial.begin(115200);

  for (int i = 0; i < 4; i++){
    openClients[i] = true;
  }
}

void loop() {
  
  if (WiFiClient connectedClient = server.available()){ //new client connection
    Serial.print("connection with");
    Serial.println(connectedClient.localIP());
    bool openSlot = false;  //actually not sure if this is needed, would it just reject if over max connections?
    for (int i = 0; i < 4; i++){
      if (openClients[i]){
        openClients[i] = false;
        openSlot = true;
        connectedClients[i] = connectedClient;
        Serial.println("accepted client");
        break;
      }
    }
    if (!openSlot){
      Serial.println("too many clients");
      connectedClient.stop();
    }
  }
  for (int i = 0; i < 4; i++){
    WiFiClient currClient = connectedClients[i];
    
  }
  for (int i = 0; i < 4; i++){  //iterate through connections, read input
    WiFiClient currClient = connectedClients[i];
    if (currClient.available() >= 5){
      Serial.println("reading input");
      getInput(currClient, i);
    }
  }
}

void setDC(uint8_t newDC){
  dc = newDC;
  onLength = cycleLength * dc;
}

void writePWM( unsigned long deltaTime){  //dc ranges from 20-100
  currCycle += deltaTime;
  if (currCycle > cycleLength){
    currCycle -= cycleLength;
  }
  if (currCycle < onLength){
    digitalWrite(PUMP_PIN, HIGH);
  }
  else{
    digitalWrite(PUMP_PIN, LOW);
  }
}

void turnPumpOn(){
  setDC(100);
}

void turnPumpOff(){
  setDC(20);
}

bool getInput(WiFiClient currClient, int clientIndex){
  bool failed = false;
  uint8_t inputs[4];
  for (int i = 0; i < 5; i++){
    uint8_t input = currClient.read();
    Serial.println("reading");
    Serial.println(input);
    if ((i == 0 && input != HEADER) || (i == 4 && input != FOOTER)){
      Serial.println("no header found");
      writeCommandFailure(currClient);
      failed = true;
      return false;
    }
    inputs[i] = input;
  }
  if (!failed){
    input_t input;
    input.currClient = currClient;
    input.clientIndex = clientIndex;
    input.command = inputs[1];
    input.values[0] = inputs[2];
    input.values[1] = inputs[3];
    executeCommand(&input);
    return true;
  }
  else{
    writeCommandFailure(currClient);
    return false;
  }
  //can I cast inputs into input_t? Will padding and other stuff be an issue?
}

void executeCommand(input_t *input){
  Serial.println("execute command");
  bool commandFound = false;
  switch (input->command){
    case 0x10:  //stop pump
      commandFound = true;
      //input->currClient.write()
    break;
    case 0x15:  //move down for x seconds and y speed
      commandFound = true;
    break;
    case 0x23:  //set pressure autoreport in milliseconds
    {
      commandFound = true;
      uint16_t reportDelay = (((uint16_t)input->values[0])<<8)+input->values[1];
      autoreportData.pressureDelay = reportDelay;
      
      input->currClient.write(input->values[0]);
      input->currClient.write(input->values[1]);
      Serial.println("RECVpressure autoreport");
      Serial.println(reportDelay);
    }
    break;
    case 0x30:  //disconnect
      commandFound = true;
      input->currClient.stop();
      openClients[input->clientIndex] = true;
    break;
    case 0x36:  //renew timeout
      commandFound = true;
    break;
    case 0x41:
      commandFound = true;
    break;
  }
  if (commandFound){
    writeCommandSuccess(input);
  }
  else{
    writeCommandFailure(input->currClient);
  }
}

void pressureAutoreport(unsigned long deltaTime){
  if (autoreportData.pressureDelay != 0){
    if (deltaTime >= autoreportData.pressureTime){
      autoreportData.pressureTime = autoreportData.pressureDelay-(deltaTime - autoreportData.pressureTime);
      sendPressureData();
    }
    else{
      autoreportData.pressureTime -= deltaTime;
    }
  }
}

void readWaterPressure(){
  //get water pressure data here
  float waterPressure;
  byte* byteCastWaterPressure = (byte*)&waterPressure;
  currClient.write(HEADER);
  currCLient.write(0x18);
  currClient.write(byteCastWaterPressure[0]);
  currClient.write(byteCastWaterPressure[1]);
  currClient.write(byteCastWaterPressure[2]);
  currClient.write(byteCastWaterPressure[3]);
  currClient.write(FOOTER);
}

void writeCommandFailure(WiFiClient currClient){
  currClient.write(HEADER);
  currClient.write(0x18);
  currClient.write(0);
  currClient.write(0);
  currClient.write(0);
  currClient.write(0);
  currClient.write(FOOTER);
}

void writeCommandSuccess(input_t *input){
  currClient.write(HEADER);
  currClient.write(0x34);
  currClient.write(0);
  currClient.write(0);
  currClient.write(0);
  currClient.write(0);
  currClient.write(FOOTER);
}

void writeCommandExecute(input_t *input){  //does TCP already kind of give reliability, is echoing the whole command to certify reliability needed? Would a simple writeCommandSuccess sufice?

}

void sendPressureData(){
  //get pressure data
  float V = analogRead(A0) * 5.00 / 1024;     //Sensor output voltage
  float P = (V - OFFSET) * 250;             //Calculate water pressure
  byte* byteCastPressure = (byte*)&P;
  for (int i = 0; i < 4; i++){
    if(openClients[i]){
      WiFiClient currClient = connectedClients[i];
      currClient.write(HEADER);
      currClient.write(0x53);
      currClient.write(byteCastPressure[0]);
      currClient.write(byteCastPressure[1]);
      currClient.write(byteCastPressure[2]);
      currClient.write(byteCastPressure[3]);
      currClient.write(FOOTER);
    }
  }
}
