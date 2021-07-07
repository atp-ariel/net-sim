# Detalles de la implementación de la Capa de Enlace

---

La capa de enlace como se mencionó es Full duplex, o sea, todos los cables son de tipo Duplex para garantizar la comunicación en ambos sentidos.

Las tramas que se implementan tienen las siguientes características:

* INIT BIT (1 bit) 2
* MAC de destino (16 bits)
* MAC de origen (16 bits)
* Tamaño de los datos (8 bits)
* Tamaño de los datos de verificación (8 bits)
* Datos 
* Datos de verificación 
  
Cada vez que se hace referencia al tamaño, se hace referencia al tamaño en bytes de los datos y los datos de verificación.

Cada trama incluye una bandera en su inicio que es INIT BIT que está representado por el 2 que representa que comienza el envío de una trama.

Las computadoras leen el cable Duplex y echan a andar la máquina de estados que representa el funcionamiento de la lectura. Dicha máquina de estados tiene los siguientes estados:

0. No se ha recibido nada
1. Se recibió la bandera inicial y se comienza a recibir la MAC de destino
2. Se recibió la MAC de destino y se recibe la MAC de origen
3. Se recibió la MAC de origen y se recibe el tamaño en bytes de los datos.
4. Se recibió el tamaño de los datos, y se recibe el tamaño en bytes de los datos de verificación.
5. Se recibió el tamaño de los datos de verificación y se reciben los datos.
6. Se recibió los datos y se reciben los datos de verificación.

Note que en cualquiera de los estados si se recibe un 2, se toma que una nueva trama comienza por tanto se va al estado 1.

La información relacionada al funcionamiento del Switch se encuentra en [la documentación](devices.md)

