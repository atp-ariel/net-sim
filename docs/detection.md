# Algoritmos de detección de errores

---

Como se conoce cada Trama tiene un campo que representa información útil para detectar errores en los datos, y el tamaño de la información anterior. Por tanto, una trama queda de la siguiente forma:

* INIT BIT (1 bit) 2
* MAC de destino (16 bits)
* MAC de origen (16 bits)
* Tamaño de los datos (8 bits)
* Tamaño de los datos de verificación (8 bits)
* Datos 
* Datos de verificación 

Cada vez que se hace referencia al tamaño, se hace referencia al tamaño en bytes de los datos.

## Patrón de diseño para solucionar el problema.

---

Para solucionar el problema de varios algoritmos de detección se implementó el patrón de comportamiento conocido como Strategy.

Se creó una interfaz denominada `IStrategy_Detection` que comprueba y aplica utilizando la estrategio o algoritmo específico si una trama fue enviada con errores.

### Hash Sum

Para configurar el algoritmo Hash Sum, es necesario en el campo `error-detection` introducir `hash-sum`. 

El funcionamiento de este algoritmo es tomar la representación de cada byte de los datos en base 10 y sumarlos. Este resultado se lleva a binario y se envía como dato de verificación. 

Por ejemplo: sea `d = 101001001001010111110001`, los bytes son los siguientes:

* `11110001` que representa 241
* `10010101` que representa 149
* `10100100` que representa 164

La suma de estos valores es 554, que su representación en binario es: `0000001000101010`, que se representa en 2 bytes.

### Bit de paridad

Para configurar el algoritmo Hash Sum, es necesario en el campo `error-detection` introducir `parity`. 

Dado un dato se añade un bit que representa  (1) si la cantidad de unos en la representación binaria de los datos es impar, (0) en caso contrario.

Sea añade como dato de verificación un byte cuyo último bit es el bit de paridad.

### CRC 16

Para configurar el algoritmo Hash Sum, es necesario en el campo `error-detection` introducir `crc-16`. 

La comprobación de redundancia cíclica o también conocido como Polynomial Code Checksum. Es una función diseñada para detectar alteraciones en las tramas envíadas a través de una red de computadoras.

En este caso se implementó el CRC cuyo polinomio generador es $x^{16} + x^{15} + x^{2} + 1$, la representación binaria del polinomio es la siguiente: 0b11000000000000101. El dato de verificación está basado en residuos  de una división de polinomios. 

