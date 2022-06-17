//#define Serial Serial1
#include <Servo.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

int HEADER = 0xAB;
int FOOTER = 0xB3;

struct Input{
  uint8_t command;
  uint8_t paramNum;
  uint8_t values[6];
};

int thrusterPins[] = {4, 3, 6, 7, 8, 5};
Servo thrusters[6];
int servoPins[] = {10, 11};
Servo clawServos[2];

Adafruit_BNO055 bnoIMU = Adafruit_BNO055(55, 0x28);
unsigned long pastMillis;

void setup(){
  for (int i = 0; i < 6; i++){
    thrusters[i].attach(thrusterPins[i]);
  }
  for (int i = 0; i < 2; i++){
    clawServos[i].attach(servoPins[i]);
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
        inputValue.values[packetIndex-2] = input;
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
    case 0x5A:
      if (inputValue.paramNum != 1){
        break;
      }
      rotateClaw(inputValue);
    break;
    case 0x32: //halt
      if (inputValue.paramNum != 0){
        break;
      }
      halt(inputValue);
    break;
    case 0x45: //return offshore or onshore
      writeOnshore();
    break;
  }
}
void writeOnshore(){  //Indicates that this board is the onshore board
  uint8_t onshore = 0x10;
  Serial.write(HEADER);
  Serial.write(0x15);
  Serial.write(onshore);
  Serial.write(FOOTER);
}

void moveMultipleThrusters(Input inputValue){
  for (int i = 0; i < 6; i++){
    thrusters[i].writeMicroseconds(inputValue.values[i]*10);
  }
}

void moveSingleThruster(Input inputValue){
  thrusters[inputValue.values[0]].writeMicroseconds(inputValue.values[1]*10);
}

void rotateClaw(Input inputValue){
  //uint16_t deg = (inputValue.values[0]<<8) + inputValue.values[1];
  //Serial.println(deg);
  clawServos[1].write(inputValue.values[0]);
}

void moveClawServo(Input inputValue){
  //uint16_t deg = (inputValue.values[0]<<8) + inputValue.values[1];
  clawServos[0].write(inputValue.values[0]); //I'm not sure if the system uses small or big endian, too lazy to check
}

void halt(Input inputValue){
  for (int i = 0; i < 6; i++){
    thrusters[i].writeMicroseconds(1500);
  }
}
