import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from config import DATA_PATH, FEATURES, N_CLUSTERS, RANDOM_STATE


class AgrupamientoModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=10)
        self.high_label: int | None = None
        self._entrenar()

    def _entrenar(self):
        df = pd.read_csv(DATA_PATH)
        X = df[FEATURES].values
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        centroids_orig = self.scaler.inverse_transform(self.model.cluster_centers_)
        self.high_label = int(np.argmax(centroids_orig[:, FEATURES.index("NOx(GT)")]))

    def predecir(self, datos: dict) -> dict:
        df_input = pd.DataFrame([datos])
        X = df_input[FEATURES].values
        X_scaled = self.scaler.transform(X)
        label = int(self.model.predict(X_scaled)[0])
        dists = cdist(X_scaled, self.model.cluster_centers_)[0]
        dist = float(dists[label])
        centroids_orig = self.scaler.inverse_transform(self.model.cluster_centers_)
        centroid = {
            FEATURES[i]: round(float(centroids_orig[label][i]), 4)
            for i in range(len(FEATURES))
        }
        nivel = "Alto" if label == self.high_label else "Bajo"
        return {
            "label": label,
            "nivel": nivel,
            "distancia_al_centroide": round(dist, 4),
            "centroide": centroid
        }
