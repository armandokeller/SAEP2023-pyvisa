# Código adaptado de https://github.com/tektronix/Programmatic-Control-Examples/tree/master/Examples/Oscilloscopes/BenchScopes/src/SimplePlotExample
import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt

rm = visa.ResourceManager()
osciloscopio = rm.open_resource("USB0::0x0699::0x0368::C012397::INSTR")

# Consulta a string de identificação do osciloscópio
resposta = osciloscopio.query("*IDN?")
print(resposta)

osciloscopio.timeout = 10000 # ms
osciloscopio.encoding = 'latin_1'
osciloscopio.read_termination = '\n'
osciloscopio.write_termination = None
osciloscopio.write('*cls') # clear ESR
osciloscopio.write('*rst') # reset

osciloscopio.write('autoset EXECUTE') # autoset


# io config
osciloscopio.write('header 0')
osciloscopio.write('data:encdg RIBINARY')
osciloscopio.write('data:source CH1') # channel
osciloscopio.write('data:start 1') # first sample
record = int(osciloscopio.query('wfmpre:nr_pt?'))
osciloscopio.write('data:stop {}'.format(record)) # last sample
osciloscopio.write('wfmpre:byt_nr 1') # 1 byte per sample

# acq config

#osciloscopio.write("ACQuire:MODe AVErage") # Modo de aquisição (normal
#osciloscopio.write("ACQuire:NUMAVg 64") # Amostra por média (16 amostras)

osciloscopio.write('acquire:state 0') # stop
osciloscopio.write('acquire:stopafter SEQUENCE') # single
osciloscopio.write('acquire:state 1') # run
r = osciloscopio.query('*opc?') # sync

# Recebe os dados da curva
bin_wave = osciloscopio.query_binary_values('curve?', datatype='b', container=np.array)


# Recebe os dados das escalas 
tscale = float(osciloscopio.query('wfmpre:xincr?'))
tstart = float(osciloscopio.query('wfmpre:xzero?'))
vscale = float(osciloscopio.query('wfmpre:ymult?')) # volts / level
voff = float(osciloscopio.query('wfmpre:yzero?')) # reference voltage
vpos = float(osciloscopio.query('wfmpre:yoff?')) # reference position (level)


# Ajusta os vetores para as escalas
# horizontal (tempo)
total_time = tscale * record
tstop = tstart + total_time
scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)
# vertical (tensão)
unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
scaled_wave = (unscaled_wave - vpos) * vscale + voff


# Plota o gráfico
plt.plot(scaled_time, scaled_wave)
plt.title('Osciloscópio -  CH1')
plt.xlabel('Tempo [s]')
plt.ylabel('Tensão [V]')
plt.show()