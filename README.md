# Tarea4

Carné: B72299.

Nombre: Roberto Cordero Jiménez.

## 1. Crear un esquema de modulación BPSK para los bits presentados.

Para crear la modulacion se utilizo el esquema BPSK el cual codifica los bits mediante una onda portadora sinusoidal. Dicha onda portadora asignara una onda con una fase de 0 grados si el bit es igual a 1 y, de igual forma, asignara una onda con una fase de 180 grados a los bits cuyos valores sean iguales a 0.

La forma de la onda prtadora fue la siguiente:

![alt text][Portadora]

[Portadora]: https://github.com/robercorde25/Tarea4/blob/master/Portadora.PNG "Logo Title Text 2"

Y se implemento mediante el codigo:

```python
#Frecuencia de la portadora
f=5000 #Hz

#Periodo de la portadora
T= 1/f

#Puntos de muestreo para cada periodo (bit)
p=50

#Eje x cada periodo de la onda portadora
tp = np.linspace(0,T,p)

#Eje y de cada periodo (creacion de la forma de onda portadora)
sinus = np.sin(2*np.pi*f*tp)
```

Despues se modulo la senal y y se obtuvo la siguiente visualizacion, donde se muestran los primeros cinco bits codificados:

![alt text][Modulada]

[Modulada]: https://github.com/robercorde25/Tarea4/blob/master/Modulada.PNG "Logo Title Text 2"

La modulacion anterior se implemento por medio del codigo siguiente:

```python

#Eje x la señal portadora con todos los bits
t= np.linspace(0,N*T,N*p)

#Eje y la señal portadora con todos los bits (modulacion BPSK)

senal = np.zeros(t.shape)

for k, b in enumerate(bits):
    if b==1:
        senal[k*p:(k+1)*p] = b*sinus
    else:
        senal[k*p:(k+1)*p] = -1*sinus

```

El codigo anterior indica que si el bit por codificar es igual a 1, entonces la modulacion en ese periodo sera igual a la forma seno (con fase de 0 grados); mientras que si el bit por codificar es igual a 0,  la modulacion en ese periodo sera igual a -seno (el cual tiene una fase de 180 grados).



## 2. Calcular la potencia promedio de la señal modulada generada.

Para calcular la potencia promedio de la senal se utilizo la biblioteca integrate mediante el codigo siguiente:


```python
potencia = senal**2
Ps = (integrate.trapz(potencia,t)) / (N*T)
```

De la cual se obtuvo el resultado: 

![alt text][Ec1]

[Ec1]: https://latex.codecogs.com/svg.latex?Ps%20=%200.49



## 3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.

Seguidamente, se simularon se distintos canales por los cuales la senal modulada debia pasar (-2dB, -1dB, 0dB, 1dB, 2dB, 3dB), donde se obtuvieron siguientes las visualizaciones para los primeros cinco bits:


![alt text][-2]

[-2]: https://github.com/robercorde25/Tarea4/blob/master/-2.PNG "Logo Title Text 2"


![alt text][-1]

[-1]: https://github.com/robercorde25/Tarea4/blob/master/-1.PNG "Logo Title Text 2"


![alt text][0]

[0]: https://github.com/robercorde25/Tarea4/blob/master/0.PNG "Logo Title Text 2"


![alt text][1]

[1]: https://github.com/robercorde25/Tarea4/blob/master/1.PNG "Logo Title Text 2"


![alt text][2]

[2]: https://github.com/robercorde25/Tarea4/blob/master/2.PNG "Logo Title Text 2"


![alt text][3]

[3]: https://github.com/robercorde25/Tarea4/blob/master/3.PNG "Logo Title Text 2"


## 4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.

Para la senal modulada, sin atravesar ningun canal, se obtuvo la grafica de densidad espectral siguiente:

![alt text][Den1]

[Den1]: https://github.com/robercorde25/Tarea4/blob/master/Den1.PNG "Logo Title Text 2"

Asimismo, cuando la onda modulada atraviesa los distintos canales, se tienen los resultados siguientes:

![alt text][Den2]

[Den2]: https://github.com/robercorde25/Tarea4/blob/master/Den2.PNG "Logo Title Text 2"

En ambas graficas se observa que la concentracion de energia se da alrededor de la componente fundamental de 5kHz.


## 5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.

En la decodificacion se realizo un producto de senales por periodo, donde se tomaron la forma original de la senal portadora (seno) y la senal modulada despues de haber atravesado uno se los cinco canales. Dicho producto implicaba una senal con fase 0 (portadora con forma seno) y una senal ya sea con una fase de 0 o 180 grados mas su ruido (bits codificados). Si el producto de dichas senal es positivo, significa que el bit codificado es 1 puesto que el mismo corresponde a una senal con fase de 0 grados; no asi, cuando el producto es negativo, el bit codificado era 0 puesto que este corresponde a una senal con fase de 180 grados.

La decodificacion se realizo por medio del codigo siguiente:

```python

#Simulacion de las cinco senales a traves de un canal con ruido
Rxm2 = senal + ruidom2
Rxm1 = senal + ruidom1
Rx0 = senal + ruido0
Rx1 = senal + ruido1
Rx2 = senal + ruido2
Rx3 = senal + ruido3


#Vector de bits recibidos para los cinco ruidos
bitsRxm2 = np.zeros(bits.shape)
bitsRxm1 = np.zeros(bits.shape)
bitsRx0 = np.zeros(bits.shape)
bitsRx1 = np.zeros(bits.shape)
bitsRx2 = np.zeros(bits.shape)
bitsRx3 = np.zeros(bits.shape)


#Demodulacion de las senales con distintos ruidos (-2dB, -1dB, 0dB, 1dB, 2dB, 3dB).
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
```

Despues de la decodificacion se hizo un conteo de errores para cada una de las senales, donde se obtuvo los resultados siguientes:

- ![alt text][Ec2]

[Ec2]: https://latex.codecogs.com/svg.latex?E_{-2dB}%20=%200% "Logo Title Text 2"

- ![alt text][Ec3]

[Ec3]: https://latex.codecogs.com/svg.latex?E_{-1dB}%20=%200% "Logo Title Text 2"

- ![alt text][Ec2]

[Ec4]: https://latex.codecogs.com/svg.latex?E_{0dB}%20=%200% "Logo Title Text 2"

- ![alt text][Ec2]

[Ec5]: https://latex.codecogs.com/svg.latex?E_{1dB}%20=%200% "Logo Title Text 2"

- ![alt text][Ec2]

[Ec6]: https://latex.codecogs.com/svg.latex?E_{2dB}%20=%200% "Logo Title Text 2"

- ![alt text][Ec2]

[Ec7]: https://latex.codecogs.com/svg.latex?E_{3dB}%20=%200% "Logo Title Text 2"
