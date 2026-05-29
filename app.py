from flask import Flask, jsonify
from flask_cors import CORS
from routes import register_routes

app = Flask(__name__)
CORS(app)

register_routes(app)


@app.route("/")
def home():
    return jsonify({
        "api": "API de Casos de Estudio",
        "endpoints": {
            "POST /api/agrupamiento/predict": "Clasificar contaminacion en Bajo/Alto",
            "POST /api/clasificacion/predict": "Predecir exito estudiantil (Aprueba/Reprueba)",
            "POST /api/regresion/predict": "Predecir precio de vivienda (USD)"
        }
    })


if __name__ == "__main__":
    app.run(debug=True, port=3000)
