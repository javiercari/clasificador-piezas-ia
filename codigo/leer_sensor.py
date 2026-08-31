# leer_sensor_simulado.py - Estructura orientada a void loop()
import os
import time
import random
import matplotlib.pyplot as plt


PUERTO = 'COM4'
BAUDIOS = 115200
N_MUESTRAS_VENTANA = 200  

DISTANCIA_REPOSO = 30.0  # cm (Banda sin pieza)
ALTURA_PIEZA = 15.0      # cm (Altura de la pieza)

# -------------------------------------------------------------
# SIMULACIÓN DEL HARDWARE
# -------------------------------------------------------------
def leer_sensor_ultrasonico():
    """
    Simula la función que lee el puerto serial dentro del loop.
    En hardware real esta función equivale a:
    linea = ser.readline().decode('utf-8').strip()
    """
    time.sleep(0.01)  # Simula el delay(10) del Arduino
    
    evento periódico de paso de pieza
    t = time.time() % 6  # Ciclo de 6 segundos
    if 2.0 <= t <= 4.0:
        distancia = DISTANCIA_REPOSO - ALTURA_PIEZA  # Pieza presente (~15 cm)
    else:
        distancia = DISTANCIA_REPOSO                 # Reposo (~30 cm)
        
    ruido = random.gauss(0, 0.4)
    return round(distancia + ruido, 2)

# -------------------------------------------------------------
# VOID SETUP()
# -------------------------------------------------------------
def setup():
    print(f"Iniciando comunicación en {PUERTO} a {BAUDIOS} baudios...")
    # ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
    # time.sleep(2)
    print("Sistema listo. Presiona Ctrl+C para salir.\n")

# -------------------------------------------------------------
# VOID LOOP()
# -------------------------------------------------------------
def loop():
    valores_ventana = []
    print("Muestreando en tiempo real...")

    # Bucle infinito q
    while True:
        # 1. Leer el dato del puerto 
        lectura_raw = str(leer_sensor_ultrasonico())

        # 2. Convertir y filtrar basura (try / except)
        try:
            valor = float(lectura_raw)
        except ValueError:
            continue  # Descarta lecturas corruptas

        # 3. Procesar valor en tiempo real
        valores_ventana.append(valor)
        print(f"Sensor: {valor} cm | Muestras acumuladas: {len(valores_ventana)}/{N_MUESTRAS_VENTANA}")

        # 4. Cuando la ventana se llena, guardamos/graficamos y reiniciamos
        if len(valores_ventana) >= N_MUESTRAS_VENTANA:
            print("\n¡Ventana de 200 muestras completada!")
            graficar_y_guardar(valores_ventana)
            
            # Limpiamos la ventana para seguir leyendo en el siguiente 'loop'
            valores_ventana = []
            print("\nReiniciando captura para el siguiente evento...\n")

# -------------------------------------------------------------
# FUNCIÓN AUXILIAR DE GRAFICACIÓN
# -------------------------------------------------------------
def graficar_y_guardar(datos):
    plt.figure(figsize=(10, 5))
    plt.plot(datos, color='#2ca02c', linewidth=1.8, label='Distancia (cm)')
    
    plt.gca().invert_yaxis()  # Invierte eje para ver la pieza hacia arriba
    plt.title('Ventana de Señal Continuo (Loop)', fontsize=14, fontweight='bold')
    plt.xlabel('Número de Muestra', fontsize=12)
    plt.ylabel('Distancia al Sensor (cm)', fontsize=12)
    plt.axhline(y=DISTANCIA_REPOSO, color='r', linestyle='--', alpha=0.5, label='Nivel Reposo')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    os.makedirs('../figuras', exist_ok=True)
    ruta_guardado = '../figuras/senal.png'
    plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {ruta_guardado}")
    
    plt.show()  # Muestra la ventana capturada

# -------------------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# -------------------------------------------------------------
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")