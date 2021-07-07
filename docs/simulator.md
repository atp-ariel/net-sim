# Documentación de `Simulator`

La clase `Simulator` representa la estructura encargada de llevar a cabo la simulación de la red. Para ello, se tienen los siguientes campos:


* `simulation_time` tiempo actual de la simulación en milisegundos
* `signal_time`
* `instructions` todas las instucciones que están en `script.txt`
* `pending` instrucciones pendientes
* `sending_device` dispositivos  que están enviando en ese momento.
* `time_instruction` instrucciones que deben ser ejecutadas en esa instancia de tiempo.

Esta clase es la que responde a todos los eventos que se levantan en otras clases, como `.askForSignalTime`, `.consultDevice`, `.sendEvent`, entre otros.

## Singleton de la clase Simulator

Se necesita tener una sola instancia de la clase Simulator, y que sea accesible desde distintos puntos del proyecto. Para esto se emplea el patrón de diseño Singleto.

## Storage Device

La clase `Storage_Device` representa el almacen de los dispositvos y network-component que pertenecen a la red. 

* `devices` lista de todos los dispositivos en la simulación.
* `deviceMap` diccionario donde dado un nombre del dispositivo se obtiene el índice de dicho dispositivo en la lista `device`.
* `subred` diccionario donde la llave es el ip de la subred y el valor es una lista de dispositivos. 

Además se implementa el patrón Singleton en esta clase.
