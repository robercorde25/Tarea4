# Tarea4

Carné: B72299.

Nombre: Roberto Cordero Jiménez.

## Crear un esquema de modulación BPSK para los bits presentados.

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




























