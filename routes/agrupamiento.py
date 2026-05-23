from flask import Blueprint, request
from models import agrupamiento_model
from utils.response import success_response, error_response

agrupamiento_bp = Blueprint("agrupamiento", __name__, url_prefix="/api/agrupamiento")


@agrupamiento_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON invalido o vacio")

        from config import FEATURES
        missing = [c for c in FEATURES if c not in data]
        if missing:
            return error_response(f"Faltan columnas: {missing}. Requeridas: {FEATURES}")

        resultado = agrupamiento_model.predecir(data)
        return success_response(resultado)

    except Exception as e:
        return error_response(str(e), 500)
