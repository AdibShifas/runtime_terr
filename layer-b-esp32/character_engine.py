# character_engine.py - Sheldon Character State Machine
# Ported from Layer A (Manya's original) to MicroPython
# Uses time.ticks_ms() instead of time.time() for ESP32 compatibility

import time
import random
from lines_sheldon import LINES
from config import MIN_SPEECH_GAP_MS, DEBUG


class CharacterEngine:
    def __init__(self):
        self.irritation = 0           # 0 upwards, increases on failures
        self.intensity = 0            # 0=LOW, 1=MID, 2=HIGH (from physical switch)
        self.last_spoke_ms = 0        # Last time we spoke (in ticks_ms)
        self.min_gap_ms = MIN_SPEECH_GAP_MS

    def on_event(self, event: str) -> str:
        """
        Processes an event and returns a spoken line or None.
        
        Args:
            event: Event string like 'COLLISION', 'STUCK', 'BOOT', etc.
            
        Returns:
            A line to speak, or None if cooldown not over or invalid event.
        """
        now = time.ticks_ms()
        
        # 1. Cooldown check (using ticks_diff for proper wraparound handling)
        if time.ticks_diff(now, self.last_spoke_ms) < self.min_gap_ms:
            if DEBUG:
                print(f"[ENGINE] Cooldown active, ignoring {event}")
            return None

        # 2. Validate event
        if event not in LINES:
            if DEBUG:
                print(f"[ENGINE] Unknown event: {event}")
            return None

        # 3. Update state based on event
        if event in ["COLLISION", "STUCK"]:
            self.irritation += 1
            if DEBUG:
                print(f"[ENGINE] Irritation increased to {self.irritation}")
        elif event == "RESET":
            self.irritation = 0
            if DEBUG:
                print("[ENGINE] Irritation reset to 0")
        
        # 4. Determine Tier
        # Base tier is intensity (from physical switch)
        # Irritation >= 3 pushes tier up by 1 (capped at 2)
        tier = self.intensity
        if self.irritation >= 3:
            tier = min(2, tier + 1)
        
        if DEBUG:
            print(f"[ENGINE] Intensity={self.intensity}, Irritation={self.irritation}, Tier={tier}")
        
        # 5. Select Line
        possible_lines = LINES[event].get(tier, LINES[event][0])
        line = random.choice(possible_lines)
        
        self.last_spoke_ms = now
        return line

    def set_intensity(self, level: int):
        """
        Sets the base intensity/pedantry level (0-2).
        Called when physical switch position changes.
        """
        old_intensity = self.intensity
        self.intensity = max(0, min(2, level))
        
        if DEBUG and old_intensity != self.intensity:
            print(f"[ENGINE] Intensity changed: {old_intensity} -> {self.intensity}")
    
    def get_state(self) -> dict:
        """Returns current engine state for debugging."""
        return {
            "irritation": self.irritation,
            "intensity": self.intensity,
            "last_spoke_ms": self.last_spoke_ms
        }
