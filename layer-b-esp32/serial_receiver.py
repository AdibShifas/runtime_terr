# serial_receiver.py - UART Receiver for Intel Galileo Events
# Reads events from Galileo via UART and returns them as strings

from machine import UART, Pin
from config import UART_ID, UART_BAUDRATE, UART_TX_PIN, UART_RX_PIN, DEBUG


class SerialReceiver:
    def __init__(self):
        """Initialize UART connection to Intel Galileo."""
        self.uart = UART(
            UART_ID,
            baudrate=UART_BAUDRATE,
            tx=Pin(UART_TX_PIN),
            rx=Pin(UART_RX_PIN)
        )
        self.buffer = ""
        
        if DEBUG:
            print(f"[SERIAL] Initialized UART{UART_ID} at {UART_BAUDRATE} baud")
            print(f"[SERIAL] RX pin: GPIO{UART_RX_PIN}, TX pin: GPIO{UART_TX_PIN}")

    def read_event(self) -> str:
        """
        Non-blocking read of a single event from the UART buffer.
        
        Events are expected as line-terminated strings (e.g., "COLLISION\n").
        
        Returns:
            Event string (without newline) if complete event received, else None.
        """
        # Check if data available
        if self.uart.any():
            # Read available bytes
            data = self.uart.read()
            if data:
                try:
                    self.buffer += data.decode('utf-8')
                except UnicodeDecodeError:
                    if DEBUG:
                        print("[SERIAL] Unicode decode error, clearing buffer")
                    self.buffer = ""
                    return None
        
        # Check for complete line (event)
        if '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            event = line.strip().upper()
            
            if event:
                if DEBUG:
                    print(f"[SERIAL] Received event: {event}")
                return event
        
        return None

    def flush(self):
        """Clear the receive buffer."""
        self.buffer = ""
        while self.uart.any():
            self.uart.read()
        
        if DEBUG:
            print("[SERIAL] Buffer flushed")
