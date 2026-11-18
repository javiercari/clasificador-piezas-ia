# pca.py - reduce las caracteristicas a dos componentes y las grafica
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Definir rutas relativas al proyecto
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
ruta_features = os.path.join(carpeta_proyecto, 'datos', 'features.csv')
ruta_figura = os.path.join(carpeta_proyecto, 'figuras', 'pca.png')

os.makedirs(os.path.join(carpeta_proyecto, 'figuras'), exist_ok=True)

features = pd.read_csv(ruta_features)
X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']          # NO se usa para calcular el PCA, solo para colorear

# Estandarización obligatoria antes de PCA
X_esc = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)
componentes = pca.fit_transform(X_esc)

var_pc1 = pca.explained_variance_ratio_[0] * 100
var_pc2 = pca.explained_variance_ratio_[1] * 100
var_total = pca.explained_variance_ratio_.sum() * 100

print("Varianza explicada por cada componente:", pca.explained_variance_ratio_)
print(f"Varianza acumulada de las dos: {var_total:.2f}%")

# TODO 1 RESUELTO: Graficar componentes[:,0] contra componentes[:,1], un color por etiqueta
fig, ax = plt.subplots(figsize=(8, 6))

for clase in sorted(y.unique()):
    mascara = (y == clase)
    ax.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        label=clase,
        s=75,
        alpha=0.85,
        edgecolors='black'
    )

# Etiquetar cada punto con su número de ventana para identificar atípicos
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
ax.set_title(f"Proyección PCA del Dataset (Varianza acumulada: {var_total:.2f}%)")
ax.legend(title="Clase")
ax.grid(True, linestyle='--', alpha=0.5)

# TODO 2 RESUELTO: Guardar la figura en figuras/pca.png
plt.savefig(ruta_figura, dpi=300, bbox_inches='tight')
plt.close()

print(f"Gráfica guardada exitosamente en: {ruta_figura}")