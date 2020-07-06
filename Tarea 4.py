# -*- coding: utf-8 -*-
"""
Created on Sun May 31 10:23:37 2020

@author: Roberto Cordero Jimenez
Carne: B72299
Modelos Probabilisticos de Senales y Sistemas
"""

import numpy as np
from numpy import exp, linspace, random
from scipy import stats
from scipy import signal
from scipy import integrate
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv
from fitter import Fitter
from pylab import linspace, plot
from mpl_toolkits import mplot3d

#1. Crear un esquema de modulación BPSK para los bits presentados. 

"""
bits10k.csv en float
"""

archivo = np.loadtxt(open("bits10k.csv", "r"),str, delimiter=",")
bits = archivo.astype(float)

"""
Numero de bits
"""
N = 10000

"""
Frecuencia de la portadora
"""
f=5000 #Hz

"""
Periodo de la portadora
"""
T= 1/f


"""
Puntos de muestreo para cada periodo (bit)
"""
p=50

"""
Eje x cada periodo de la onda portadora
"""
tp = np.linspace(0,T,p)


"""
Eje y de cada periodo (creacion de la forma de onda portadora)
"""

sinus = np.sin(2*np.pi*f*tp)

"""
Grafica de la portadora
"""
plt.figure(1)
plt.title("Forma de la portadora")
plt.plot(tp,sinus)
plt.xlabel("Tiempo del periodo")
plt.ylabel("Amplitud de la portadora")
plt.show()

"""
Frecuencia de muestreo
"""

fs= p/T


"""
Eje x la señal portadora con todos los bits
"""

t= np.linspace(0,N*T,N*p)

"""
Eje y la señal portadora con todos los bits (modulacion BPSK)
"""

senal = np.zeros(t.shape)

for k, b in enumerate(bits):
    if b==1:
        senal[k*p:(k+1)*p] = b*sinus
    else:
        senal[k*p:(k+1)*p] = -1*sinus



"""
Grafica de la modulacion BPSK (Primeros 5 bits para una mejor visualizacion)
"""

pb=5
plt.figure(2)
plt.title("Senal modulada")
plt.plot(senal[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()
print("Los primeros cinco bits son: " + str(bits[0:5]))

#2. Calcular la potencia promedio de la senal modulada generada. 

potencia = senal**2
Ps = (integrate.trapz(potencia,t)) / (N*T)

print("La potencia de la senal es: " + str(Ps))

#3. Simular un canal ruidoso tipo AWNG (ruido aditivo blanco gaussiano).  Con una relación señal a ruido (SNR) desde -2 hasta 3 dB.


"""
Creacion del vector desde -2dB hasta 3dB
"""

SNRm2 = -2
SNRm1 = -1
SNR0 = 0
SNR1 = 1
SNR2 = 2
SNR3 = 3

                  
"""
Potencia de la senal con ruido
"""

Pnm2 = Ps/ (10**(SNRm2/10)) #Se obtuvo de un despeje a mano
Pnm1 = Ps/ (10**(SNRm1/10)) 
Pn0 = Ps/ (10**(SNR0/10))
Pn1 = Ps/ (10**(SNR1/10))
Pn2 = Ps/ (10**(SNR2/10))
Pn3 = Ps/ (10**(SNR3/10))

"""
Desviacion estandar de los ruidos
"""
sigmam2 = np.sqrt(Pnm2)
sigmam1 = np.sqrt(Pnm1)
sigma0 = np.sqrt(Pn0)
sigma1 = np.sqrt(Pn1)
sigma2 = np.sqrt(Pn2)
sigma3 = np.sqrt(Pn3)

"""
Creacion del ruido desde -2dB hasta 3dB
"""
ruidom2 = np.random.normal(0,sigmam2,senal.shape)
ruidom1 = np.random.normal(0,sigmam1,senal.shape)
ruido0 = np.random.normal(0,sigma0,senal.shape)
ruido1 = np.random.normal(0,sigma1,senal.shape)
ruido2 = np.random.normal(0,sigma2,senal.shape)
ruido3 = np.random.normal(0,sigma3,senal.shape)

"""
Simulacion de las cinco senales a traves de un canal con ruido
"""

Rxm2 = senal + ruidom2
Rxm1 = senal + ruidom1
Rx0 = senal + ruido0
Rx1 = senal + ruido1
Rx2 = senal + ruido2
Rx3 = senal + ruido3

"""
Visualizacion de las cinco senales (primeros bits) a traves de un canal con ruido
"""

pb=5
plt.figure(3)
plt.title("Senal modulada con un ruido de -2dB")
plt.plot(Rxm2[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()

plt.figure(4)
plt.title("Senal modulada con ruido de -1dB")
plt.plot(Rxm1[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()

plt.figure(5)
plt.title("Senal modulada con ruido de 0dB")
plt.plot(Rx0[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()

plt.figure(6)
plt.title("Senal modulada con ruido de 1dB")
plt.plot(Rx1[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()

plt.figure(7)
plt.title("Senal modulada con ruido de 2dB")
plt.plot(Rx2[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()

plt.figure(8)
plt.title("Senal modulada con ruido de 3dB")
plt.plot(Rx3[0:pb*p])
plt.xlabel('Tiempo (ms)')
plt.show()





#4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.


# Antes del canal ruidoso
fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.figure(9)
plt.title("Densidad espectral de la senal modulada")
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.show()

# Después del canal ruidoso
fwm2, PSDm2 = signal.welch(Rxm2, fs, nperseg=1024)
fwm1, PSDm1 = signal.welch(Rxm1, fs, nperseg=1024)
fw0, PSD0 = signal.welch(Rx0, fs, nperseg=1024)
fw1, PSD1 = signal.welch(Rx1, fs, nperseg=1024)
fw2, PSD2 = signal.welch(Rx2, fs, nperseg=1024)
fw3, PSD3 = signal.welch(Rx3, fs, nperseg=1024)
plt.figure(10)
plt.title("Densidad espectral de la senal modulada con los cinco ruidos")
plt.semilogy(fwm2, PSDm2, label='Linea -2dB')
plt.semilogy(fwm1, PSDm1, label='Linea -1dB')
plt.semilogy(fw0, PSD0, label='Linea 0dB')
plt.semilogy(fw1, PSD1, label='Linea 1dB')
plt.semilogy(fw2, PSD2, label='Linea 2dB')
plt.semilogy(fw3, PSD3, label='Linea 3dB')
plt.legend()
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.show()



#5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.
"""
Vector de bits recibidos para los cinco ruidos
"""
bitsRxm2 = np.zeros(bits.shape)
bitsRxm1 = np.zeros(bits.shape)
bitsRx0 = np.zeros(bits.shape)
bitsRx1 = np.zeros(bits.shape)
bitsRx2 = np.zeros(bits.shape)
bitsRx3 = np.zeros(bits.shape)


"""
Decodificacion de la senal por medio de energia (obtenida del producto de senales) para los cinco ruidos distindos
"""

for k, b in enumerate(bits):
    PE = np.sum(Rxm2[k*p:(k+1)*p]*sinus)
    if PE > 0:
        bitsRxm2[k] = 1
    else:
        bitsRxm2[k] = 0
        
for k, b in enumerate(bits):
    PE = np.sum(Rxm1[k*p:(k+1)*p]*sinus)
    if PE > 0:
        bitsRxm1[k] = 1
    else:
        bitsRxm1[k] = 0
        
for k, b in enumerate(bits):
    PE = np.sum(Rx0[k*p:(k+1)*p]*sinus)
    if PE > 0:
        bitsRx0[k] = 1
    else:
        bitsRx0[k] = 0
        
for k, b in enumerate(bits):
    PE = np.sum(Rx1[k*p:(k+1)*p]*sinus)
    if PE > 0:
        bitsRx1[k] = 1
    else:
        bitsRx1[k] = 0
        
for k, b in enumerate(bits):
    PE = np.sum(Rx2[k*p:(k+1)*p]*sinus)
    if PE > 0:
        bitsRx2[k] = 1
    else:
        bitsRx2[k] = 0
        
for k, b in enumerate(bits):
    PE = np.sum(Rx3[k*p:(k+1)*p]*sinus)
    if PE > 0:
        bitsRx3[k] = 1
    else:
        bitsRx3[k] = 0


print("Los primeros cinco bits son: " + str(bits[0:5]))
print("Los primeros cinco bits demodulados de la senal con -2dB de ruido son: " + str(bitsRxm2[0:5]))
print("Los primeros cinco bits demodulados de la senal con -1dB de ruido son: " + str(bitsRxm1[0:5]))
print("Los primeros cinco bits demodulados de la senal con 0dB de ruido son: " + str(bitsRx0[0:5]))
print("Los primeros cinco bits demodulados de la senal con 1dB de ruido son: " + str(bitsRx1[0:5]))
print("Los primeros cinco bits demodulados de la senal con 2dB de ruido son: " + str(bitsRx2[0:5]))
print("Los primeros cinco bits demodulados de la senal con 3dB de ruido son: " + str(bitsRx3[0:5]))

errm2 = np.sum(np.abs(bits - bitsRxm2))
errm1 = np.sum(np.abs(bits - bitsRxm1))
err0 = np.sum(np.abs(bits - bitsRx0))
err1 = np.sum(np.abs(bits - bitsRx1))
err2 = np.sum(np.abs(bits - bitsRx2))
err3 = np.sum(np.abs(bits - bitsRx3))

BERm2 = (errm2/N)
BERm1 = (errm1/N)
BER0 = (err0/N)
BER1 = (err1/N)
BER2 = (err2/N)
BER3 = (err3/N)

print("Hubo un porcentaje de error del: " + str(BERm2) + "% en la senal de -2dB.")
print("Hubo un porcentaje de error del: " + str(BERm1) + "% en la senal de -1dB.")
print("Hubo un porcentaje de error del: " + str(BER0) + "% en la senal de 0dB.")
print("Hubo un porcentaje de error del: " + str(BER1) + "% en la senal de 1dB.")
print("Hubo un porcentaje de error del: " + str(BER2) + "% en la senal de 2dB.")
print("Hubo un porcentaje de error del: " + str(BER3) + "% en la senal de 3dB.")


#6. Graficar BER vs. SNR


BER = [BERm2,BERm1,BER0,BER1,BER2,BER3 ]

plt.figure(6)
plt.title("BER vs. SNR")
plt.plot([-2,-1,0,1,2,3],BER,'ro')
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.show()


































