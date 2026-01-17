# Layer B: ESP32 Engine (MicroPython)

Sheldon character engine for ESP32, receiving events from Intel Galileo and outputting speech.

## Files

| File | Purpose |
|------|---------|
| `config.py` | Pin definitions, baud rates, timing |
| `main.py` | Main entry point and event loop |
| `character_engine.py` | State machine (irritation, intensity, line selection) |
| `lines_sheldon.py` | Sheldon-style voice lines |
| `serial_receiver.py` | UART listener for Galileo events |
| `switch_reader.py` | 3-position intensity switch reader |
| `audio_player.py` | Pluggable audio output (print/DFPlayer) |

## Wiring

### UART (Galileo → ESP32)
```
Galileo TX  →  ESP32 GPIO16 (RX2)
Galileo GND →  ESP32 GND
```

### Intensity Switch
```
Switch LOW  →  ESP32 GPIO25
Switch HIGH →  ESP32 GPIO26
Switch COM  →  3.3V
```

### DFPlayer Mini (Optional)
```
DFPlayer RX →  ESP32 GPIO18
DFPlayer TX →  ESP32 GPIO19
DFPlayer VCC → 5V
DFPlayer GND → GND
Speaker     → DFPlayer SPK+/SPK-
```

## Upload to ESP32

1. Install MicroPython on ESP32
2. Upload all `.py` files to ESP32 root
3. Reset ESP32 - `main.py` runs automatically

## Testing Without Hardware

Run `test_engine.py` on your laptop (regular Python) to test character logic:

```bash
python test_engine.py
```

## Events Supported

| Event | Effect |
|-------|--------|
| `BOOT` | Startup announcement |
| `COLLISION` | +1 irritation, speaks |
| `STUCK` | +1 irritation, speaks |
| `RESET` | Reset irritation to 0 |
| `MOVE_START` | Movement start line |
| `MOVE_STOP` | Movement stop line |
| `MODE_SWITCH` | When intensity switch changes |
