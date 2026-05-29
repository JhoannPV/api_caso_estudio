from flask import Blueprint, request
from models import regresion_model
from utils.response import success_response, error_response

regresion_bp = Blueprint("regresion", __name__, url_prefix="/api/regresion")

@regresion_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON invalido o vacio")
        features = regresion_model.features
        required = ["longitude", "latitude", "housing_median_age", "total_bedrooms",
                     "median_income", "ocean_proximity", "rooms_per_household",
                     "population_per_household"]
        missing = [c for c in required if c not in data]
        if missing:
            return error_response(f"Faltan columnas: {missing}")
        resultado = regresion_model.predecir(data)
        return success_response(resultado)
    except Exception as e:
        return error_response(str(e), 500)
