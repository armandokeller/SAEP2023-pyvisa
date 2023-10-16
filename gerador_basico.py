import pyvisa as visa
from time import sleep

rm = visa.ResourceManager()
gerador = rm.open_resource("USB0::0x0699::0x0349::C012352::INSTR")

# Consulta a string de identificação do gerador
resposta = gerador.query("*IDN?")
print(resposta)

print("Forma de onda senoidal")
# Define a forma de onda para senoidal
gerador.write("FUNCtion SINusoid")
# Define a amplitude para 2 Vpp
gerador.write("VOLTage 2")
# Define a frequência para 1 kHz
gerador.write("FREQuency 1E3")
# Define a saida para High Z
gerador.write("OUTPut:IMPedance INFinity")
# Liga a saída
gerador.write("OUTPut ON")

sleep(10)
print("Forma de onda quadrada")
gerador.write("FUNCtion SQUare")

sleep(10)
print("Forma de onda rampa")
gerador.write("FUNCtion RAMP")

sleep(10)
print("Forma de onda arbitrária")
gerador.write("FUNCtion EMEMory")