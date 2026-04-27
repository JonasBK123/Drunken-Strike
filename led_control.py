"""
PWM-styret LED grow-light via GPIO12 (hardware PWM).
Lysstyrke sættes som procent 0–100.
"""

import RPi.GPIO as GPIO
import time

LED_PIN = 12        # hardware PWM pin
PWM_FREQ = 1000     # 1 kHz — over det synlige flimmer-område

# Lysniveauer baseret på lux-måling
LUX_HIGH = 5000     # over denne → LED slukket (nok dagslys)
LUX_LOW  = 500      # under denne → LED fuld styrke

def setup() -> GPIO.PWM:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    pwm = GPIO.PWM(LED_PIN, PWM_FREQ)
    pwm.start(0)
    return pwm

def set_brightness(pwm: GPIO.PWM, percent: float):
    """Sæt lysstyrke 0.0–100.0 %."""
    duty = max(0.0, min(100.0, percent))
    pwm.ChangeDutyCycle(duty)
    print(f"LED lysstyrke: {duty:.1f}%")

def lux_to_brightness(lux: float) -> float:
    """Beregn LED-styrke omvendt proportional med dagslys."""
    if lux >= LUX_HIGH:
        return 0.0
    if lux <= LUX_LOW:
        return 100.0
    return (LUX_HIGH - lux) / (LUX_HIGH - LUX_LOW) * 100.0

def demo():
    pwm = setup()
    try:
        for pct in [0, 25, 50, 75, 100, 50, 0]:
            set_brightness(pwm, pct)
            time.sleep(1)
    finally:
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    demo()
