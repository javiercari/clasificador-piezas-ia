# Bitácora del proyecto

## Semana 1 - Encuadre y configuración del entorno

### Antes de la clase

Fui creando mi cuenta de github, cree mi repositorio y la carpetas, como bitaora,readme,etc.
Descargue la aplicacion de git bash.
Tambien aprendi a como hacer push, como trabajar en el cmd y como hacer commit.



**¿Cuál es la diferencia entre programar la regla y aprender la regla?** Si yo la programo le estoy diciendo a la computadora como hacerlo, en cambio si hago que aprenda yo le doy ejemplos y ella por si sola va a entender cual es la regla 

**¿Cuál es tu dominio y cuáles son tus tres tipos de pieza?** Tamaño(chico,mediano,grande)

**Describe el bucle de control de tu sistema:**
sensor ultrasónico HC-SR04,mide distancia entre él y la pieza. 
Dependiendo de la posición de la pieza, esa distancia permite determinar su altura/tamaño. 
Entrada:

Distancia = 6.7 cm

Salida del modelo:

MEDIANO

Después de que el modelo clasifique la pieza, un servomotor puede mover una compuerta para enviarla al lugar correspondiente.

Por ejemplo:

CHICO → servo mueve la compuerta hacia la izquierda.



**Dato**                                                               HC-SR04
**Tipo de salida**	                                                      Digital, por pulso (TTL)
**Rango de medición**	                                                         2 cm – 400 cm
**Tiempo de respuesta**	                                                 ≈ 60 ms entre mediciones recomendadas
**Voltaje de alimentación**	                                                        5 V DC

## Semana 2 - La primera señal del sensor (U1)

En mi equipo me toco medir la distancia, para esto utilizare el sensor ultrasonico, el cual investigando lo mejor seria ponerlo arriba para que cuando pase el objeto mida la presencia del objeto y depende la duracion de la señal se le da una distancia 

Salida: Digital, por pulso (TTL).

Tiene dos señales principales:

TRIG: entrada digital que recibe un pulso para iniciar la medición.
ECHO: salida digital por pulso. La duración del pulso indica la distancia al objeto.

Ejemplos de como se verian:

4.32
7.85
11.27

Que representarían, por ejemplo:

4.32 cm → objeto chico
7.85 cm → objeto mediano
11.27 cm → objeto grande

Python necesita recibir únicamente datos numéricos del sensor para poder procesarlos.

Si Arduino envía:

Serial.println("Leyendo...");

Python recibiría el texto:

Leyendo...

y no podría interpretarlo directamente como una distancia para entrenar o usar el modelo.

### Avance del proyecto

Aun vamos avanzando para poder ir viendo que se va a trabajar pero sabiendo las bases y herramientas que vamos a ocupar. Ya que aun no se sabe que haremos

ya logre hacer push a github

Este es el procedimiento para hacer push:

-Para hacer un push primero edito mi archivo
-luego hago git add .
luego git commit
luego git push

