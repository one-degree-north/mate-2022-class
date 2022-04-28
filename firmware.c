#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"
#include "hardware/pwm.h"
#include "hardware/uart.h"
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include <stdio.h>
#include "bno055.h"

// convenience things...
#ifndef INT_SHORTHAND
#define u8 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t
#define i8 int8_t
#define i16 int16_t
#define i32 int32_t
#define i64 int64_t
#endif

#ifndef MIN
#define MIN(a, b)       (((a) < (b)) ? (a) : (b))
#endif

#ifndef MAX
#define MAX(a, b)       (((a) > (b)) ? (a) : (b))
#endif

#ifndef ABS
#define ABS(a)          ((a) < 0 ? -(a) : (a))
#endif

// define GPIO pins
#define THRUSTER_ONE 9
#define THRUSTER_TWO 8
#define THRUSTER_THREE 7
#define THRUSTER_FOUR 6
#define THRUSTER_FIVE 3
#define THRUSTER_SIX 2

#define MAX_DELTA_POS 2000 // delta us per second

#define SERVO 28

// servo configuration
#define SERVO_MIN 1000
#define SERVO_MID 1500
#define SERVO_MAX 2000

// joystick & buttons
#define AXIS_X 26
#define AXIS_Y 27
#define JOYSTICK_PRESS


/*** SECTION: UTILITIES ***/

bool assertRange(i32 value, i32 min, i32 max) {
    return min <= value && value <= max;
}

/*** SECTION: THRUSTERS AND SERVOS ***/

u16 thrusterPos[6];
u16 targetThrusterPos[6];
u64 prevThrusterLoopMicroseconds;
u16 servoPos;

void initOneShot125(uint pin) {
    // initialize the pin
    gpio_init(pin);
    gpio_set_function(pin, GPIO_FUNC_PWM);
    u8 slice = pwm_gpio_to_slice_num(pin);
    u8 channel = pwm_gpio_to_channel(pin);

    // configure PWM
    pwm_set_phase_correct(slice, false);
    pwm_config config = pwm_get_default_config();

    // OneShot125 will run where 1000-2000 map to 125us-250us
    // 96MHz core divided by 12 results in 8MHz, divided by 3999+1 results in 2kHz
    // loop 1000/4000 * 500us = 125us 1500/4000 * 500us = 192us 2000/4000 * 500us
    // = 250us
    pwm_config_set_clkdiv_int(&config, 12);
    pwm_init(slice, &config, true);
    pwm_set_wrap(slice, 3999);
    pwm_set_chan_level(slice, channel, 1500);
}

void initServo(uint pin) {
    // check if pin is on PWM slice 4 or 6, aka GPIO 24,25,28,29
    if (pin != 24 && pin != 25 && pin != 28 && pin != 29) {
        printf("[initServo] ERROR: invalid GPIO pin for PWM init Servo");
        return;
    }

    // initialize the pin
    gpio_init(pin);
    gpio_set_function(pin, GPIO_FUNC_PWM);
    u8 slice = pwm_gpio_to_slice_num(pin);
    u8 channel = pwm_gpio_to_channel(pin);

    // configure PWM
    pwm_set_phase_correct(slice, false);
    pwm_config config = pwm_get_default_config();

    // OneShot125 will run where 1000-2000 map to 125us-250us
    // 96MHz core divided by 96 results in 1MHz, divided by 19999+1 results in
    // 50Hz loop 1000/20000 * 20000us = 1000us 1500/20000 * 20000us = 1500us
    // 2000/20000 * 20000us = 2000us
    pwm_config_set_clkdiv_int(&config, 96);
    pwm_init(slice, &config, true);
    pwm_set_wrap(slice, 19999);
    pwm_set_chan_level(slice, channel, 1500);
}

void setServo(uint servo, uint level) {
    // level: [1000, 2000]
    if (!assertRange(level, 1000, 2000))
        return;

    u8 slice = pwm_gpio_to_slice_num(SERVO);
    u8 channel = pwm_gpio_to_channel(SERVO);

    pwm_set_chan_level(slice, channel, level);
}

void runThruster(uint thruster, uint level) {
    // level: [1000, 2000]
    if (!assertRange(level, 1000, 2000))
        return;

    u8 slice = pwm_gpio_to_slice_num(thrusterPins[thruster]);
    u8 channel = pwm_gpio_to_channel(thrusterPins[thruster]);

    pwm_set_chan_level(slice, channel, level);
}

void setThrusterTarget(uint thruster, uint level) {
    targetThrusterPos[thruster] = level;
}

void setThruster(uint thruster, uint level) {
    thrusterPos[thruster] = level;
}

void setupOutputs() {
    for (int i = 0; i < numThrusters; ++i) {
        initOneShot125(thrusterPins[i]);
        thrusterPos[i] = 1500;
        targetThrusterPos[i] = 1500;
    }
    servoPos = 1500;

    prevThrusterLoopMicroseconds = to_us_since_boot(get_absolute_time());
}

void loopOutputs() {
    u64 now = to_us_since_boot(get_absolute_time());
    u64 elapsed_us = prevThrusterLoopMicroseconds - now;

    // set each output to current value
    for (int i = 0; i < numThrusters; ++i) {
        runThruster(i, thrusterPos[i]);
    }
    // lerp each output to new value (closer to target)
    for (int i = 0; i < numThrusters; ++i) {
        u16 targetDelta = ABS(targetThrusterPos[i] - thrusterPos[i]);
        i8 sign = targetThrusterPos[i] - thrusterPos[i] > 0 ? 1 : -1;
        u16 maxDelta = MIN(MAX_DELTA_POS * elapsed_us / 1000000, 0xFFFF);

        i16 movement = MIN(targetDelta, maxDelta) * sign;
        thrusterPos[i] += movement;
    }

    setServo(servoPos);
}

/*** SECTION: ANALOG INPUTS ***/

void initJoystick() {
    adc_init();
    adc_gpio_init(AXIS_X);
    adc_gpio_init(AXIS_Y);
    gpio_init(JOYSTICK_PRESS);

}

/*** SECTION: MAIN ***/

void halt() {
    for (int i = 0; i < numThrusters; ++i) {
        targetThrusterPos[i] = 1500;
        thrusterPos[i] = 1500;
    }
    loopOutputs();
}


void setup() {
    // before we do ANYTHING, set the system clock to 96MHz
    set_sys_clock_khz(96000, false);
    setupOutputs();

}

void loop() {
    loopOutputs();
}

int main() {

    setup();

    while (true) {
        loop();
    }

    return 0;
}
