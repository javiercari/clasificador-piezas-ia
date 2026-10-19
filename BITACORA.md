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

## Semana 2 - La primera señal del sensor (U1)
### Antes de la clase

#### BLOQUE 1

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

#### BLOQUE 2

¿Cuánto tarda tu pieza en cruzar frente al sensor?
Tiempo estimado: 0.6 segundos (600 ms).

Con ese tiempo, ¿qué delay() eliges para tener al menos 20 muestras del evento?**
   delay(10) en Arduino (da lecturas cada 10 ms / 100 Hz).
   Justificación: Para obtener al menos 20 muestras en 600 ms, requiero un intervalo máximo de 30 ms por muestra ($600\text{ ms} / 20 = 30\text{ ms}$). Use delay(10) para ir bien sobrado dentro del límite técnico del sensor HC-SR04 (~60 ms por eco).

   ¿Cuántas muestras te da eso mientras la pieza pasa?
   60 muestras aproximadamente durante el evento completo ($600\text{ ms} / 10\text{ ms} = 60\text{ muestras}$). 

### Avance del proyecto

Compre el sensor ultrasonico y cada miembro del equipo compro el suyo 



## Semana 3- Recolección de datos etiquetados (U2)
### Antes de la clase

#### BLOQUE 1

**Estructura de las columnas de `datos/datos.csv`:**

   `ventana`: ID del evento completo (pasada de la pieza frente al sensor).
   `t`: Tiempo o contador de muestra dentro del evento (de 0 en adelante).
   `valor`: Distancia en cm medida por el sensor ultrasónico (HC-SR04).
   `etiqueta`: Tamaño de la pieza identificado manualmente.

 **Etiquetas de tamaño (en minúsculas y sin acentos):**
  * `chica`
  * `mediana`
  * `grande`

 **Ejemplo de 5 filas de la tabla (Paso de una pieza mediana frente al ultrasónico):**

  ```python
  ventana,t,valor,etiqueta
  0,0,30.15,mediana
  0,1,30.02,mediana
  0,2,16.20,mediana
  0,3,15.95,mediana
  0,4,29.88,mediana
```

#### Bloque 2 


  ### Protocolo de recolección de datos

**Ventanas por clase:** Se capturarán **30 ventanas por clase** (90 ventanas en total para `chica`, `mediana` y `grande`), asegurando un dataset perfectamente balanceado.
* **Orden de captura:** Las pasadas se realizarán de manera estrictamente **alternada** (`chica` -> `mediana` -> `grande` -> `chica`...), evitando capturar un tipo de pieza por bloques para prevenir que la fatiga o los cambios térmicos del sensor se asocien a una sola etiqueta.
* **Control de velocidad:**
  * Se pegará sobre la mesa una cinta adhesiva de **30 cm de longitud** indicando el punto exacto de inicio y fin del recorrido.
  * Se marcará el ritmo con un metrónomo a $60\text{ BPM}$ para completar cada pasado en **exactamente 1 segundo** ($0.6\text{ s}$ de detección efectiva frente al sensor).
* **Geometría del montaje:** La pieza pasará rozando la mesa a una distancia fija de **30 cm del sensor ultrasónico** (en reposo), manteniéndose alineada 

## Semana 4-Limpieza y normalización de señales (U2)
### Antes de la clase

#### Bloque 1

Se me complico un poco iniciarla ya que tuve que revisar otra vez mi bitacora por que como que algo estaba mal en mi semana 3, un compañero me ayudo para comparar lo suyo con lo mio y me di cuenta que estaba bien.
Ya despues de esto el sensor lo quise probar y el echo no estaba funcionando bien, lo probe varias veces y al parecer ya no funciona, asi que use otro que traia de repuesto, todo esto me quito mucho tiempo.
Ya cuando quise iniciar el bloque 1 ya no tenia tiempo y no pude crear el archivo de limpiar.py

En la clase de hoy se resolvieron dudas, se explico acerca del que tiene que ver el promedio en los datos que da el sensor, se reitero la diferencia entre muestras y ventanas, y acerca de los valores maximos y minimos .

**Qué tipo de ruido ves en tu señal y de dónde crees que viene?**

Veo un ruido aleatorio de alta frecuencia (como si la línea estuviera vibrando un poco), que creo que viene de las vibraciones del motor de la banda y variaciones de la fuente de alimentación. También salen valores atípicos (picos raros de 0 o mayores a 400 cm), que ocurren cuando el ultrasonido rebota mal en la pieza o se le agota el tiempo de espera al sensor.

**Qué rango físico tiene tu sensor y qué valores estás descartando por imposibles?**

El sensor ultrasónico (HC-SR04) mide de 2 a 400 cm. Descarté cualquier lectura menor o igual a 0 cm y mayor a 400 cm porque son físicamente imposibles en la banda y solo representan errores de medición o lecturas perdidas.

**Qué tamaño de filtro elegiste y por qué, en relación con la duración de tu evento?**

Elegí un filtro de media móvil con ventana de 5 muestras. Como el evento de la pieza dura alrededor de 200 muestras, un filtro de 5 es bastante chico: alcanza a suavizar la vibración sin aplanar los picos ni deformar la altura, por lo que se sigue notando bien la diferencia entre pieza chica, mediana y grande.


#### BLOQUE 2

**Cuánto se movió tu línea base entre la primera y la última ventana de la sesión?**
Entre la primera ventana (ventana 0) y la última (ventana 3), la línea base en reposo pasó de 11.72 cm a 11.73 cm. El movimiento total de la línea base fue de 0.00 cm (variación exacta de 0.0044 cm), lo que indica que el valor de reposo se mantuvo casi idéntico a lo largo de la prueba.

**¿Qué normalización elegiste y por qué?**
Elegí la normalización Min-Max (que escala todas las lecturas al rango de 0 a 1). La elegí porque en los pasos previos ya habíamos eliminado los valores atípicos fuera del rango físico del sensor (0 a 400 cm). Al no tener picos absurdos o ruido extremo que pudieran aplastar la gráfica, Min-Max es ideal porque mantiene las proporciones de la pieza y deja todas las ventanas listas para compararse en una misma escala de 0 a 1.

**Al comparar antes y después: ¿se parecen más entre sí las ventanas de una misma clase?**
Sí, se parecen mucho más. Antes de procesar los datos, las ventanas de la misma clase tenían pequeñas variaciones en la distancia de reposo y en la amplitud por la vibración del sensor. Después de restar la línea base y aplicar Min-Max, todas las ventanas de una misma clase inician exacto en 0 y alcanzan su pico en 1, logrando que los perfiles de la señal para piezas chicas, medianas o grandes tengan formas mucho más uniformes.

#### Correcion de REVISION.md

En la semana 4 ya esta todo agregado en bitacora y ya estan los archivos que se piden, que era lo que me pidio en la revision.
Tambien corregi la estructura de bitacora.


## Semana 5
### Antes de la clase 

| Característica | Justificación para clasificación de tamaño con sensor ultrasónico |
| :--- | :--- |
| **Duración del evento** | Mide cuántas muestras tarda la pieza en pasar bajo el sensor. Una pieza grande o larga mantiene el sensor obstruido por más tiempo (más muestras) que una chica. |
| **Mínimo (`min`)** | El ultrasónico mide distancia. Cuando pasa una pieza alta, la distancia disminuye; por lo tanto, el mínimo indica qué tan alta es la pieza (a mayor altura, menor distancia registrada). |
| **Rango (`max - min`)** | Mide la diferencia entre la distancia de reposo (banda vacía) y la parte más alta de la pieza, representando directamente la altura física del objeto. |
| **Energía ($\sum x^2$)** | Combina la altura de la pieza con el tiempo que tarda en pasar. Una pieza grande tendrá mayor energía acumulada durante el evento. |
| **Media (`mean`)** | Promedia la desviación de la distancia durante la ventana. Piezas más grandes reducen más el promedio de la distancia leída. |
| **Desviación Estándar (`std`)** | Mide la variabilidad de la lectura. Muestra la diferencia entre la zona llana de la banda y el perfil que sobresale de la pieza. |

#### Predicción de características

La mejor característica será: La duración del evento. Debido a que la banda avanza a velocidad constante, la longitud física de la pieza se refleja directamente en el número de muestras que dura la caída de distancia.
 
 La característica más inútil será: La media. Al promediar toda la ventana (incluyendo las lecturas de reposo antes y después de que pase la pieza), la información del tamaño real se diluye y puede confundir piezas de distintas proporciones.


