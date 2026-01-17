#ifndef MOTORS_H
#define MOTORS_H

void setupMotors();
void moveForward();
void stopMotors();
void moveBackward();
void turnLeft();
void turnRight();
// Add other movements as necessary (turnLeft, turnRight, etc.)
// For this demo, random movement logic will be in main

bool isMoving();

#endif
