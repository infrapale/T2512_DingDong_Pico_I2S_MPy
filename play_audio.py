import sys
import machine
from machine import SPI, I2S, Pin
import sdcard
import os
import io

#https://github.com/micropython/micropython
#https://randomnerdtutorials.com/raspberry-pi-pico-microsd-card-micropython/



# Define SPI pins
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))
cs = machine.Pin(17, machine.Pin.OUT)

# Initialize SD card over SPI
sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# List directory
print(os.listdir("/sd"))

while False:
    pass        




# List SD card directory
print("SD Card contents:")
for file in os.listdir('/sd'):
    print(file)

SCK_PIN = 10           # Serial Clock
WS_PIN = 11            # Word Select (LRCLK)
SD_PIN = 12             # Serial Data


audio_i2s = I2S(
    1,
    sck=SCK_PIN,
    ws=WS_PIN,
    sd=SD_PIN,
    mode=I2S.TX,
    bits=16,
    format=I2S.STEREO,
    rate=16000,
    ibuf=40000,
)

# Play beep.wav
with open('/sd/cat-time.wav', 'rb') as wav_file:
    # Skip WAV header (44 bytes)
    wav_file.seek(44)
    
    # Read and play audio data
    while True:
        data = wav_file.read(4096)
        if not data:
            break
        audio_i2s.write(data)

audio_i2s.deinit()
print("Playback complete")