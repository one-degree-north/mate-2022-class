//#define Serial Serial1
#include <Servo.h>
//#define Serial Serial1
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

int HEADER = 0xAB;
int FOOTER = 0xB3;

struct Input{
  uint8_t command;
  uint8_t paramNum;
  uint8_t values[6];
};

int thrusterPins[] = {7, 9, 10, 11, 12, 13};
Servo thrusters[6];
int servoPins[] = {3, 4, 5}
Servo clawServos[3];

Adafruit_BNO055 bnoIMU = Adafruit_BNO055(55, 0x28);
AutoreportData autoData;
unsigned long pastMillis;

void setup(){
  for (int i = 0; i < 6; i++){
    thrusterServos[i].attach(thrusterPins[i]);
  }
  for (int i = 0; i < 3; i++){
    clawServos[i].attach(clawPins[i], 1200, 1800);
  }
  Serial.begin(115200);
}

void loop(){
  readInput();
}

int packetIndex = 0;
Input inputValue;
void readInput(){
  if (Serial.available()){
    int input = Serial.read();
    if (packetIndex == 0){
      if (input != HEADER){
        packetIndex--;
      }
    }
    else if (packetIndex == 1){
      inputValue.command = input;
    }
    else if (packetIndex >= 2){
      if (input == FOOTER){
        inputValue.paramNum = packetIndex-2;
        processCommand(inputValue);
        packetIndex = -1;
      }
      else if (packetIndex > 8){
        packetIndex = -1;
      }
      else{
        inputValue.value[packetIndex-2] = input;
      }
    }
    packetIndex++;
  }
}

void processCommand(Input inputValue){
  switch(inputValue.command){
    case 0x14: //provides all thruster values
      if(inputValue.paramNum != 6){
        break;
      }
      moveMultipleThrusters(inputValue);
    break;
    case 0x1C: //move claw servo
      if (inputValue.paramNum != 1){
        break;
      }
      moveClawServo(inputValue);
    break;
    case 0x32: //halt
      if (inputValue.paramNum != 0){
        break;
      }
      halt(inputValue);
    break;
    case 0x50: //
      
    break;
  }
}

void moveMultipleThrusters(Input inputValue){
  for (int i = 0; i < 6; i++){
    thrusterPins[i].writeMicroseconds(inputValue.values[i]*10);
  }
}

void moveClawServo(Input inputValue){
  clawServos[0].write(inputValue*2);
}

void halt(Input inputValue){
  for (int i = 0; i < 6; i++){
    thrusterPins[i].writeMicroseconds(1500);
  }
}
