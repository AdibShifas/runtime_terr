#include "serial_events.h"
#include "config.h"

void setupSerialEvents() {
    ESP_SERIAL.begin(SERIAL_BAUD_RATE);
    // Wait for serial to settle if necessary (Galileo can be slow)
    delay(100);
}

void sendEvent(const char* eventName) {
    if (eventName != NULL) {
        ESP_SERIAL.println(eventName);
        // Debug output to main USB serial as well
        Serial.print("DEBUG SENT: ");
        Serial.println(eventName);
    }
}
