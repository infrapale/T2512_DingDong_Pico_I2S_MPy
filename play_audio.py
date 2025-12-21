import sys
import machine
from machine import SPI, I2S, Pin
import sdcard
import os
import io
import board_def as BD
from mysd import MySD

#https://github.com/micropython/micropython
#https://randomnerdtutorials.com/raspberry-pi-pico-microsd-card-micropython/

sd = MySD(BD.SD_CLK, BD.SD_MOSI, BD.SD_MISO, BD.SD_CS)
sd.mount()  
sd.print_directory()


'''
# Define SPI pins
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  sck=machine.Pin(BD.SD_CLK),
                  mosi=machine.Pin(BD.SD_MOSI),
                  miso=machine.Pin(BD.SD_MISO))
cs = machine.Pin(BD.SD_CS, machine.Pin.OUT)

# Initialize SD card over SPI
sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# List directory
print(os.listdir("/sd"))
'''

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
    sck =BD.I2S_SCK,
    ws = BD.I2S_WS,
    sd = BD.I2S_SD,
    mode=I2S.TX,
    bits=16,
    format=I2S.STEREO,
    rate=16000,
    ibuf=40000,
)

sd.dummy()
still_data = True
try:
    wav_file = sd.fopen('/sd/cat-time.wav',mode='rb')
    sd.fseek(44,0)    
    while still_data:
        data = sd.fread(4096)   
        if not data:
                still_data = False
        else:
            audio_i2s.write(data)

except Exception as e:
    print("Error:", e)

    '''# Skip WAV header (44 bytes)
    # Skip WAV header (44 bytes)
    #wav_file.seek(44)
    sdfile_seek(wav_file,44)    
    # Read and play audio data
    while True:
        #data = wav_file.read(4096)
        data = sdfile_read(wav_file,4096)   
        if not data:
            break
        audio_i2s.write(data)
'''
while(True):
    pass    


# Play beep.wav
with open('/sd/cat-time.wav', 'rb') as wav_file:
    # Skip WAV header (44 bytes)
    #wav_file.seek(44)
    sdfile_seek(wav_file,44)    
    # Read and play audio data
    while True:
        #data = wav_file.read(4096)
        data = sdfile_read(wav_file,4096)   
        if not data:
            break
        audio_i2s.write(data)

audio_i2s.deinit()
print("Playback complete")