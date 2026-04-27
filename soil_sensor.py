"""
Jordfugtsensor via MCP3021 ADC (I2C adresse 0x48)
Returnerer fugtprocent og tør/våd-status.
"""

import smbus2
import time

MCP3021_ADDR = 0x48
BUS_NUM = 1

# Kalibrér disse værdier: mål råværdi i tør jord og i vand
ADC_DRY = 900    # råværdi i tør jord
ADC_WET = 400    # råværdi i fuld vand

MOISTURE_THRESHOLD = 30.0  # procent — under denne → TØR → tænd pumpe

def read_adc_raw(bus: smbus2.SMBus) -> int:
    data = bus.read_i2c_block_data(MCP3021_ADDR, 0, 2)
    raw = ((data[0] & 0x3F) << 4) | (data[1] >> 4)
    return raw

def raw_to_moisture_pct(raw: int) -> float:
    """Omregn råværdi til fugtprocent (0 = tør, 100 = våd)."""
    pct = (ADC_DRY - raw) / (ADC_DRY - ADC_WET) * 100.0
    return max(0.0, min(100.0, pct))

def is_dry(moisture_pct: float) -> bool:
    return moisture_pct < MOISTURE_THRESHOLD

def main():
    with smbus2.SMBus(BUS_NUM) as bus:
        while True:
            raw = read_adc_raw(bus)
            pct = raw_to_moisture_pct(raw)
            status = "TØR → pump ON" if is_dry(pct) else "FUGTig → pump OFF"
            print(f"ADC: {raw:4d}  |  Fugt: {pct:5.1f}%  |  {status}")
            time.sleep(2)

if __name__ == "__main__":
    main()
