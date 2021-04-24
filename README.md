# Net-Sim

El simulador de una red de computadoras que se presenta cuenta con la implementación de las siguientes capas:

* **Capa Física (host, hub, y cables coaxiales):** cuando un host escribe revisa el estado del canal de comunicación y solo escribe si este está vacío. Cuando se realizan conexiones entonces se revisan si ocurren colisiones y se toma la decisión de detener el envío de información de uno de los host que envía.
* **Capa de Enlace (switch, cables duplex, frame):** la red que se simula es _full duplex_. Se envían frames desde un host a otro, utilizando los switch para facilitar dicho proceso. Cuando un host envía información a un switch, este último almacena los datos hasta tener la información de a que MAC debe enviar los datos.
* **Capa de Enlace (detección y corrección de errores):** cada frame transporta información relacionada con el dato que se envía, se implementaron tres algoritmos: Hash Sum (`hash-sum`), Bit de Paridad (`parity`) y CRC16 (`crc-16`).

## Añadir configuraciones

En el archivo `config.txt` se escribe en formato `.json` las configuraciones. Hasta el momento se tienen 3 posibles configuraciones:

* **Nombre del script de instrucciones:** `script-name` que por defecto es `script.txt`.
* **Signal time:** `signal-time` tiempo en milisegundos (ms) que debe mantenerse un bit en el cable. Por defecto, debe estar configurado en 10 ms
* **Algoritmo de detección de errores:** `error-detection`. Las opciones posibles son: Hash Sum (`hash-sum`), Bit de Paridad (`parity`) y CRC16 (`crc-16`).

## Ejecución

Se incluye un archivo Makefile que realiza el proceso de ejecución del proyecto por tanto, basta escribir en la terminal de Linux el comando `make`.

Se adjunta el contenido del Makefile:

```
run: 
	if test -d output; then rm -rf "./output"; fi	
	mkdir output
	python main.py
```

La carpeta `./output/` se crea de forma dinámica cuando se ejecuta el proyecto.

Debe crearse el archivo de nombre `script.txt` para las instrucciones a simular. En caso de definir otro archivo, configurarlo en `config.txt`.

## Integrantes

* Ariel Alfonso Triana Pérez C-311
* Carlos Toledo Silva C-311