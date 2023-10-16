import pyvisa as visa

rm = visa.ResourceManager()
dispositivos =  rm.list_resources("USB?*")

for dispositivo in dispositivos:
    print(dispositivo)

# Osciloscópio: USB0::0x0699::0x0368::C012397::INSTR
# Gerador USB0::0x0699::0x0349::C012352::INSTR
