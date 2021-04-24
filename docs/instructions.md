# Documentación de `Instructions` e `InstructionFactory`

Para la modelación de las instrucciones se tiene la siguiente jerarquía de clases:

![](./img/instruction.png)

Donde `Instruction` es una clase abstracta que tiene un método abstracto `.execute()`, el cual instancia una clase `Executor`  encargada de llevar a cabo la acción de la instrucción.

Cada clase heredera de `Instruction` almacena además los datos necesarios para su ejecución por ejemplo, la instucción `Send` almacena el nombre del dispositivo que debe enviar, y los datos a enviar.

Además, se tiene un método que devuelve la instancia de una instrucción, utilizando el patrón de diseño Factory. Para ello se tiene una jerarquía igual a la anterior con clases Factory's.

## `Executor`

Esta clase abstracta tiene acceso a la simulación y ejecuta las instrucciones. Se tiene una clase para cada instrucción.

