import machine
import sdcard
import os
import board_def as BD


class SDCardManager:
    """Manages SD card initialization and access"""
    def __init__(self, cs_pin=5):
        self.cs = machine.Pin(BD.SD_CS, machine.Pin.OUT)
        self.spi = machine.SPI(0, 
                               baudrate=1000000, 
                               mosi=machine.Pin(BD.SD_MOSI), 
                               miso=machine.Pin(BD.SD_MISO), 
                               sck=machine.Pin(BD.SD_CLK))
        self.sd = sdcard.SDCard(self.spi, self.cs)
        os.mount(self.sd, "/sd")
    
    def unmount(self):
        os.umount("/sd")

# Main program
if __name__ == "__main__":
    # Initialize SD card once
    sd_manager = SDCardManager()
    
    # Now pass sd_manager to your classes
    # Example: my_class = MyClass(sd_manager)
    
    # Your program logic here
    
    # Cleanup
    sd_manager.unmount()

    def read_file(sd_manager, filename):
        """Read file from SD card"""
        with open(f"/sd/{filename}", "r") as f:
            return f.read()

    def write_file(sd_manager, filename, data):
        """Write file to SD card"""
        with open(f"/sd/{filename}", "w") as f:
            f.write(data)