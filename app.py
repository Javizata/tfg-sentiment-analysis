from flask import Flask
from config import Config
from helpers import socketio

# Importar rutas HTTP
from blueprints.main.routes import main
from blueprints.pipeline.routes import pipeline_bp
from blueprints.models.routes import models_bp
from blueprints.stats.routes import stats_bp


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # Inicializar Socket.IO
    socketio.init_app(app, cors_allowed_origins="*")

    # Registrar blueprints HTTP
    app.register_blueprint(main)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(models_bp)
    app.register_blueprint(stats_bp)

    # Registrar MÓDULOS DE EVENTOS (Socket.IO)
    import blueprints.main.events
    import blueprints.pipeline.events
    import blueprints.models.events
    import blueprints.stats.events

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)