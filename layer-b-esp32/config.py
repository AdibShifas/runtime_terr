# config.py - ESP32 Pin Configuration for Sheldon Rover
# Layer B: ESP32 Engine Configuration

# =============================================================================
# UART Configuration (Receiving events from Intel Galileo)
# =============================================================================
UART_ID = 2              # UART2 on ESP32
UART_BAUDRATE = 9600     # Match with Galileo
UART_TX_PIN = 17         # GPIO17 (TX2) - not used for receiving, but defined
UART_RX_PIN = 16         # GPIO16 (RX2) - receives events from Galileo

# =============================================================================
# Intensity Switch Configuration (3-position switch)
# =============================================================================
# Using 2 GPIO pins to read 3 states: LOW, MID, HIGH
# Switch wiring:
#   LOW:  PIN_LOW = HIGH, PIN_HIGH = LOW
#   MID:  PIN_LOW = LOW,  PIN_HIGH = LOW  (both off = middle)
#   HIGH: PIN_LOW = LOW,  PIN_HIGH = HIGH
SWITCH_PIN_LOW = 25      # GPIO25 - pulled HIGH when switch is in LOW position
SWITCH_PIN_HIGH = 26     # GPIO26 - pulled HIGH when switch is in HIGH position

# =============================================================================
# Audio Configuration
# =============================================================================
# Option 1: DFPlayer Mini (recommended for loud, clear audio)
DFPLAYER_TX_PIN = 18     # GPIO18 - TX to DFPlayer RX
DFPLAYER_RX_PIN = 19     # GPIO19 - RX from DFPlayer TX

# Option 2: I2S DAC (MAX98357A)
I2S_BCK_PIN = 27         # Bit clock
I2S_WS_PIN = 14          # Word select (LRCLK)
I2S_DATA_PIN = 12        # Data out

# Option 3: PWM Audio (no extra hardware, low quality)
PWM_AUDIO_PIN = 25       # DAC output pin

# =============================================================================
# Timing Configuration
# =============================================================================
MIN_SPEECH_GAP_MS = 2000  # Minimum gap between spoken lines (milliseconds)
LOOP_DELAY_MS = 50        # Main loop delay

# =============================================================================
# Debug Mode
# =============================================================================
DEBUG = True              # Print debug messages to console
