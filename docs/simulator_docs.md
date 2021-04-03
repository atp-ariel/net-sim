# Documentación de `Simulator`

La clase `Simulator` representa la estructura encargada de llevar a cabo la simulación de la red. Para ello, se tienen los siguientes campos:

* `devices` lista de todos los dispositivos en la simulación.
* `deviceMap` diccionario donde dado un nombre del dispositivo se obtiene el índice de dicho dispositivo en la lista `device`.
* `simulation_time` tiempo actual de la simulación en milisegundos
* `signal_time`
* `instructions` todas las instucciones que están en `script.txt`
* `pending` instrucciones pendientes
* `sending_device` dispositivos  que están enviando en ese momento.
* `time_instruction` instrucciones que deben ser ejecutadas en esa instancia de tiempo.

Esta clase es la que responde a todos los eventos que se levantan en otras clases, como `.askForSignalTime`, `.consultDevice`, `.sendEvent`, entre otros.
