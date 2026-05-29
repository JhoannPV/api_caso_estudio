import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OCEAN_MAP = {
    "<1H OCEAN": 0,
    "INLAND": 1,
    "NEAR OCEAN": 0,
    "NEAR BAY": 0,
    "ISLAND": 0,
}

class RegresionModel:
    def __init__(self):
        artifacts = BASE_DIR / "artifacts"
        self.model = joblib.load(artifacts / "modelo_regresion.pkl")
        self.features = joblib.load(artifacts / "features_regresion.pkl")

    def _preparar_input(self, datos: dict) -> np.ndarray:
        df = pd.DataFrame([datos])
        ocean_raw = df.pop("ocean_proximity").iloc[0] if "ocean_proximity" in df.columns else "NEAR BAY"
        df["ocean_INLAND"] = OCEAN_MAP.get(str(ocean_raw).strip(), 0)
        for col in self.features:
            if col not in df.columns:
                df[col] = 0
        return df[self.features].values

    def predecir(self, datos: dict) -> dict:
        X = self._preparar_input(datos)
        valor = float(self.model.predict(X)[0])
        return {
            "valor_predicho": round(valor, 2),
            "valor_formateado": f"${valor:,.0f}",
            "features_usadas": self.features,
        }
