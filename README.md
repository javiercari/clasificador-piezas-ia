# Clasificador de piezas - Material

Proyecto del curso Inteligencia Artificial.

- Alumno: Javier Corona Arias
- Código: 220398647
- Dominio: clasificación por tamaño (chico,mediano,grande)

## Descripción

Sistema que lee señales de sensores mientras una pieza pasa frente a ellos,
clasifica de qué tipo es con un modelo de aprendizaje de máquina y acciona
un actuador para enrutarla. Crece semana a semana con los temas del curso:
adquisición, características, clasificación, anomalías y despliegue en PLC.




## Ficha Técnica del Dataset (`datos/features.csv`)

- **Total de ventanas/eventos registrados:** 4 ventanas en fase de desarrollo (3 de clase `grande`, 1 de clase `chica`).
- **Número de características por ventana:** 7 características estadísticas y temporales.
- **Lista de características:**
  1. `media`: Valor promedio de la distancia corregida por línea base.
  2. `desv`: Desviación estándar de las lecturas en la ventana.
  3. `minimo`: Caída máxima en cm registrada durante el paso de la pieza.
  4. `maximo`: Valor máximo de la lectura corregida.
  5. `rango`: Diferencia entre el pico máximo y mínimo (`maximo - minimo`).
  6. `energia`: Suma de los cuadrados de la señal corregida ($ \sum x^2 $).
  7. `duracion`: Cantidad de muestras temporales donde la pieza obstruye el sensor ($ |x| > 0.5 \text{ cm} $).
- **Identificadores:** `ventana` (índice de rastro de la señal) y `etiqueta` (clase objetivo: `chica`, `mediana`, `grande`).
- **Dominio de variables:** Señales puramente temporales (las características espectrales FFT fueron descartadas por no ser discriminantes).