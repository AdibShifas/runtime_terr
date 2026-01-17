#include "motors.h"
#include "config.h"
#include <Arduino.h>

static bool _moving = false;

void setupMotors() {
    pinMode(PIN_MOTOR_LEFT_FWD, OUTPUT);
    pinMode(PIN_MOTOR_LEFT_BCK, OUTPUT);
    pinMode(PIN_MOTOR_RIGHT_FWD, OUTPUT);
    pinMode(PIN_MOTOR_RIGHT_BCK, OUTPUT);
    stopMotors();
}

void moveForward() {
    digitalWrite(PIN_MOTOR_LEFT_BCK, LOW);
    digitalWrite(PIN_MOTOR_RIGHT_BCK, LOW);
    analogWrite(PIN_MOTOR_LEFT_FWD, 200); // PWM speed example
    analogWrite(PIN_MOTOR_RIGHT_FWD, 200);
    _moving = true;
}

void stopMotors() {
    digitalWrite(PIN_MOTOR_LEFT_FWD, LOW);
    digitalWrite(PIN_MOTOR_LEFT_BCK, LOW);
    digitalWrite(PIN_MOTOR_RIGHT_FWD, LOW);
    digitalWrite(PIN_MOTOR_RIGHT_BCK, LOW);
    _moving = false;
}

void moveBackward() {
    digitalWrite(PIN_MOTOR_LEFT_FWD, LOW);
    digitalWrite(PIN_MOTOR_RIGHT_FWD, LOW);
    analogWrite(PIN_MOTOR_LEFT_BCK, 200);
    analogWrite(PIN_MOTOR_RIGHT_BCK, 200);
    _moving = true;
}

void turnLeft() {
    // Pivot turn: Left Back, Right Fwd
    digitalWrite(PIN_MOTOR_LEFT_FWD, LOW);
    analogWrite(PIN_MOTOR_LEFT_BCK, 200);
    digitalWrite(PIN_MOTOR_RIGHT_BCK, LOW);
    analogWrite(PIN_MOTOR_RIGHT_FWD, 200);
    _moving = true;
}

void turnRight() {
    // Pivot turn: Left Fwd, Right Back
    digitalWrite(PIN_MOTOR_LEFT_BCK, LOW);
    analogWrite(PIN_MOTOR_LEFT_FWD, 200);
    digitalWrite(PIN_MOTOR_RIGHT_FWD, LOW);
    analogWrite(PIN_MOTOR_RIGHT_BCK, 200);
    _moving = true;
}

bool isMoving() {
    return _moving;
}
