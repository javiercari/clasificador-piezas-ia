
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# 1. Definir rutas relativas al proyecto
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
ruta_features = os.path.join(carpeta_proyecto, 'datos', 'features.csv')
ruta_modelo = os.path.join(carpeta_proyecto, 'modelo.pkl')
ruta_figura_cm = os.path.join(carpeta_proyecto, 'figuras', 'confusion.png')

os.makedirs(os.path.join(carpeta_proyecto, 'figuras'), exist_ok=True)

if not os.path.exists(ruta_features):
    print(f"No se encontró {ruta_features}. Ejecuta primero features.py.")
    exit()

features = pd.read_csv(ruta_features)

X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']

# Partición de datos adaptativa para fase de desarrollo y dataset completo ($N=90$)
if len(features) >= 6 and len(y.unique()) > 1:
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.25,
            stratify=y,        # Misma proporción de clases en ambas partes
            random_state=42   # Semilla para repetibilidad
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )
else:
    # Muestras iniciales de prueba
    X_train, X_test, y_train, y_test = X, X, y, y

# Estandarización: fit_transform en train, transform en test
escalador = StandardScaler()
X_train_esc = escalador.fit_transform(X_train)
X_test_esc  = escalador.transform(X_test)

# Definir k-NN (k=5 para el dataset completo o adaptable para pruebas cortas)
n_vecinos = min(5, len(X_train)) if len(X_train) >= 5 else max(1, len(X_train))
modelo = KNeighborsClassifier(n_neighbors=n_vecinos)
modelo.fit(X_train_esc, y_train)

y_pred = modelo.predict(X_test_esc)

clases_ordenadas = sorted(y.unique())
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=clases_ordenadas)

print(f"Exactitud: {acc * 100:.2f}%")
print()
print("Matriz de confusión:")
print(cm)
print("Clases en ese orden:", clases_ordenadas)

# El escalador se guarda junto al modelo y las columnas: sin ellos el modelo no sirve en producción
joblib.dump(
    {
        'modelo': modelo,
        'escalador': escalador,
        'columnas': list(X.columns)
    },
    ruta_modelo
)
print(f"\nGuardado en {ruta_modelo}")

# TODO RESUELTO: Graficar la matriz de confusión y guardarla en figuras/confusion.png
fig, ax = plt.subplots(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clases_ordenadas)
disp.plot(cmap=plt.cm.Blues, ax=ax, values_format='d')
plt.title('Matriz de Confusión - k-NN')
plt.savefig(ruta_figura_cm, dpi=300, bbox_inches='tight')
plt.close()

print(f"Matriz de confusión guardada en: {ruta_figura_cm}")