from machine import Pin
from utime import sleep
from machine import UART
from machine import I2S
from machine import Timer  # Ensure Timer is imported correctly
import ustruct
from io import BoardDef


# https://github.com/raspberrypi/pico-micropython-examples

pin = Pin("LED", Pin.OUT)
led_yellow = Pin(7, Pin.OUT)
led_red = Pin(6, Pin.OUT)

led_red.off()
led_yellow.off()
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


led_states = {
    'red': {'pin': led_red, 'timeout': 0},
    'yellow': {'pin': led_yellow, 'timeout': 0}
}


alarm_data = {'From':'X01', 'Severity':0, 'Label':'xxxx', 'Duration':0}
alarm_severity_duration = {
    0: 0,      # No alarm
    1: 5,      # 5 seconds
    2: 10,     # 10 seconds
    3: 15,     # 15 seconds
    4: 20,     # 20 seconds
    5: 30,     # 30 seconds
    6: 45,     # 45 seconds
    7: 60,     # 1 minute
    8: 120,    # 2 minutes
    9: 180     # 3 minutes
}


# Function to be called every 100 ms
def led_task(timer):
    for led in led_states.values():
        if led['timeout'] > 0:
            led['pin'].on()
            led['timeout'] -= 1
            if led['timeout'] == 0:
                led['pin'].off()
   

# Create a hardware timer
tim = Timer()  # Timer ID (0, 1, etc. depends on board)
tim.init(period=100, mode=Timer.PERIODIC, callback=led_task)


# ==== USER CONFIGURATION ====
WAV_FILE = "test.wav"  # Must be 16-bit PCM WAV
SCK_PIN = 10           # Serial Clock
WS_PIN = 11            # Word Select (LRCLK)
SD_PIN = 12             # Serial Data
BUFFER_SIZE = 2048     # Bytes per buffer
# ============================


def play_tone(frequency, duration_ms, volume=32767):
    """Play a tone using I2S interface"""
    
    sample_rate = 44100
    samples = int(sample_rate * duration_ms / 1000)
    
    audio = I2S(1, sck=Pin(SCK_PIN), ws=Pin(WS_PIN), sd=Pin(SD_PIN), mode=I2S.TX, bits=16, format=I2S.STEREO, rate=sample_rate, ibuf=20000)
    buf = bytearray(samples * 4)
    for i in range(samples):
        sample = int(volume * __import__('math').sin(2 * __import__('math').pi * frequency * i / sample_rate))

        buf[i*4:i*4+2] = sample.to_bytes(2, 'little')
        buf[i*4+2:i*4+4] = sample.to_bytes(2, 'little')   
    audio.write(buf)
    audio.deinit()
    """
    """
    print("play tone done")

def decode_alarm_messages(data):
    # Placeholder for decoding logic
    data = data.strip().lstrip('<').rstrip('>')
    data = data.split(';')
    if data[0] == 'ALARM':
        alarm_data['From'] = data[1]
        alarm_data['Severity'] = int(data[2])
        alarm_data['Label'] = data[3]   
        alarm_data['Duration'] = alarm_severity_duration.get(alarm_data['Severity'], 0) 
        led_states['yellow']['timeout'] =10
        play_tone(440, 100, 20000)
    else:
        led_states['red']['timeout'] = 20
    print(alarm_data)



play_tone(220, 100)

while True:
    if uart.any():
        data = uart.read()
        if data is not None:
            data = data.decode('utf-8')  
            print(data)
            decode_alarm_messages(data) 
    try:
        pin.toggle()
        # led_yellow.toggle()
        # led_red.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break

pin.off()
tim.deinit()
print("Finished.")

