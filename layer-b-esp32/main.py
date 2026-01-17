# main.py - Sheldon Rover Main Loop (Layer B: ESP32 Engine)
# Receives events from Intel Galileo, processes through character engine, plays audio

import time
from config import LOOP_DELAY_MS, DEBUG
from character_engine import CharacterEngine
from serial_receiver import SerialReceiver
from switch_reader import SwitchReader
from audio_player import create_audio_player


def main():
    """Main entry point for the Sheldon Rover ESP32 engine."""
    
    print("=" * 50)
    print("  🤖 Sheldon Rover - Layer B: ESP32 Engine")
    print("=" * 50)
    
    # Initialize components
    engine = CharacterEngine()
    serial = SerialReceiver()
    switch = SwitchReader()
    
    # Choose audio backend: "print" for testing, "dfplayer" for real hardware
    audio = create_audio_player("print")  # Change to "dfplayer" when ready
    
    # Set initial intensity from switch
    initial_level = switch.read_level()
    engine.set_intensity(initial_level)
    
    print(f"[MAIN] Initial intensity: {initial_level}")
    print("[MAIN] Waiting for events from Galileo...")
    print("-" * 50)
    
    # Boot announcement
    boot_line = engine.on_event("BOOT")
    if boot_line:
        audio.speak(boot_line, event="BOOT", tier=engine.intensity)
    
    # Main loop
    while True:
        try:
            # 1. Check for switch changes
            new_level = switch.read_if_changed()
            if new_level is not None:
                engine.set_intensity(new_level)
                # Optionally announce mode switch
                mode_line = engine.on_event("MODE_SWITCH")
                if mode_line:
                    audio.speak(mode_line, event="MODE_SWITCH", tier=engine.intensity)
            
            # 2. Check for events from Galileo
            event = serial.read_event()
            if event:
                line = engine.on_event(event)
                if line:
                    audio.speak(line, event=event, tier=engine.intensity)
            
            # 3. Small delay to prevent busy-waiting
            time.sleep_ms(LOOP_DELAY_MS)
            
        except KeyboardInterrupt:
            print("\n[MAIN] Shutting down...")
            break
        except Exception as e:
            print(f"[MAIN] Error: {e}")
            time.sleep_ms(1000)  # Wait before retrying


# Auto-run when module is executed
if __name__ == "__main__":
    main()
