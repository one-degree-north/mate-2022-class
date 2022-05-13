#include <Servo.h>

#define THRUSTER_LEFT       11
#define THRUSTER_RIGHT      5
#define THRUSTER_FRONT_LEFT    6
#define THRUSTER_FRONT_RIGHT   9
#define THRUSTER_BACK_LEFT  3
#define THRUSTER_BACK_RIGHT 10
#define SERVO_CLAW          8
#define JOYSTICK_LEFT_X     A5
#define JOYSTICK_LEFT_Y     A4
#define JOYSTICK_RIGHT_X    A3
#define JOYSTICK_RIGHT_Y    A2
#define TRIGGER_LEFT        A1
#define TRIGGER_RIGHT       A0
#define CLAW_POTENTIOMETER  A6
#define Z_POTENTIOMETER     A7

#define RESET_BUTTON        2

#define DEBUG_ENABLED

#ifdef DEBUG_ENABLED
    #define DEBUG if(1)
#else
    #define DEBUG if(0)
#endif

// define containers
typedef struct Joystick {
    uint8_t pin_x;
    uint8_t pin_y;
    int16_t x;
    int16_t y;
    int16_t default_x;
    int16_t default_y;
} joystick_t;

typedef struct Trigger {
    uint8_t pin;
    int16_t default_value;
    int16_t value;
} trigger_t;

typedef struct Output {
    Servo servo;
    uint8_t pin;
    int16_t min;
    int16_t max;
} output_t;

void printJoystick (joystick_t* joy) {
    Serial.print("js pin_x=");
    Serial.print(joy->pin_x);
    Serial.print(" pin_y=");
    Serial.print(joy->pin_y);
    Serial.print(" x=");
    Serial.print(joy->x);
    Serial.print(" y=");
    Serial.print(joy->y);
    Serial.print(" def_x=");
    Serial.print(joy->default_x);
    Serial.print(" def_y=");
    Serial.println(joy->default_y);
}

void printTrigger (trigger_t* trig) {
    Serial.print("trig pin=");
    Serial.print(trig->pin);
    Serial.print(" val=");
    Serial.print(trig->value);
    Serial.print(" def_value=");
    Serial.println(trig->default_value);
}

// create containers for our setup
joystick_t leftJoystick = {JOYSTICK_LEFT_X, JOYSTICK_LEFT_Y, 0, 0, 0, 0};
joystick_t rightJoystick = {JOYSTICK_RIGHT_X, JOYSTICK_RIGHT_Y, 0, 0, 0, 0};

trigger_t leftTrigger = {TRIGGER_LEFT, 0, 0};
trigger_t rightTrigger = {TRIGGER_RIGHT, 0, 0};
trigger_t clawPot = {CLAW_POTENTIOMETER, 0, 0};
trigger_t zPot = {Z_POTENTIOMETER, 0, 0};

output_t leftThruster = {Servo(), THRUSTER_LEFT, 1000, 2000};
output_t rightThruster = {Servo(), THRUSTER_RIGHT, 1000, 2000};
output_t frontLeftThruster = {Servo(), THRUSTER_FRONT_LEFT, 2000, 1000};
output_t frontRightThruster = {Servo(), THRUSTER_FRONT_RIGHT, 1000, 2000};
output_t backLeftThruster = {Servo(), THRUSTER_BACK_LEFT, 1000, 2000};
output_t backRightThruster = {Servo(), THRUSTER_BACK_RIGHT, 1000, 2000};
output_t clawServo = {Servo(), SERVO_CLAW, 1200, 1600};

/*** SECTION: CONFIGURATION ***/
void configureOutput(output_t* out) {
    out->servo.attach(out->pin);
    out->servo.writeMicroseconds(1500);
}

void configureJoystick(joystick_t* joy) {
    pinMode(joy->pin_x, INPUT);
    pinMode(joy->pin_y, INPUT);
    delay(1);
    joy->default_x = analogRead(joy->pin_x);
    joy->default_y = analogRead(joy->pin_y);
}

void configureTrigger(trigger_t* trig) {
    pinMode(trig->pin, INPUT);
    delay(1);
    trig->default_value = analogRead(trig->pin);
}

void configureReset() {
  pinMode(RESET_BUTTON, INPUT_PULLUP);
  delay(1);
}

/*** SECTION: LOOP I/O ***/

void updateJoystick(joystick_t* joy) {
    joy->x = analogRead(joy->pin_x) - joy->default_x;
    joy->y = analogRead(joy->pin_y) - joy->default_y;
}

void updateTrigger(trigger_t* trig) {
    trig->value = analogRead(trig->pin) - trig->default_value;
}

void updateReset() {
    if (digitalRead(RESET_BUTTON) == LOW) {
        configureJoystick(&leftJoystick);
        configureJoystick(&rightJoystick);
    
        configureTrigger(&leftTrigger);
        configureTrigger(&rightTrigger);

        Serial.println("RESET BUTTON!");

        delay(100);
    }
}

void writeOutput(output_t* out, int8_t percent) {
    if (percent > 100) percent = 100;
    if (percent < -100) percent = -100;
    if (percent > -12 && percent < 12) percent = 0;
    int16_t micros = map(percent, -100, 100, out->min, out->max);
    out->servo.writeMicroseconds(micros);

    DEBUG Serial.print("output ");
    DEBUG Serial.print(out->pin);
    DEBUG Serial.print(" set to ");
    DEBUG Serial.println(micros);
}

/*** SECTION: INSTRUCTIONS ***/

void moveX(int8_t percent) {
    writeOutput(&leftThruster, percent);
    writeOutput(&rightThruster, percent);
}

void yaw(int8_t percent) {
    writeOutput(&leftThruster, percent);
    writeOutput(&rightThruster, percent);
}

void xYaw(int8_t percent_x, int8_t percent_yaw) {
    writeOutput(&leftThruster, -(percent_x + percent_yaw));
    writeOutput(&rightThruster, (percent_x - percent_yaw));
}

void moveZ(int8_t percent) {
    writeOutput(&frontLeftThruster, percent);
    writeOutput(&frontRightThruster, percent);
    writeOutput(&backLeftThruster, percent);
    writeOutput(&backRightThruster, percent);
}

void pitch(int8_t percent) {
    writeOutput(&frontLeftThruster, percent);
    writeOutput(&frontRightThruster, percent);
    writeOutput(&backLeftThruster, -percent);
    writeOutput(&backRightThruster, -percent);
}

void roll(int8_t percent) {
    writeOutput(&frontLeftThruster, percent);
    writeOutput(&frontRightThruster, -percent);
    writeOutput(&backLeftThruster, percent);
    writeOutput(&backRightThruster, -percent);
}

void zPitchRoll(int8_t percent_up, int8_t percent_pitch, int8_t percent_roll) {
    writeOutput(&frontLeftThruster, (percent_up + percent_pitch + percent_roll));
    writeOutput(&frontRightThruster, (percent_up + percent_pitch - percent_roll));
    writeOutput(&backLeftThruster, (percent_up - percent_pitch + percent_roll));
    writeOutput(&backRightThruster, (percent_up - percent_pitch - percent_roll));
}

void clawMove(int8_t percent) {
    writeOutput(&clawServo, percent);
}

/*** SECTION: ARDUINO ***/

void setup() {
    configureJoystick(&leftJoystick);
    configureJoystick(&rightJoystick);

    configureTrigger(&leftTrigger);
    configureTrigger(&rightTrigger);
    configureTrigger(&clawPot);
    clawPot.default_value = 507;
    configureTrigger(&zPot);

    configureOutput(&leftThruster);
    configureOutput(&rightThruster);
    configureOutput(&frontLeftThruster);
    configureOutput(&frontRightThruster);
    configureOutput(&backLeftThruster);
    configureOutput(&backRightThruster);
    configureOutput(&clawServo);

    configureReset();

    DEBUG Serial.begin(115200);
    DEBUG while (!Serial) delay(1);
    DEBUG Serial.println("ready. waiting 7.5s for thruster init:");
    delay(7500);
    DEBUG Serial.println("running");
}

void loop() {
    updateReset();
    
    updateJoystick(&leftJoystick);
    updateJoystick(&rightJoystick);

    updateTrigger(&leftTrigger);
    updateTrigger(&rightTrigger);
    updateTrigger(&clawPot);

    DEBUG printJoystick(&leftJoystick);
    DEBUG printJoystick(&rightJoystick);
    DEBUG printTrigger(&leftTrigger);
    DEBUG printTrigger(&rightTrigger);
    DEBUG printTrigger(&clawPot);

    int rjy = rightJoystick.y;
    if (rjy >= 0) {
      rjy = map(rjy, -80, 80, -100, 100);
    } else {
      rjy = map(rjy, -250, 250, -100, 100);
    }

    zPitchRoll( map(zPot.value, -500, 500, 100, -100),
                rjy,
                map(rightJoystick.x, -128, 128, -25, 25));
    xYaw(map(leftJoystick.x, 300, -300, -100, 100), map(-leftJoystick.y, 300, -300, -100, 100));
    clawMove(map(clawPot.value, -500, 500, 100, -100));
    DEBUG Serial.println();

    delay(50);
}
