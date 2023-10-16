# Código adaptado de https://github.com/tektronix/Programmatic-Control-Examples/tree/master/Examples/Signal_Sources/src/AFG3KSendWaveformExample/python


import numpy as np # http://www.numpy.org/
import pyvisa # https://pyvisa.readthedocs.io/en/stable/
from lcapy import u,t,exp

# variables
visa_descriptor = 'USB0::0x0699::0x0349::C012352::INSTR'
record_length = 4096


# Editar parâmetros
nome_arquivo = "sinal.txt"
tempo_final = 10
pontos = record_length
expressao = u(t)-u(t-2)+(t-4)*u(t-4)-(t-6)*u(t-6)-(t-8)*u(t-8)+(t-10)*u(t-10)  #10*t*u(t)-20*(t-2)*u(t-2)+10*(t-4)*u(t-4)
# Editar até aqui
tempo = np.linspace(0.0000000000000000000001,tempo_final,pontos)
sinal = expressao.evaluate(tempo)


# calculations
# example arbitrary function: 1-cycle sine
sample = np.arange(record_length)
vector = np.sin(2 * np.pi * sample / len(sample))

vector = sinal # Substitui o sinal do exemplo pelo gerado pela expressão

# Normalizando os valores para o DAC
m = 16382 / (vector.max() - vector.min())
b = -m * vector.min()
dac_values = (m * vector + b)
np.around(dac_values, out=dac_values)
dac_values = dac_values.astype(np.uint16)


# instrument communication
rm = pyvisa.ResourceManager()
afg = rm.open_resource(visa_descriptor)
afg.write_termination = None
afg.read_termination = '\n'
afg.timeout = 10000 # ms


afg.write('*cls')
r = afg.query('*esr?')
print(' esr value: 0b{:08b}'.format(int(r)))
r = afg.query('system:error?')
print(' msg: {}'.format(r))

#Coloca o gerador no modo de forma de onda arbitrária
afg.write("FUNCtion EMEMory")
# Ajusta a amplitude pelo sinal original
amplitude = vector.max() - vector.min()
afg.write(f'VOLTage:AMPLitude {amplitude}')
print(f"Definindo amplitude para {amplitude}")

# Ajusta o período pelo tempo final
periodo = tempo_final
afg.write(f"FREQuency {1/periodo}")

cmd = 'data:define EMEM,{:d}'.format(record_length)
print('writing: "{}"'.format(cmd))
afg.write(cmd)
r = afg.query('*esr?')
print(' esr value: 0b{:08b}'.format(int(r)))
r = afg.query('system:error?')
print(' msg: {}'.format(r))

afg.write_binary_values('data EMEM,',
                        dac_values,
                        datatype='h',
                        is_big_endian=True)
r = afg.query('*esr?')
print(' esr value: 0b{:08b}'.format(int(r)))
r = afg.query('system:error?')
print(' msg: {}'.format(r))

print('Desconectando...')
afg.close()

print('Pronto')