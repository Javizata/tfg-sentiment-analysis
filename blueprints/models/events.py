from flask_socketio import emit
from helpers import socketio
from flask import url_for
from app_state import APP_STATE
from services.models.model_registry import load_classic_models


@socketio.on("connect", namespace="/model_info")
def handle_connect():
    print("Cliente conectado en models")
    emit("server_message", {"data": "Conectado al servidor"})

@socketio.on("mensaje_cliente", namespace="/base")
def handle_message(data):
    print("Mensaje recibido:", data)
    emit("server_message", {"data": data})
    
@socketio.on("get_app_state", namespace="/model_info")
def get_state():
    emit("app_state", APP_STATE, namespace="/model_info")

@socketio.on("install_classic_models", namespace="/model_info")
def install_models():
    load_classic_models()
    emit("app_state", APP_STATE, namespace="/model_info")

@socketio.on("selected_models", namespace="/model_info")
def selected_models(data):
    
    if not APP_STATE["ready"]:
            emit(
                "error",
                {"message": "No hay modelos disponibles"},
                namespace="/stats"
            )
            return

    print(data)
    next_page = data.get("next")
    APP_STATE["models_to_use"] = data["models"]
    if next_page == "review":
        emit(
            "redirect",
            {"url": url_for("main.review")},
            namespace="/model_info"
        )

    elif next_page == "graphs":
        emit(
            "redirect",
            {"url": url_for("main.graphs")},
            namespace="/model_info"
        )

        
