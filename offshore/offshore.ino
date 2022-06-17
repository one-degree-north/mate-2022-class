//#define Serial Serial1
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

int HEADER = 0xAB;
int FOOTER = 0xB3;

struct Input{
  uint8_t command;
  uint8_t value;
};

struct AutoreportData{
  long gyroDelay;
  long accelDelay;
  long orientationDelay;
  long gyroTime;
  long accelTime;
  long orientationTime;
};

Adafruit_BNO055 bnoIMU = Adafruit_BNO055(55, 0x28);
AutoreportData autoData;
unsigned long pastMillis;


void setup(){
  Serial.begin(115200);
  bnoIMU.begin();
  pastMillis = millis();
  autoData.gyroDelay = 10;
  autoData.accelDelay = 10;
  autoData.orientationDelay = 10;
  autoData.gyroTime = 0;
  autoData.accelTime = 0;
  autoData.orientationTime = 0;
}

void loop(){
  unsigned long now = millis();
  unsigned long deltaTime = now - pastMillis;
  pastMillis = now;
  readInput();
  autoreport(deltaTime);
}

void autoreport(unsigned long deltaTime){
  if (autoData.gyroDelay != 0){
    if (deltaTime >= autoData.gyroTime){
      autoData.gyroTime = autoData.gyroDelay-(deltaTime - autoData.gyroTime);
      writeGyroOutput();
    }
    else{
      autoData.gyroTime -= deltaTime;
    }
  }
  if (autoData.accelDelay != 0){
    if (deltaTime >= autoData.accelTime){
      autoData.accelTime = autoData.accelDelay-(deltaTime - autoData.accelTime);
      writeAccelOutput();
    }
    else{
      autoData.accelTime -= deltaTime;
    }
  }
  if (autoData.orientationDelay != 0){
    if (deltaTime >= autoData.orientationTime){
      autoData.orientationTime = autoData.orientationDelay-(deltaTime - autoData.orientationTime);
      writeOrientationOutput();
    }
    else{
      autoData.orientationTime -= deltaTime;
    }
  }
}

int packetIndex = 0;
Input inputValue;
void readInput(){
  if (Serial.available()){
    int input = Serial.read();
    //Serial.write(input);
    //Serial.print(packetIndex);
    if (packetIndex <= 0){
      if (input != HEADER){
        packetIndex--;
      }
    }
    else if (packetIndex == 1){
      inputValue.command = input;
    }
    else if (packetIndex == 2){
      inputValue.value = input;
    }
    if (packetIndex >= 3){
      if (input == FOOTER){
        processCommand(inputValue);
      }
      packetIndex = -1;
    }
    packetIndex++;
  }
}

void processCommand(Input inputValue){
  switch(inputValue.command){
    case 0x10: //send accel data once
      writeAccelOutput();
    break;
    case 0x12: //set accel auto report
      autoData.accelDelay = inputValue.value*10;
      autoData.accelTime = 0;
    break;
    case 0x20: //send gyro data once
      writeGyroOutput();
    break;
    case 0x23: //set gyro auto report
      autoData.gyroDelay = inputValue.value*10;
      autoData.gyroTime = 0;
    break;
    case 0x30:  //get orientation data once
      writeOrientationOutput();
    break;
    case 0x35:  //set orientation auto report
      autoData.orientationDelay = inputValue.value*10;
      autoData.orientationTime = 0;
    break;
    case 0x40:  //reset adafruit qtpy along with bno055
      NVIC_SystemReset();
    break;
    case 0x45:  //return offshore or onshore
      writeOffshore();
    break;
  }
}

void writeOffshore(){ //indicates that the board is offshore
  uint8_t offshore = 0x15;
  Serial.write(HEADER);
  Serial.write(0x15);
  Serial.write(offshore);
  Serial.write(FOOTER);
}

void writeOrientationOutput(){
  sensors_event_t event;
  bnoIMU.getEvent(&event, Adafruit_BNO055::VECTOR_EULER);
  byte* x = (byte*)&event.orientation.x;
  byte* y = (byte*)&event.orientation.y;
  byte* z = (byte*)&event.orientation.z;
  Serial.write(HEADER);
  Serial.write(0x23);
  Serial.write(x[0]);
  Serial.write(x[1]);
  Serial.write(x[2]);
  Serial.write(x[3]);
  Serial.write(y[0]);
  Serial.write(y[1]);
  Serial.write(y[2]);
  Serial.write(y[3]);
  Serial.write(z[0]);
  Serial.write(z[1]);
  Serial.write(z[2]);
  Serial.write(z[3]);
  Serial.write(FOOTER);
}

void writeGyroOutput(){
  sensors_event_t event;
  bnoIMU.getEvent(&event, Adafruit_BNO055::VECTOR_GYROSCOPE);
  byte* x = (byte*)&event.orientation.x;
  byte* y = (byte*)&event.orientation.y;
  byte* z = (byte*)&event.orientation.z;
  Serial.write(HEADER);
  Serial.write(0x20);
  Serial.write(x[0]);
  Serial.write(x[1]);
  Serial.write(x[2]);
  Serial.write(x[3]);
  Serial.write(y[0]);
  Serial.write(y[1]);
  Serial.write(y[2]);
  Serial.write(y[3]);
  Serial.write(z[0]);
  Serial.write(z[1]);
  Serial.write(z[2]);
  Serial.write(z[3]);
  Serial.write(FOOTER);
}

void writeAccelOutput(){
  sensors_event_t event;
  bnoIMU.getEvent(&event, Adafruit_BNO055::VECTOR_ACCELEROMETER);
  byte* x = (byte*)&event.acceleration.x;
  byte* y = (byte*)&event.acceleration.y;
  byte* z = (byte*)&event.acceleration.z;
  Serial.write(HEADER);
  Serial.write(0x10);
  Serial.write(x[0]);
  Serial.write(x[1]);
  Serial.write(x[2]);
  Serial.write(x[3]);
  Serial.write(y[0]);
  Serial.write(y[1]);
  Serial.write(y[2]);
  Serial.write(y[3]);
  Serial.write(z[0]);
  Serial.write(z[1]);
  Serial.write(z[2]);
  Serial.write(z[3]);
  Serial.write(FOOTER);
}
