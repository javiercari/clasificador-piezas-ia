# evaluar_red.py - Compara k-NN / Arbol con Redes Neuronales (MLPClassifier)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import os

# 1. Ubicar datos
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
ruta_features = os.path.join(carpeta_proyecto, 'datos', 'features.csv')

if not os.path.exists(ruta_features):
    print(f"No se encontro {ruta_features}. Ejecuta primero features.py.")
    exit()

df = pd.read_csv(ruta_features)

# Seleccionar caracteristicas y etiqueta
columnas_x = [col for col in df.columns if col not in ['ventana', 'etiqueta']]
X = df[columnas_x]
y = df['etiqueta']

# Dividir dataset si hay suficientes datos, o evaluar el conjunto disponible
if len(df) >= 6:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
else:
    X_train, X_test, y_train, y_test = X, X, y, y

# Estandarizacion obligatoria para Redes Neuronales
scaler = StandardScaler()
X_train_esc = scaler.fit_transform(X_train)
X_test_esc = scaler.transform(X_test)

# Definir modelos
modelos = {
    'El tuyo de la semana 7 (k-NN)': KNeighborsClassifier(n_neighbors=min(3, len(X_train))),
    'Red (10 neuronas)': MLPClassifier(hidden_layer_sizes=(10,), max_iter=2000, random_state=42),
    'Red (50 neuronas)': MLPClassifier(hidden_layer_sizes=(50,), max_iter=2000, random_state=42)
}

print("==================================================")
print("     COMPARACION DE MODELOS (SEMANA 8)")
print("==================================================\n")

resultados = []

for nombre, modelo in modelos.items():
    modelo.fit(X_train_esc, y_train)
    
    pred_train = modelo.predict(X_train_esc)
    pred_test = modelo.predict(X_test_esc)
    
    acc_train = accuracy_score(y_train, pred_train) * 100
    acc_test = accuracy_score(y_test, pred_test) * 100
    
    resultados.append({
        'Modelo': nombre,
        'Exactitud train': f"{acc_train:.1f}%",
        'Exactitud test': f"{acc_test:.1f}%"
    })

df_res = pd.DataFrame(resultados)
print(df_res.to_string(index=False))