import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class ClasificacionModel:
    def __init__(self):
        self.model = joblib.load(BASE_DIR / "modelo_clasificacion.pkl")
        self.features = joblib.load(BASE_DIR / "features_clasificacion.pkl")
        self.encoders = joblib.load(BASE_DIR / "encoders_clasificacion.pkl")
        self.cat_cols = list(self.encoders.keys())

    def _preparar_input(self, datos: dict) -> np.ndarray:
        df = pd.DataFrame([datos])
        for col in self.cat_cols:
            if col in df.columns:
                val = str(df[col].iloc[0])
                le = self.encoders[col]
                if val not in le.classes_:
                    raise ValueError(
                        f"Valor '{val}' no reconocido para '{col}'. "
                        f"Valores validos: {list(le.classes_)}"
                    )
                df[col] = le.transform([val])[0]
        return df[self.features].values

    def predecir(self, datos: dict) -> dict:
        X = self._preparar_input(datos)
        label = int(self.model.predict(X)[0])
        proba = self.model.predict_proba(X)[0]
        resultado = "Aprueba" if label == 1 else "Reprueba"
        return {
            "label": label,
            "resultado": resultado,
            "probabilidad_reprobar": round(float(proba[0]), 4),
            "probabilidad_aprobar": round(float(proba[1]), 4),
        }
