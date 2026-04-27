"""
Relæ-styret vandpumpe via GPIO17.
Pumpen kører i et tidsbaseret puls for at undgå overblødning.
"""

import RPi.GPIO as GPIO
import time

PUMP_PIN = 17           # GPIO pin til relæ IN
PUMP_ON_TIME  = 5.0     # sekunder pumpen kører ad gangen
PUMP_OFF_TIME = 30.0    # sekunder pause mellem pulsringer

# Relæmoduler er typisk aktiv-LOW: HIGH = slukket, LOW = tændt
RELAY_ACTIVE = GPIO.LOW
RELAY_IDLE   = GPIO.HIGH

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUMP_PIN, GPIO.OUT, initial=RELAY_IDLE)

def pump_on():
    GPIO.output(PUMP_PIN, RELAY_ACTIVE)
    print("Pumpe: TIL")

def pump_off():
    GPIO.output(PUMP_PIN, RELAY_IDLE)
    print("Pumpe: FRA")

def water_pulse(on_time: float = PUMP_ON_TIME):
    """Kør pumpen i `on_time` sekunder, derefter sluk."""
    pump_on()
    time.sleep(on_time)
    pump_off()

def run_if_dry(moisture_pct: float):
    """Kald denne fra hovdprogrammet med aktuel fugtprocent."""
    if moisture_pct < 30.0:
        print(f"Jord tør ({moisture_pct:.1f}%) — starter vandpuls")
        water_pulse()
    else:
        print(f"Jord OK ({moisture_pct:.1f}%) — pumpe inaktiv")

def cleanup():
    pump_off()
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        water_pulse(on_time=3)
        time.sleep(2)
    finally:
        cleanup()
