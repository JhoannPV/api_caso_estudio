import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.spatial.distance import cdist
from config import FEATURES

BASE_DIR = Path(__file__).resolve().parent.parent


class AgrupamientoModel:
    def __init__(self):
        artifacts = BASE_DIR / "artifacts"
        self.scaler = joblib.load(artifacts / "scaler_agrupamiento.pkl")
        self.model = joblib.load(artifacts / "kmeans_agrupamiento.pkl")
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
            "centroide": centroid,
        }
