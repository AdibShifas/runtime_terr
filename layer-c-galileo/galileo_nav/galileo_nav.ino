#include <Arduino.h>
#include "config.h"
#include "events.h"
#include "serial_events.h"
#include "motors.h"
#include "sensors.h"

unsigned long lastActivityTime = 0;
bool isStuckReported = false;

void setup() {
    Serial.begin(115200); // Debug serial
    setupSerialEvents();
    setupMotors();
    setupSensors();
    
    // Give ESP32 time to boot
    delay(2000);
    sendEvent(EVENT_BOOT);
    lastActivityTime = millis();
}

void loop() {
    unsigned long now = millis();
    
    // 1. Check Manual Reset
    if (checkReset()) {
        stopMotors();
        sendEvent(EVENT_RESET);
        // Wait for release
        while(checkReset()) delay(100);
        lastActivityTime = now;
        return; 
    }

    // 2. Navigation Logic
    bool moving = isMoving();

    if (moving) {
        // We are moving, check for bad things
        if (checkCollision()) {
            stopMotors();
            sendEvent(EVENT_COLLISION);
            
            // Recovery Maneuver
            delay(1000); // Wait a bit
            moveBackward();
            delay(1000);
            stopMotors();
            delay(500);
            turnLeft(); // Or random?
            delay(800);
            stopMotors();
            
            lastActivityTime = millis();
        }
        else if (checkStuck()) {
             if (!isStuckReported) {
                 stopMotors(); // Maybe? Or keep trying? Use STOP for safety.
                 sendEvent(EVENT_STUCK);
                 isStuckReported = true;
                 lastActivityTime = now;
             }
        }
        else {
            isStuckReported = false; // Reset flag if moving fine
        }
    } 
    else {
        // We are stopped/idle
        
        // Simple Autonomous Behavior:
        // If we've been idle for a bit, start moving again?
        // Or wait for a command? 
        // The prompt says "Move the rover around the room". 
        // Let's implement a simple "Wander" behavior: 
        // If not moving, wait 2 seconds, then start moving again.
        
        if (now - lastActivityTime > 2000 && now - lastActivityTime < IDLE_TIMEOUT_MS) {
             // Basic randomized turn could be added here before moving
             sendEvent(EVENT_MOVE_START);
             moveForward();
             // In a real robot, we might turn slightly if we just hit something
        }
        
        // Check for Idle Timeout
        if (now - lastActivityTime > IDLE_TIMEOUT_MS) {
            sendEvent(EVENT_IDLE);
            lastActivityTime = now; // Reset timer so we don't spam
        }
    }
    
    delay(50); // Small loop delay
}
