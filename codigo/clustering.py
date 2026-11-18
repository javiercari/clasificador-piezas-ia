# clustering.py - agrupa el dataset sin usar las etiquetas
import os

# Limitar hilos de OpenBLAS antes de importar librerias numericas (evita error de memoria en Windows)
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Definir rutas relativas al proyecto
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
ruta_features = os.path.join(carpeta_proyecto, 'datos', 'features.csv')
ruta_figura = os.path.join(carpeta_proyecto, 'figuras', 'clustering.png')

os.makedirs(os.path.join(carpeta_proyecto, 'figuras'), exist_ok=True)

features = pd.read_csv(ruta_features)
X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']            # solo para comparar al final

X_esc = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
grupos = kmeans.fit_predict(X_esc)

# La tabla que compara lo que encontro con lo que era
print("\n--- Tabla cruzada (Etiquetas reales vs Grupos K-Means) ---")
print(pd.crosstab(y, grupos))

# TODO RESUELTO: graficar los datos en el plano de PCA de la semana pasada,
# coloreando por GRUPO en vez de por etiqueta, y guardarla en figuras/clustering.png
pca = PCA(n_components=2)
componentes = pca.fit_transform(X_esc)
centros_pca = pca.transform(kmeans.cluster_centers_)

var_pc1 = pca.explained_variance_ratio_[0] * 100
var_pc2 = pca.explained_variance_ratio_[1] * 100

fig, ax = plt.subplots(figsize=(8, 6))

for grupo in sorted(set(grupos)):
    mascara = (grupos == grupo)
    ax.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        label=f"Grupo {grupo}",
        s=80,
        alpha=0.85,
        edgecolors='black'
    )

# Dibujar los centroides de K-Means proyectados en el plano PCA
ax.scatter(
    centros_pca[:, 0],
    centros_pca[:, 1],
    c='red',
    marker='X',
    s=200,
    edgecolors='black',
    linewidths=1.5,
    label='Centroides (K-Means)',
    zorder=5
)

# Etiquetar cada punto con su ventana para facilitar el analisis
for i, vent in enumerate(features['ventana']):
    ax.annotate(
        f"v{vent}",
        (componentes[i, 0], componentes[i, 1]),
        textcoords="offset points",
        xytext=(4, 4),
        fontsize=7,
        alpha=0.7
    )

ax.set_xlabel(f"PC1 ({var_pc1:.2f}% de varianza explicada)")
ax.set_ylabel(f"PC2 ({var_pc2:.2f}% de varianza explicada)")
ax.set_title("Agrupamiento K-Means (k=3) proyectado en plano PCA")
ax.legend(title="Asignación K-Means")
ax.grid(True, linestyle='--', alpha=0.5)

plt.savefig(ruta_figura, dpi=300, bbox_inches='tight')
plt.close()

print(f"\nGráfica guardada exitosamente en: {ruta_figura}")