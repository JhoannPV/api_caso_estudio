from flask import Flask, jsonify
from flask_cors import CORS
from routes import register_routes

app = Flask(__name__)
CORS(app)

register_routes(app)


@app.route("/")
def home():
    return jsonify({
        "api": "API de Agrupamiento - Calidad del Aire",
        "endpoints": {
            "POST /api/agrupamiento/predict": "Clasificar un registro en Bajo/Alto"
        }
    })


if __name__ == "__main__":
    app.run(debug=True, port=3000)
