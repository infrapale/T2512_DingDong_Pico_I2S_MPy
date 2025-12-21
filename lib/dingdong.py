import os
import struct
import _thread
import time
from machine import Pin, I2S
import board_def as BD  

# dingdong.py
#
# DingDong - simple WAV player for Pico MicroPython using I2S and SD card
# - Streams PCM WAV files from a mounted SD card path
# - Parses WAV header (PCM only) and converts 8-bit/mono to 16-bit stereo as needed
#
# Usage:
#   from dingdong import DingDong
#   dd = DingDong(sck_pin=18, ws_pin=19, sd_mount="/sd")          # adjust pins
#   dd.play("/sd/doorbell.wav", background=True)
#   dd.stop()


("I2S not available in this build")

class DingDong:
    def __init__(self, sd, pin_sck, pin_ws, pin_sd, i2s_id=0, bits=16,rate=44100, buffer_frames=1024):
        """
        sck_pin, ws_pin: integer pin numbers for I2S SCK and WS (LRCLK)
        sd_mount: filesystem mount point where WAV files are stored
        i2s_id: first arg used to construct I2S (depends on implementation)
        bits: output bit depth (usually 16)
        buffer_frames: internal frames per buffer (tune for performance)
        """

        #self.vfs = vfs
        self.sd = sd
        self.bits = bits
        self._playing = False
        self._stop = False
        #self._thread = None
        #self._lock = _thread.allocate_lock()
        # Create I2S TX object. Signature may differ across builds; try common forms.
        try:
            self.i2s = I2S(i2s_id, sck=pin_sck, ws=pin_ws, sd=pin_sd, mode=I2S.TX, bits=bits, format=I2S.STEREO, rate=rate, ibuf=40000)
        except TypeError:
            # alternative constructor
            self.i2s = I2S(id=i2s_id, sck=pin_sck, ws=pin_ws, sd=pin_sd, mode=I2S.TX, bits=bits, format=I2S.STEREO, rate=rate, ibuf=40000)
        except Exception as e:
            raise

        self._buffer_frames = buffer_frames

    def play(self, filename):
        still_data = True
        try:
            wav_file = self.sd.fopen(filename,mode='rb')
            self.sd.fseek(44,0)    
            while still_data:
                data = self.sd.fread(4096)   
                if not data:
                        still_data = False
                else:
                    self.i2s.write(data)
        except Exception as e:
            print("Error:", e)  

 
