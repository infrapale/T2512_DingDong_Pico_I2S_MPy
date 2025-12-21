from machine import SPI, Pin
import sdcard
import os


class MySD:
    """Wrapper for file operations on SD card"""
    def __init__(self, sck,mosi,miso,sd_cs):
        self.spi =SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  sck=Pin(sck),
                  mosi=Pin(mosi),
                  miso=Pin(miso))
        self.cs = Pin(sd_cs, Pin.OUT)
        self.sd_cs = sdcard.SDCard(self.spi, self.cs)
        self.vfs = os.VfsFat(self.sd_cs)
    

    def mount(self, mount_point="/sd"): 
        os.mount(self.vfs, "/sd")

    def unmount(self, mount_point="/sd"):
        os.umount(mount_point)  

    def print_directory(self, path="/sd"):
        print("SD Card contents:")
        for file in os.listdir(path):
            print(file)

    def dummy(self):
        print('Dummy method called ')

    def fopen(self, filepath, mode='r'):             
        self.file = open(filepath, mode)
        #self.lock = _thread.allocate_lock()
        return self.file
    
    def fseek(self, pos, whence=0):
        self.file.seek(pos, whence)

    def fread(self, n=-1):
        return self.file.read(n)    
    
    '''

    def read(self, n=-1):
        with self.lock:
            return self.file.read(n)

    def write(self, data):
        with self.lock:
            self.file.write(data)

    def seek(self, pos, whence=0):
        with self.lock:
            self.file.seek(pos, whence)

    def close(self):
        with self.lock:
            self.file.close()
    '''
