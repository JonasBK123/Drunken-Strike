"""
LDR-sensor via MCP3021 ADC (I2C adresse 0x48)
Konverterer rå ADC-værdi til lux-approksimation: y = ax + b
"""

import smbus2
import time

MCP3021_ADDR = 0x48
BUS_NUM = 1

# Kalibreringskonstanter (tilpas efter måling i mørke og lys)
# y = ax + b  →  lux = A * adc_val + B
A = 0.05   # hældning
B = -10.0  # skæring

def read_adc_raw(bus: smbus2.SMBus) -> int:
    """Læs 10-bit råværdi fra MCP3021."""
    data = bus.read_i2c_block_data(MCP3021_ADDR, 0, 2)
    raw = ((data[0] & 0x3F) << 4) | (data[1] >> 4)
    return raw

def raw_to_lux(raw: int) -> float:
    """Omregn ADC-råværdi til approksimeret lux."""
    lux = A * raw + B
    return max(0.0, lux)

def main():
    with smbus2.SMBus(BUS_NUM) as bus:
        while True:
            raw = read_adc_raw(bus)
            lux = raw_to_lux(raw)
            print(f"ADC råværdi: {raw:4d}  |  Lys: {lux:7.1f} lux")
            time.sleep(1)

if __name__ == "__main__":
    main()
