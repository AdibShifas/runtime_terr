#ifndef SERIAL_EVENTS_H
#define SERIAL_EVENTS_H

#include <Arduino.h>

void setupSerialEvents();
void sendEvent(const char* eventName);

#endif
