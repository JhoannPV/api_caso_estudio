from flask import Blueprint, request
from models import clasificacion_model
from utils.response import success_response, error_response

clasificacion_bp = Blueprint("clasificacion", __name__, url_prefix="/api/clasificacion")


@clasificacion_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON invalido o vacio")

        features = clasificacion_model.features
        missing = [c for c in features if c not in data]
        if missing:
            return error_response(
                f"Faltan columnas: {missing}. Requeridas: {features}"
            )

        resultado = clasificacion_model.predecir(data)
        return success_response(resultado)

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)
