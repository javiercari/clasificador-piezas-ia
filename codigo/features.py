# features.py - convierte cada ventana en una fila de caracteristicas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================================================
# 1. UBICACIÓN DE ARCHIVOS
# ==================================================
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

carpeta_datos = os.path.join(carpeta_proyecto, 'datos')
carpeta_figuras = os.path.join(carpeta_proyecto, 'figuras')

ruta_entrada = os.path.join(carpeta_datos, 'datos_limpios.csv')
ruta_salida = os.path.join(carpeta_datos, 'features.csv')
ruta_figura = os.path.join(carpeta_figuras, 'features.png')

os.makedirs(carpeta_figuras, exist_ok=True)

# ==================================================
# 2. LEER DATOS LIMPIOS
# ==================================================
if not os.path.exists(ruta_entrada):
    print(f"No se encontro {ruta_entrada}. Ejecuta primero limpiar.py.")
    exit()

datos = pd.read_csv(ruta_entrada)

# Umbral en cm de desviacion para detectar la presencia de la pieza
UMBRAL = 0.5 

filas = []

# ==================================================
# 3. EXTRAER CARACTERÍSTICAS POR VENTANA
# ==================================================
for ventana, g in datos.groupby('ventana'):
    # Usamos la señal corregida por linea base
    x = g['valor_corregido'].values
    etiqueta = g['etiqueta'].iloc[0]

    fila = {
        'ventana':  ventana,
        'media':    x.mean(),
        'desv':     x.std(),
        'minimo':   x.min(),
        'maximo':   x.max(),
        'rango':    x.max() - x.min(),
        'energia':  np.sum(x**2),
        # TODO 1: duracion del evento (muestras por encima del umbral)
        'duracion': np.sum(np.abs(x) > UMBRAL),
        'etiqueta': etiqueta,
    }
    filas.append(fila)

features = pd.DataFrame(filas)

# ==================================================
# 4. GUARDAR DATASET DE CARACTERÍSTICAS (TODO 3)
# ==================================================
features.to_csv(ruta_salida, index=False)

print("======================================")
print("     CARACTERÍSTICAS EXTRAÍDAS")
print("======================================")
print(features.head())
print("\nResumen por clase:")
print(features.groupby('etiqueta').size())
print(f"\nDatos guardados en: {ruta_salida}")

# ==================================================
# 5. DIAGRAMA DE DISPERSIÓN (3 PARES DE FEATURES)
# ==================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

pares = [
    ('rango', 'duracion'),
    ('desv', 'minimo'),
    ('energia', 'duracion')
]

for ax, (fx, fy) in zip(axes, pares):
    for etiqueta, g in features.groupby('etiqueta'):
        ax.scatter(g[fx], g[fy], label=etiqueta, s=120)
    ax.set_xlabel(fx)
    ax.set_ylabel(fy)
    ax.set_title(f'{fx} vs {fy}')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig(ruta_figura, dpi=300, bbox_inches='tight')
plt.close()

print(f"Grafica guardada en: {ruta_figura}")