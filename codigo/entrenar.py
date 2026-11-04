# entrenar.py - Preparación de X, y, partición train/test y entrenamiento base (Semana 7 Bloque 1)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import os

# 1. Cargar dataset de características
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
ruta_features = os.path.join(carpeta_proyecto, 'datos', 'features.csv')

if not os.path.exists(ruta_features):
    print(f"No se encontró {ruta_features}. Ejecuta primero features.py.")
    exit()

df = pd.read_csv(ruta_features)

# 2. Separar características (X) y vector de etiquetas (y)
# Se eliminan 'ventana' (identificador) y 'etiqueta' (variable objetivo)
X = df.drop(columns=['ventana', 'etiqueta'])
y = df['etiqueta']

print(f"Dataset cargado: {X.shape[0]} ejemplos, {X.shape[1]} características.")

# 3. Partición estratificada (Train / Test)
if len(df) >= 6:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
else:
    # Para datasets pequeños en desarrollo, usar partición funcional
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

# 4. Estandarización de características (Crucial para k-NN)
scaler = StandardScaler()
X_train_esc = scaler.fit_transform(X_train)
X_test_esc = scaler.transform(X_test)

# 5. Modelo baseline: Árbol de Decisión
arbol = DecisionTreeClassifier(max_depth=3, random_state=42)
arbol.fit(X_train, y_train)

acc_train = accuracy_score(y_train, arbol.predict(X_train)) * 100
acc_test = accuracy_score(y_test, arbol.predict(X_test)) * 100

print(f"\n--- Modelo Inicial: Árbol de Decisión ---")
print(f"Exactitud Entrenamiento: {acc_train:.1f}%")
print(f"Exactitud Prueba (Test): {acc_test:.1f}%")