import smbus
import time

class MCP3021:
    bus = smbus.SMBus(1)

    def __init__(self, address = 0x4B):
        self.address = address

    def read_raw(self):
        # reads word (16bits) as int
        rd = self.bus.read_word_data(self.address, 0)
        # exchanges upper and lower bytes
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        # ignores two least significant bits
        return data >> 2
    
    def read_prct(self):
        rd = self.bus.read_word_data(self.address, 0)
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        raw = data >> 2
        wet = (779-raw)*100/(779-300)
        return wet

adc = MCP3021()

while True:
    raw = adc.read_raw()
    prct = adc.read_prct()
    print("Raw :", raw)
    print("wet: ", prct)
    time.sleep(1)