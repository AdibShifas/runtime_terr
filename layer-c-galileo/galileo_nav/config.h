#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// --- Serial Configuration ---
#define SERIAL_BAUD_RATE 9600
// Intel Galileo usually uses Serial1 for the UART header (Pins 0/1)
// Adjust if using software serial or USB-serial
#define ESP_SERIAL Serial1 

// --- Motor Pins (Example L298N or similar) ---
#define PIN_MOTOR_LEFT_FWD   5
#define PIN_MOTOR_LEFT_BCK   6
#define PIN_MOTOR_RIGHT_FWD  9
#define PIN_MOTOR_RIGHT_BCK  10

// --- Sensor Pins ---
#define PIN_ULTRASONIC_TRIG  2
#define PIN_ULTRASONIC_ECHO  3
#define PIN_BUMP_LEFT        4
#define PIN_BUMP_RIGHT       7
#define PIN_RESET_BUTTON     8

// --- Thresholds ---
#define COLLISION_DIST_CM    15
#define IDLE_TIMEOUT_MS      10000

#endif // CONFIG_H
