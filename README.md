# API de Casos de Estudio

API Flask con tres módulos: **Agrupamiento** (calidad del aire), **Clasificación**
(rendimiento estudiantil) y **Regresión** (precio de viviendas).
Los modelos se entrenan con datos del repositorio UCI y California Housing.

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

## Endpoints

### 1. Agrupamiento — Calidad del Aire

Clasifica el nivel de contaminación en **Bajo/Alto** usando KMeans pre-entrenado. El modelo se serializa desde el notebook `1. AGRUPAMIENTO/AnalisisCalidadAire.ipynb` y se carga desde `artifacts/` al iniciar la API, sin reentrenamiento.

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

**Respuesta:**

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

| Campo | Descripción |
|---|---|
| `label` | Cluster asignado (0 = Bajo, 1 = Alto) |
| `nivel` | Etiqueta legible |
| `distancia_al_centroide` | Distancia euclidiana al centroide |
| `centroide` | Valores del centroide de referencia |

### 2. Clasificación — Éxito Estudiantil

Predice si un estudiante **Aprueba o Reprueba** el curso de matemáticas usando
Gradient Boosting con 27 variables.

```
POST /api/clasificacion/predict
Content-Type: application/json

{
  "sex": "F",
  "age": 18,
  "famsize": "GT3",
  "Medu": 4,
  "Fedu": 4,
  "Mjob": "at_home",
  "Fjob": "teacher",
  "reason": "course",
  "guardian": "mother",
  "traveltime": 2,
  "studytime": 2,
  "failures": 0,
  "schoolsup": "yes",
  "famsup": "no",
  "paid": "no",
  "activities": "no",
  "nursery": "yes",
  "romantic": "no",
  "famrel": 4,
  "freetime": 3,
  "goout": 4,
  "Dalc": 1,
  "Walc": 1,
  "health": 3,
  "absences": 6,
  "G1": 5,
  "G2": 6
}
```

**Respuesta:**

```json
{
  "ok": true,
  "data": {
    "label": 0,
    "resultado": "Reprueba",
    "probabilidad_reprobar": 0.9957,
    "probabilidad_aprobar": 0.0043
  }
}
```

| Campo | Descripción |
|---|---|
| `label` | 0 = Reprueba, 1 = Aprueba |
| `resultado` | Etiqueta legible |
| `probabilidad_reprobar` | Probabilidad estimada de reprobar (0-1) |
| `probabilidad_aprobar` | Probabilidad estimada de aprobar (0-1) |

### 3. Regresión — Precio de Vivienda

Predice el valor de mercado de una vivienda en California usando
Gradient Boosting con 8 variables seleccionadas por RFECV.

```
POST /api/regresion/predict
Content-Type: application/json

{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41,
  "total_bedrooms": 129,
  "median_income": 8.3252,
  "ocean_proximity": "NEAR BAY",
  "rooms_per_household": 6.98,
  "population_per_household": 2.56
}
```

**Respuesta:**

```json
{
  "ok": true,
  "data": {
    "valor_predicho": 417313.39,
    "valor_formateado": "$417,313",
    "features_usadas": [
      "longitude", "latitude", "housing_median_age", "total_bedrooms",
      "median_income", "ocean_INLAND", "rooms_per_household",
      "population_per_household"
    ]
  }
}
```

| Campo | Descripción |
|---|---|
| `valor_predicho` | Precio estimado en USD |
| `valor_formateado` | Precio con formato legible |
| `features_usadas` | Lista de variables utilizadas por el modelo |

**Mapeo de `ocean_proximity`:**

| Valor original | `ocean_INLAND` |
|---|---|
| `<1H OCEAN` | 0 |
| `INLAND` | 1 |
| `NEAR OCEAN` | 0 |
| `NEAR BAY` | 0 |
| `ISLAND` | 0 |

### Valores válidos para campos categóricos

| Campo | Valores |
|---|---|
| `sex` | `F`, `M` |
| `famsize` | `LE3`, `GT3` |
| `Mjob`, `Fjob` | `teacher`, `health`, `services`, `at_home`, `other` |
| `reason` | `home`, `reputation`, `course`, `other` |
| `guardian` | `mother`, `father`, `other` |
| `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `romantic` | `yes`, `no` |

## Estructura

```
api_caso_estudio/
├── app.py                          # Entry point
├── config.py                       # Rutas, constantes (agrupamiento)
├── data/                           # Conjuntos de datos (CSV)
│   ├── AirQualityUCI_preparado.csv
│   └── student-mat.csv
├── artifacts/                      # Modelos serializados (.pkl)
│   ├── modelo_clasificacion.pkl
│   ├── features_clasificacion.pkl
│   ├── encoders_clasificacion.pkl
│   ├── modelo_regresion.pkl
│   ├── features_regresion.pkl
│   ├── scaler_agrupamiento.pkl
│   └── kmeans_agrupamiento.pkl
├── models/                         # Clases de los modelos
│   ├── agrupamiento.py             # KMeans + carga de artefactos serializados
│   ├── clasificacion.py            # Gradient Boosting + encoders
│   ├── regresion.py                # Gradient Boosting regressor
│   └── __init__.py                 # Instancias singleton
├── routes/                         # Blueprints Flask
│   ├── agrupamiento.py             # /api/agrupamiento
│   ├── clasificacion.py            # /api/clasificacion
│   ├── regresion.py                # /api/regresion
│   └── __init__.py                 # Registro de blueprints
├── utils/response.py               # Helpers JSON
├── requirements.txt
└── README.md
```
