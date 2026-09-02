# codigo/adquirir.py - Captura ventanas etiquetadas y las guarda en datos/datos.csv
import os
import csv
import time
import serial
import pandas as pd

PUERTO = 'COM4'         
BAUDIOS = 115200
N_MUESTRAS = 200          # Largo de cada ventana
ARCHIVO = 'datos/datos.csv'

# Asegurar que el directorio datos/ exista
os.makedirs('datos', exist_ok=True)

etiqueta = input("Etiqueta de esta pieza (chica, mediana, grande): ").strip().lower()
n_ventanas = int(input("Cuántas ventanas vas a capturar en esta sesión: "))

# -------------------------------------------------------------
# TODO 1 y 2: CONTROL DE ENCABEZADOS Y NÚMERO DE VENTANA
# -------------------------------------------------------------
archivo_existe = os.path.exists(ARCHIVO)
archivo_vacio = not archivo_existe or os.path.getsize(ARCHIVO) == 0

# Averiguar en qué número de ventana nos quedamos la última vez
ventana_inicial = 0
if archivo_existe and not archivo_vacio:
    try:
        df_existente = pd.read_csv(ARCHIVO)
        if 'ventana' in df_existente.columns and not df_existente.empty:
            ventana_inicial = int(df_existente['ventana'].max()) + 1
    except Exception as e:
        print(f"Nota: No se pudo leer el archivo existente ({e}). Se iniciará ventana en 0.")

# Abrir en modo append ('a') para no borrar lo capturado anteriormente
archivo = open(ARCHIVO, 'a', newline='')
escritor = csv.writer(archivo)

# Si el archivo es nuevo o está vacío, escribir primero la fila de encabezados
if archivo_vacio:
    escritor.writerow(['ventana', 't', 'valor', 'etiqueta'])

# -------------------------------------------------------------
# CONEXIÓN SERIAL Y CAPTURA
# -------------------------------------------------------------
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)  # Esperar reinicio de Arduino

ventana = ventana_inicial
for i in range(n_ventanas):
    input(f"\nVentana {ventana} ({etiqueta}). Presiona Enter y pasa la pieza...")
    ser.reset_input_buffer()  # Limpia muestras viejas acumuladas en la espera
    
    t = 0
    while t < N_MUESTRAS:
        linea = ser.readline().decode('utf-8', errors='ignore').strip()
        try:
            valor = float(linea)
        except ValueError:
            continue
            
        escritor.writerow([ventana, t, valor, etiqueta])
        t += 1

    print(f"  {N_MUESTRAS} muestras guardadas correctamente para la ventana {ventana}.")
    ventana += 1

archivo.close()
ser.close()
print(f"\n¡Listo! Captura completada y datos guardados en {ARCHIVO}")