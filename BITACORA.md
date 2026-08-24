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




### Avance del proyecto

Aun vamos avanzando para poder ir viendo que se va a trabajar pero sabiendo las bases y herramientas que vamos a ocupar. Ya que aun no se sabe que haremos

ya logre hacer push a github

Este es el procedimiento para hacer push:

-Para hacer un push primero edito mi archivo
-luego hago git add .
luego git commit
luego git push
