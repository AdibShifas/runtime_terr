#include "sensors.h"
#include "config.h"
#include <Arduino.h>

void setupSensors() {
    pinMode(PIN_ULTRASONIC_TRIG, OUTPUT);
    pinMode(PIN_ULTRASONIC_ECHO, INPUT);
    pinMode(PIN_BUMP_LEFT, INPUT_PULLUP);
    pinMode(PIN_BUMP_RIGHT, INPUT_PULLUP);
    pinMode(PIN_RESET_BUTTON, INPUT_PULLUP);
}

long readUltrasonicDistance() {
    digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(PIN_ULTRASONIC_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
    
    // Timeout of 30ms (approx 5m)
    long duration = pulseIn(PIN_ULTRASONIC_ECHO, HIGH, 30000); 
    if (duration == 0) return 999; // No echo -> far away
    
    // Speed of sound 340 m/s -> 0.034 cm/us. Divide by 2 (round trip).
    return (duration * 0.034 / 2);
}

bool checkCollision() {
    // 0. Simulation / Debug via Serial
    if (Serial.available()) {
        char c = Serial.read();
        if (c == 'c' || c == 'C') return true; // Type 'c' to simulate collision
    }

    // 1. Check Bump Switches (Active LOW usually)
    if (digitalRead(PIN_BUMP_LEFT) == LOW) return true;
    if (digitalRead(PIN_BUMP_RIGHT) == LOW) return true;

    // 2. Check Ultrasonic
    long distance = readUltrasonicDistance();
    if (distance < COLLISION_DIST_CM && distance > 0) {
        return true;
    }

    return false;
}

bool checkStuck() {
    // Requires encoders or current sensing to be accurate.
    // For this prototype, we will return false unless explicitly implemented.
    // Or we can simulate random stuck events if enabled for testing.
    return false; 
}

bool checkReset() {
    return (digitalRead(PIN_RESET_BUTTON) == LOW);
}
