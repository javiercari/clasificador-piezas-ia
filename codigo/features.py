# features.py - Extracción de características temporales y espectrales (Semana 6 Bloque 2)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================================================
# 1. RUTAS Y CONFIGURACIÓN
# ==================================================
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

carpeta_datos = os.path.join(carpeta_proyecto, 'datos')
carpeta_figuras = os.path.join(carpeta_proyecto, 'figuras')

ruta_entrada = os.path.join(carpeta_datos, 'datos_limpios.csv')
ruta_salida = os.path.join(carpeta_datos, 'features.csv')
ruta_figura_espectro = os.path.join(carpeta_figuras, 'espectro.png')
ruta_figura_disp_esp = os.path.join(carpeta_figuras, 'features_espectro.png')

os.makedirs(carpeta_datos, exist_ok=True)
os.makedirs(carpeta_figuras, exist_ok=True)

if not os.path.exists(ruta_entrada):
    print(f"No se encontró {ruta_entrada}. Ejecuta primero limpiar.py.")
    exit()

datos = pd.read_csv(ruta_entrada)

FS = 100.0   # Frecuencia de muestreo (100 Hz)
UMBRAL = 0.5 # Umbral en cm para detectar paso de objeto

filas = []

plt.figure(figsize=(10, 5))

for ventana, g in datos.groupby('ventana'):
    x = g['valor_corregido'].values
    etiqueta = g['etiqueta'].iloc[0]

    # --- CARACTERÍSTICAS EN EL TIEMPO ---
    media = x.mean()
    desv = x.std()
    val_min = x.min()
    val_max = x.max()
    rango = val_max - val_min
    energia_tiempo = np.sum(x**2)
    duracion = np.sum(np.abs(x) > UMBRAL)

    # --- CARACTERÍSTICAS EN FRECUENCIA (FFT) ---
    espectro = np.abs(np.fft.rfft(x))[1:]  # Se elimina la componente DC (0 Hz)
    frecuencias = np.fft.rfftfreq(len(x), 1/FS)[1:]

    f_dominante = frecuencias[np.argmax(espectro)]
    centroide = np.sum(frecuencias * espectro) / np.sum(espectro)
    
    # TODO 1: Energía espectral total
    e_espectral = np.sum(espectro**2)
    
    # TODO 2: Energía por bandas (Baja: 0-10 Hz, Alta: 10-50 Hz)
    banda_baja = np.sum(espectro[(frecuencias >= 0) & (frecuencias < 10)]**2)
    banda_alta = np.sum(espectro[(frecuencias >= 10) & (frecuencias <= 50)]**2)

    # Graficar espectro de la ventana
    plt.plot(frecuencias, espectro, label=f'Ventana {ventana} ({etiqueta})')

    fila = {
        'ventana': ventana,
        'media': media,
        'desv': desv,
        'minimo': val_min,
        'maximo': val_max,
        'rango': rango,
        'energia': energia_tiempo,
        'duracion': duracion,
        'f_dominante': f_dominante,
        'centroide': centroide,
        'e_espectral': e_espectral,
        'banda_baja': banda_baja,
        'banda_alta': banda_alta,
        'etiqueta': etiqueta
    }
    filas.append(fila)

plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud del Espectro')
plt.title('Espectro de Frecuencia (FFT) por Ventana de Evento')
plt.legend()
plt.grid(True)
plt.savefig(ruta_figura_espectro, dpi=300, bbox_inches='tight')
plt.close()

features_full = pd.DataFrame(filas)

# Graficar dispersión para verificar separabilidad
plt.figure(figsize=(7, 5))
for etiqueta, g in features_full.groupby('etiqueta'):
    plt.scatter(g['duracion'], g['f_dominante'], label=etiqueta, s=120)
plt.xlabel('Duración (Tiempo)')
plt.ylabel('Frecuencia Dominante (Hz)')
plt.title('Separación de Clases: Duración vs Frecuencia Dominante')
plt.legend()
plt.grid(True)
plt.savefig(ruta_figura_disp_esp, dpi=300, bbox_inches='tight')
plt.close()

# DECISIÓN: Las características espectrales no discriminan bien eventos de paso de piezas,
# por lo que guardamos en features.csv únicamente las características temporales útiles.
features_final = features_full[['ventana', 'media', 'desv', 'minimo', 'maximo', 'rango', 'energia', 'duracion', 'etiqueta']]
features_final.to_csv(ruta_salida, index=False)

print("======================================")
print("     FEATURES CALCULADAS Y GUARDADAS")
print("======================================")
print(features_full[['ventana', 'rango', 'duracion', 'f_dominante', 'centroide', 'etiqueta']])
print(f"\nEspectro guardado en: {ruta_figura_espectro}")
print(f"Dispersión guardada en: {ruta_figura_disp_esp}")
print(f"features.csv actualizado en: {ruta_salida}")