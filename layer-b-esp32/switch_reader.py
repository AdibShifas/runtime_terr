# switch_reader.py - 3-Position Intensity Switch Reader
# Reads LOW/MID/HIGH position from physical switch via GPIO

from machine import Pin
from config import SWITCH_PIN_LOW, SWITCH_PIN_HIGH, DEBUG


class SwitchReader:
    def __init__(self):
        """
        Initialize GPIO pins for 3-position switch.
        
        Wiring:
            LOW position:  PIN_LOW = HIGH, PIN_HIGH = LOW
            MID position:  PIN_LOW = LOW,  PIN_HIGH = LOW (center/neutral)
            HIGH position: PIN_LOW = LOW,  PIN_HIGH = HIGH
        """
        # Configure pins as inputs with pull-down resistors
        self.pin_low = Pin(SWITCH_PIN_LOW, Pin.IN, Pin.PULL_DOWN)
        self.pin_high = Pin(SWITCH_PIN_HIGH, Pin.IN, Pin.PULL_DOWN)
        
        self._last_level = self.read_level()
        
        if DEBUG:
            print(f"[SWITCH] Initialized on GPIO{SWITCH_PIN_LOW} (LOW), GPIO{SWITCH_PIN_HIGH} (HIGH)")
            print(f"[SWITCH] Initial position: {self._level_name(self._last_level)}")

    def read_level(self) -> int:
        """
        Read current switch position.
        
        Returns:
            0 = LOW, 1 = MID, 2 = HIGH
        """
        low_active = self.pin_low.value()
        high_active = self.pin_high.value()
        
        if low_active and not high_active:
            return 0  # LOW
        elif not low_active and high_active:
            return 2  # HIGH
        else:
            return 1  # MID (default/center)

    def read_if_changed(self) -> int:
        """
        Read switch position only if it changed since last read.
        
        Returns:
            New level (0, 1, or 2) if changed, else None.
        """
        current_level = self.read_level()
        
        if current_level != self._last_level:
            old_level = self._last_level
            self._last_level = current_level
            
            if DEBUG:
                print(f"[SWITCH] Changed: {self._level_name(old_level)} -> {self._level_name(current_level)}")
            
            return current_level
        
        return None

    def _level_name(self, level: int) -> str:
        """Convert level number to human-readable name."""
        names = {0: "LOW", 1: "MID", 2: "HIGH"}
        return names.get(level, "UNKNOWN")
