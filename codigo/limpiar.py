import pandas as pd

# 1. Cargar el dataset original
datos = pd.read_csv('datos/datos.csv')

# 2. TODO 1: Eliminar valores atípicos fuera del rango físico del ultrasónico
# Si tus datos están en centímetros, el rango real del sensor suele ser entre 2 y 400 cm.
# Ajusta MIN_RANGO y MAX_RANGO según cómo registres la distancia en tu banda.
MIN_RANGO = 2.0
MAX_RANGO = 400.0

datos = datos[(datos['valor'] >= MIN_RANGO) & (datos['valor'] <= MAX_RANGO)].copy()

# 3. TODO 2 y 3: Aplicar el filtro de media móvil por ventana y manejar NaNs
# Definimos una función interna para filtrar una sola ventana
def aplicar_filtro_media_movil(serie):
    # center=True centra el promedio en la muestra actual
    # min_periods=1 evita generar NaNs en las orillas promediando con los datos disponibles
    return serie.rolling(window=5, center=True, min_periods=1).mean()

# Aplicamos el filtro manteniendo el aislamiento por ventana con groupby
datos['valor_filtrado'] = datos.groupby('ventana')['valor'].transform(aplicar_filtro_media_movil)

# 4. Guardar los datos limpios para el siguiente bloque
datos.to_csv('datos/datos_limpios.csv', index=False)

print("Limpieza completada exitosamente. Se generó 'datos/datos_limpios.csv'.")