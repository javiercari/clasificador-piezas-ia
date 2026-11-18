# pca_3d.py - reduce las caracteristicas a tres componentes y las grafica en 3D
import os

# Limitar hilos de OpenBLAS antes de importar librerias numericas (evita error de memoria en Windows)
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Definir rutas relativas al proyecto
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
ruta_features = os.path.join(carpeta_proyecto, 'datos', 'features.csv')
ruta_figura = os.path.join(carpeta_proyecto, 'figuras', 'pca_3d.png')

os.makedirs(os.path.join(carpeta_proyecto, 'figuras'), exist_ok=True)

features = pd.read_csv(ruta_features)
X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']          # NO se usa para calcular el PCA, solo para colorear

# Estandarización obligatoria antes de PCA
X_esc = StandardScaler().fit_transform(X)

# Reducir a 3 componentes principales
pca = PCA(n_components=3)
componentes = pca.fit_transform(X_esc)

var_pc1 = pca.explained_variance_ratio_[0] * 100
var_pc2 = pca.explained_variance_ratio_[1] * 100
var_pc3 = pca.explained_variance_ratio_[2] * 100
var_total = pca.explained_variance_ratio_.sum() * 100

print("Varianza explicada por cada componente:", pca.explained_variance_ratio_)
print(f"Varianza acumulada de las tres: {var_total:.2f}%")

# Crear figura y eje en 3D
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')

for clase in sorted(y.unique()):
    mascara = (y == clase)
    ax.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        componentes[mascara, 2],
        label=clase,
        s=80,
        alpha=0.85,
        edgecolors='black'
    )

# Etiquetar cada punto con su número de ventana en el espacio 3D
for i, vent in enumerate(features['ventana']):
    ax.text(
        componentes[i, 0],
        componentes[i, 1],
        componentes[i, 2],
        f" v{vent}",
        fontsize=8,
        alpha=0.75
    )

ax.set_xlabel(f"PC1 ({var_pc1:.2f}%)")
ax.set_ylabel(f"PC2 ({var_pc2:.2f}%)")
ax.set_zlabel(f"PC3 ({var_pc3:.2f}%)")
ax.set_title(f"Proyección PCA 3D del Dataset (Varianza acumulada: {var_total:.2f}%)")
ax.legend(title="Clase")

# Guardar imagen y abrir ventana interactiva
plt.savefig(ruta_figura, dpi=300, bbox_inches='tight', pad_inches=0.35)
print(f"Gráfica 3D guardada en: {ruta_figura}")
plt.show()