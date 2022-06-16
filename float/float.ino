#include <Servo.h>
#define UNDERWATER_TIME_MS 1000
#define ABOVE_TIME_MS 1000
#define PUMP_PIN 15
#define ITERATIONS 5
#define frequency = 25000;
float dc = 0.4;

Servo pump;
unsigned long now;
boolean finished = false;

void setup() {
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(13, INPUT);
  pump.attach(8);
  now = millis();
}

void loop() {
  if (!finished){
    //Serial.print(digitalRead(13));
    for (int i = 0; i < ITERATIONS; i++){
      digitalWrite(PUMP_PIN, LOW);
      delay(UNDERWATER_TIME_MS);
      digitalWrite(PUMP_PIN, HIGH);
      delay(ABOVE_TIME_MS);
    }
    //finished = true;
  }
}
