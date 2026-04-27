"""
Væksthus-controller — hovedprogram.
Læser sensorer via MCP3021, styrer LED og pumpe.
Løkke-interval: 10 sekunder.
"""

import smbus2
import RPi.GPIO as GPIO
import time

from ldr_sensor    import read_adc_raw as ldr_raw,  raw_to_lux,           MCP3021_ADDR
from soil_sensor   import read_adc_raw as soil_raw, raw_to_moisture_pct,  is_dry
from led_control   import setup as led_setup, set_brightness, lux_to_brightness
from pump_control  import setup as pump_setup, run_if_dry, cleanup as pump_cleanup

# ----- Hvilken kanal bruges til hvad? -----
# MCP3021 har kun ÉN analog kanal (VIN-pin).
# Skift manuelt mellem LDR og jordfugt ved at bruge to separate MCP3021-chips
# med forskellige I2C-adresser (0x48 og 0x49 via A0-pin).

LDR_ADC_ADDR  = 0x48
SOIL_ADC_ADDR = 0x49
BUS_NUM = 1
LOOP_INTERVAL = 10  # sekunder mellem målinger

def read_ldr(bus: smbus2.SMBus) -> float:
    data = bus.read_i2c_block_data(LDR_ADC_ADDR, 0, 2)
    raw = ((data[0] & 0x3F) << 4) | (data[1] >> 4)
    return raw_to_lux(raw)

def read_soil(bus: smbus2.SMBus) -> float:
    data = bus.read_i2c_block_data(SOIL_ADC_ADDR, 0, 2)
    raw = ((data[0] & 0x3F) << 4) | (data[1] >> 4)
    return raw_to_moisture_pct(raw)

def main():
    pwm = led_setup()
    pump_setup()

    try:
        with smbus2.SMBus(BUS_NUM) as bus:
            while True:
                # Læs sensorer
                lux      = read_ldr(bus)
                moisture = read_soil(bus)

                print(f"\n[{time.strftime('%H:%M:%S')}]")
                print(f"  Lys:  {lux:.1f} lux")
                print(f"  Fugt: {moisture:.1f}%")

                # Styr LED baseret på lysniveau
                brightness = lux_to_brightness(lux)
                set_brightness(pwm, brightness)

                # Styr pumpe baseret på jordfugt
                run_if_dry(moisture)

                time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        print("\nAfslutter...")
    finally:
        pwm.stop()
        pump_cleanup()

if __name__ == "__main__":
    main()
