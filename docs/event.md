# Documentación de la clase EventHook

La clase EventHook representa un evento, que puede ser lanzado utilizando el método `.fire()`. 

Dicha clase consta de una lista `handlers` donde se almacenan todos los métodos subscritos al evento. Para subscribir un método al evento basta con aplicar el operador `+=`.

Por ejemplo, supongamos se tiene el siguiente código:

```
def print_Hello():
    print("Hello", end=" ")

def print_World():
    print("World!")

evento = EventHook()
evento += print_Hello
evento += print_World

evento.fire()
```

Al ejecutar el código se muestra en pantalla la siguiente línea:

```
Hello World!
```

Pues se ejecutan todos los métodos que están en la lista `handlers` de `EventHook`. 

Un objeto `EventHook` puede tener varios métodos subscrito en `handlers`, y estos métodos devolver valores. El método `.fire()` devuelve el valor de `handlers[-1]`

Por ejemplo:

```
def ret_2():
    return 2
def ret_3():
    return 3

evento = EventHook()
evento += ret_2
evento += ret_3

print(evento.fire())

# SALIDA
# 3
```

## Necesidad de la clase `EventHook`

En nuestra modelación los dispositivos no tienen ciertas informaciones de la simulación, por ejemplo:
 
* signal time
* tiempo actual de la simulación, entre otros

Para acceder a estos datos, los dispositivos levantan un evento que pide los mismos, y luego utilizan el valor que devuelve el evento.




