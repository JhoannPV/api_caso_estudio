# API de Agrupamiento - Calidad del Aire

API Flask que clasifica el nivel de contaminación (Bajo/Alto) usando KMeans
entrenado sobre las variables ambientales del dataset AirQualityUCI.

## Requisitos

- Python 3.10+

## Instalación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
python app.py
```

La API arranca en `http://localhost:3000`.

## Endpoint

```
POST /api/agrupamiento/predict
Content-Type: application/json

{
  "PT08.S1(CO)": 1360.0,
  "PT08.S2(NMHC)": 1046.0,
  "C6H6(GT)": 11.9,
  "NOx(GT)": 166.0
}
```

### Respuesta

```json
{
  "ok": true,
  "data": {
    "label": 1,
    "nivel": "Alto",
    "distancia_al_centroide": 1.8375,
    "centroide": {
      "C6H6(GT)": 18.98,
      "NOx(GT)": 424.67,
      "PT08.S1(CO)": 1354.19,
      "PT08.S2(NMHC)": 1255.37
    }
  }
}
```

- **label**: cluster asignado (0 = Bajo, 1 = Alto)
- **nivel**: etiqueta legible
- **distancia_al_centroide**: distancia euclidiana al centroide del cluster
- **centroide**: valores del centroide de referencia para las 4 variables

## Estructura

```
api_caso_estudio/
├── app.py                    # Entry point
├── config.py                 # Rutas, constantes
├── models/agrupamiento.py    # Entrenamiento y predicción
├── routes/agrupamiento.py    # Blueprint Flask
├── utils/response.py         # Helpers de respuesta
├── AirQualityUCI_preparado.csv  # Dataset (entrenamiento al arrancar)
└── requirements.txt
```
