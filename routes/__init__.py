from .agrupamiento import agrupamiento_bp


def register_routes(app):
    app.register_blueprint(agrupamiento_bp)
