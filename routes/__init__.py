from .agrupamiento import agrupamiento_bp
from .clasificacion import clasificacion_bp


def register_routes(app):
    app.register_blueprint(agrupamiento_bp)
    app.register_blueprint(clasificacion_bp)
