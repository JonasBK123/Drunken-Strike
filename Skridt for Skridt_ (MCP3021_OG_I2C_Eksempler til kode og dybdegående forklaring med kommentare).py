# Væksthus m. I2C (Med kommentare og forklaring i "step by step"

# "Hvad er I2C? (helt konkret)"
# Kort sagt: I2C er en måde for Raspberry Pi at snakke med chips (fx MCP3021)
				#Det bruger kun 2 ledninger: SDA → data & SCL → clock (timing) => GND og VCC

# "Hvordan fungerer det?"
# Raspberry Pi er master & MCP3021 er slave -> Pi siger: “Hey, giv mig din værdi” -> MCP3021 svarer med data

# Vigtigt at HUSKE-> (!!)
# (1): Hver enhed har en adresse // (2): MCP3021 har fx en I2C adresse (fx 0x48)

# "Hvad gør MCP3021?"
# Funktion for MCP3021 er: (1): Måler spænding (0–3.3V) // (2): Returnerer et tal (0–1023)

# Det vi får returneret er (Den her del er vigtig, at huske. Da det ofte er her der sker fejl)
## Vi får hhv:
                    #(1): 10-bit værdi
                    # MEN- Det er vigtigt at være obs på:
                    # "10-bit værdien" bliver sendt som 2 bytes
                    # Den bliver: bit-shiftet
                    # Den sendes i "big endian"
                    
#De nedenstående steps, er process til hvordan I2C sættes op, med korrektanvendt kodestruktur: "KONKRET Python kode (Raspberry Pi)"
                    
#(1) Installation af I2C:
                        # sudo raspi-config // Heri, skal I2C aktiveres/tændes

#(2) Installer Lib:
                        # pip install smbus2 // Her installeres, og initiere vi det korrekte lib til kommende arbejde
                        
#[HER KOMMER NU ET EKSEMPEL PÅ "HEL" KODESTRUKTUR UD FRA OVENSTÅENDE]

# from smbus2 import SMBus

# I2C_BUS = 1
# MCP3021_ADDR = 0x48

# def read_adc():
    # with SMBus(I2C_BUS) as bus:
        #(1) data = bus.read_i2c_block_data(MCP3021_ADDR, 0x00, 2)
        
        #(OBS PÅ DETTE: // data[0] = MSB, data[1] = LSB) 
        
        #(2) raw = (data[0] << 8) | data[1]   # Her samles bytes
        
        #(3) adc_value = raw >> 2  // # Her fjernes de 2 ekstra bits
        
        #(4) return adc_value

# while True:
    # val = read_adc()
    # print("ADC:", val)

#[FORKLARING TIL OVENSTÅENDE]
    #(1) = Her læses dataen: Man vil eksempelvis få vist som dette: "[0b10101010, 0b11000000]" #Så vi bruger linjen, til at læse og "forstå/formattere" dataen
    
    #(2) = Samler bytes: Betyder, at der skal: "Flyt første byte til venstre og læg anden til"
    
    #(3) = Fix Bit Shift: Da vi som forklaret før, får "rå data", skal vores data "fixes", da vi har anvendt ovenstående "bit shift".
            #Denne linje er essentiel, da vi har fået MCP3021 har forskudt 2 bits
    
### DET STORE FORMÅL MED HVORFOR DETTE ER VIGTIGT: DETTE ER VIGTIGT FORDI, VORES MCP3021 SENDER RÅ DATA. DET SKAL FORMATTERES, DA VORES RASPBERRY PI, FORVENTER KORREKT FORMAT AF DATA.
                                                    # DET VIL OGSÅ SIGE, AT HVIS IKKE VI GØR DETTE, VIL VORES SYSTEM IKKE FUNGERE. DA VI ARBEJDER MED RASPBERRY PI SOM "FUNDAMENT".
                                                    
#[ET KODEEKSEMPEL TIL IMPLEMENTATION I VORES SYSTEM/KREDSLØB]

                        #(1): adc = read_adc()

                        ## lys regulering ##
                                                    
                        #(2): duty = a * adc + b

                        ## fugt regulering ##

                        #(3): if adc < threshold:
                                #pump_on()
                            # else:
                                #pump_off()
