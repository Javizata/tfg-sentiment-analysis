from flask import Flask
from config import Config
from helpers import socketio
from app_state import APP_STATE
from services.models.model_registry import load_classic_models
from services.models.distilbert_registry import load_distilbert_models
from services.models.artifact_state import update_app_state
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

    
    update_app_state()

    if APP_STATE["classic_ready"]:
        load_classic_models()
    if APP_STATE["distilbert_ready"]:
        load_distilbert_models()
    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True,use_reloader=False)