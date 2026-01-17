# Layer C: Intel Galileo Navigation

This component runs on the Intel Galileo board and handles navigation and event detection.

## Responsibilities
1.  **Navigation**: Controls motors to move the rover.
2.  **Event Detection**: Monitors sensors for collisions, stalls, or idle states.
3.  **Communication**: Sends event strings to the ESP32 (Layer B) via Serial1.

## Event Protocol
Sent over Serial1 (9600 baud), newline terminated:
- `BOOT`: Startup
- `MOVE_START`: Movement begins
- `MOVE_STOP`: Movement ends
- `COLLISION`: Physical obstacle hit
- `STUCK`: No progress despite movement
- `IDLE_TOO_LONG`: Inactive for >10s
- `RESET`: Manual reset

## Hardware Assumptions
- **Motors**: PWM controlled DC motors on standardized pins (see `include/config.h`).
- **Sensors**: 
    - Ultrasonic rangefinder (trig/echo)
    - Bump switches (digital input)
    - Encoders (interrupt/digital input)

## Build & Run
**Use the Arduino IDE.**

1.  Open the folder `galileo_nav/`.
2.  Double-click `galileo_nav.ino`.
3.  In Arduino IDE, select **Tools > Board > Intel Galileo Gen2**.
4.  Compile and Upload.

*Note: If you don't see the board, go to Tools > Board > Boards Manager and install "Intel i586 Boards".*

## Debug / Simulation
You can open the Serial Monitor (115200 baud).
- Type `c` and hit enter to simulate a **COLLISION** event.
