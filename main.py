from machine import Pin
from utime import sleep
from machine import UART
from machine import I2S
from machine import Timer  # Ensure Timer is imported correctly
import sdcard
import sys
import os
import ustruct
import board_def as BD
from lib.dingdong import DingDong
from mysd import MySD

sd = MySD(BD.SD_CLK, BD.SD_MOSI, BD.SD_MISO, BD.SD_CS)
sd.mount()  
sd.print_directory()

# sys.exit()


ding_dong = DingDong(sd,
                     pin_sck=BD.I2S_SCK,        # Serial Clock  
                     pin_ws=BD.I2S_WS,          # Word Select (LRCLK)
                     pin_sd =BD.I2S_SD,          # Serial Data
                     i2s_id=0,
                     rate=16000,
                     buffer_frames=2048)        # Bytes per buffer

# https://github.com/raspberrypi/pico-micropython-examples



led_yellow = Pin(BD.LED_YELLOW, Pin.OUT)
led_red = Pin(BD.LED_RED, Pin.OUT)

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
        if alarm_data['Severity'] > 0:  
            ding_dong.play('/sd/truck_horn.wav')
    else:
        led_states['red']['timeout'] = 20
    print(alarm_data)



ding_dong.play('/sd/chime_big_ben_2b.wav')

while True:
    if uart.any():
        data = uart.read()
        if data is not None:
            data = data.decode('utf-8')  
            print(data)
            decode_alarm_messages(data) 
    try:
        #pin.toggle()
        # led_yellow.toggle()
        # led_red.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break


tim.deinit()
print("Finished.")

