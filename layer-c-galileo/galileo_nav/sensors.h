#ifndef SENSORS_H
#define SENSORS_H

// Initialize sensor pins
void setupSensors();

// Returns true if a collision is detected (bump or ultrasonic)
bool checkCollision();

// Returns true if wheels are spinning but not moving (stuck)
// (Mocked for now or needs encoders)
bool checkStuck();

// Returns true if reset button is pressed
bool checkReset();

#endif
