from time import sleep
import smbus

i2c_address = 0x4B  # default address​

class SoilMoist:
    def __init__(self, i2c_addr=0x48):
        self.i2c_addr = i2c_addr
        self.bus = smbus.SMBus(1)
        
    
    def soil_raw_adc(self):
        rd = self.bus.read_word_data(self.i2c_addr, 0)
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        data = data >> 2
        return data
    
    def ldr_percent(self):
        data = soilmoist.soil_raw_adc()
        percentage = (data/60) * 100.0
        data_perc = round(percentage, 2)
        return data_perc
        

soilmoist = SoilMoist()


while True: 
    print(soilmoist.soil_raw_adc())
    sleep(0.5)


   # a = -60.0 / (brightAdc-darkAdc) # Calculate coefficients for brightness formula
  #  b = a * brightAdc + redDcmin


    #def brightnessToDutyCycles(alpha, beta): # Measure brightness and return duty cycles
  #      adcVal = brightnessAdc.read() # Read the brightness ADC
  #      redDc = alpha * adcVal + beta # Calc. the red duty cycle
   #     blueDc = redDc * 77 / 60 # If 24 V and six diodes per color
    #    return redDc, blueDc

 #   while True:

     #   redDutyCycle, blueDutyCycle = brightnessToDutyCycles(a, b)
       # redLedsPwm.ChangeDutyCycle(redDutyCycle)
      #  blueLedsPwm.ChangeDutyCycle(blueDutyCycle)