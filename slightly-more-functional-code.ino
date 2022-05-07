#include <Servo.h>

#define THRUSTER_LEFT       11
#define THRUSTER_RIGHT      7
#define THRUSTER_FRONT_LEFT    8
#define THRUSTER_FRONT_RIGHT   9
#define THRUSTER_BACK_LEFT  12
#define THRUSTER_BACK_RIGHT 10
#define SERVO_CLAW          6
#define JOYSTICK_LEFT_X     A4
#define JOYSTICK_LEFT_Y     A5
#define JOYSTICK_RIGHT_X    A6
#define JOYSTICK_RIGHT_Y    A7
#define TRIGGER_LEFT        A2
#define TRIGGER_RIGHT       A3

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

// create containers for our setup
joystick_t leftJoystick = {JOYSTICK_LEFT_X, JOYSTICK_LEFT_Y, 0, 0, 0, 0};
joystick_t rightJoystick = {JOYSTICK_RIGHT_X, JOYSTICK_RIGHT_Y, 0, 0, 0, 0};

trigger_t leftTrigger = {TRIGGER_LEFT, 0, 0};
trigger_t rightTrigger = {TRIGGER_RIGHT, 0, 0};

output_t leftThruster = {Servo(), THRUSTER_LEFT, 1000, 2000};
output_t rightThruster = {Servo(), THRUSTER_RIGHT, 1000, 2000};
output_t frontLeftThruster = {Servo(), THRUSTER_FRONT_LEFT, 1000, 2000};
output_t frontRightThruster = {Servo(), THRUSTER_FRONT_RIGHT, 1000, 2000};
output_t backLeftThruster = {Servo(), THRUSTER_BACK_LEFT, 1000, 2000};
output_t backRightThruster = {Servo(), THRUSTER_BACK_RIGHT, 1000, 2000};
output_t clawServo = {Servo(), SERVO_CLAW, 1000, 2000};

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

/*** SECTION: LOOP I/O ***/

void updateJoystick(joystick_t* joy) {
    joy->x = analogRead(joy->pin_x) - joy->default_x;
    joy->y = analogRead(joy->pin_y) - joy->default_y;
}

void updateTrigger(trigger_t* trig) {
    trig->value = analogRead(trig->pin) - trig->default_value;
}

void writeOutput(output_t* out, int8_t percent) {
    if (percent > 100) percent = 100;
    if (percent < -100) percent = -100;
    int16_t micros = map(percent, -100, 100, out->min, out->max);
    out->servo.writeMicroseconds(micros);
}

/*** SECTION: INSTRUCTIONS ***/

void moveX(int8_t percent) {
    writeOutput(&leftThruster, percent);
    writeOutput(&rightThruster, percent);
}

void yaw(int8_t percent) {
    writeOutput(&leftThruster, percent);
    writeOutput(&rightThruster, -percent);
}

void xYaw(int8_t percent_x, int8_t percent_yaw) {
    writeOutput(&leftThruster, (percent_x + percent_yaw));
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
    writeOutput(&frontLeftThruster, (percent_up + percent_pitch + percent_roll) / 3);
    writeOutput(&frontRightThruster, (percent_up + percent_pitch - percent_roll) / 3);
    writeOutput(&backLeftThruster, (percent_up - percent_pitch + percent_roll) / 3);
    writeOutput(&backRightThruster, (percent_up - percent_pitch - percent_roll) / 3);
}

/*** SECTION: ARDUINO ***/

void setup() {
    configureJoystick(&leftJoystick);
    configureJoystick(&rightJoystick);

    configureTrigger(&leftTrigger);
    configureTrigger(&rightTrigger);

    configureOutput(&leftThruster);
    configureOutput(&rightThruster);
    configureOutput(&frontLeftThruster);
    configureOutput(&frontRightThruster);
    configureOutput(&backLeftThruster);
    configureOutput(&backRightThruster);
    configureOutput(&clawServo);

    Serial.begin(115200);
    // while (!Serial) delay(1);
    Serial.println("ready. waiting 7.5s for thruster init:");
    delay(7500);
    Serial.println("running");
}

void loop() {
    updateJoystick(&leftJoystick);
    updateJoystick(&rightJoystick);

    updateTrigger(&leftTrigger);
    updateTrigger(&rightTrigger);

    moveZ(map(rightJoystick.y, -512, 512, -100, 100));
    xYaw(map(rightJoystick.y, -512, 512, -100, 100), map(rightJoystick.x, -512, 512, -100, 100));

    delay(20);
}
